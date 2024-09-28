import os
import requests
import base64
import json
import subprocess

# 定义要获取内容的链接
urls = [
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless",
    "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt"
]

def fetch_and_decode_urls(urls):
    decoded_nodes = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            # Base64 解码
            decoded_content = response.text.strip().splitlines()
            for line in decoded_content:
                try:
                    decoded_line = base64.b64decode(line).decode('utf-8')
                    decoded_nodes.append(decoded_line)
                except (ValueError, UnicodeDecodeError) as e:
                    print(f"解码失败: {line}，错误: {e}")
    return decoded_nodes

def parse_proxy(config):
    if config.startswith("vmess://"):
        return parse_vmess(config)
    elif config.startswith("vless://"):
        return parse_vless(config)
    elif config.startswith("ss://"):
        return parse_ss(config)
    elif config.startswith("ssr://"):
        return parse_ssr(config)
    elif config.startswith("trojan://"):
        return parse_trojan(config)
    else:
        print(f"未知的协议: {config}")
        return None

def parse_vmess(config):
    decoded_bytes = base64.b64decode(config[8:])  # 去掉前缀 "vmess://"
    return json.loads(decoded_bytes.decode('utf-8'))

def parse_vless(config):
    decoded_bytes = base64.b64decode(config[8:])  # 去掉前缀 "vless://"
    return json.loads(decoded_bytes.decode('utf-8'))

def parse_ss(config):
    decoded_bytes = base64.b64decode(config[5:])  # 去掉前缀 "ss://"
    # 实现解析逻辑
    return None  # 返回解析结果

def parse_ssr(config):
    decoded_bytes = base64.b64decode(config[5:])  # 去掉前缀 "ssr://"
    # 实现解析逻辑
    return None  # 返回解析结果

def parse_trojan(config):
    decoded_bytes = base64.b64decode(config[8:])  # 去掉前缀 "trojan://"
    # 实现解析逻辑
    return None  # 返回解析结果

def get_ip_or_host(config):
    if config:
        # 从配置中获取 IP 或域名
        if "add" in config:
            return config["add"]
        elif "host" in config:
            return config["host"]
    return None

def check_ping(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],  # 对于 Windows 可以改成 ["ping", "-n", "1", host]
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # 使输出为字符串而不是字节
        )
        print(f"Ping 输出: {result.stdout}")  # 打印输出
        return result.returncode == 0
    except Exception as e:
        print(f"出现错误: {e}")  # 捕获并打印异常
        return False

# 主逻辑
if __name__ == "__main__":
    # 创建 json 目录（如果不存在）
    os.makedirs("json", exist_ok=True)

    # 获取并解码节点
    all_nodes = fetch_and_decode_urls(urls)

    reachable_configs = []

    for node in all_nodes:
        config = parse_proxy(node)  # 使用新的解析函数
        ip_or_host = get_ip_or_host(config)

        if ip_or_host and check_ping(ip_or_host):
            reachable_configs.append(node)  # 保留可达的配置
            print(f"可达的节点: {ip_or_host}")
        else:
            print(f"不可达的节点: {ip_or_host}")

    # 将可达的节点保存到 json/V2Ray 文件
    with open("json/V2Ray", "w") as f:
        for node in reachable_configs:
            f.write(node + "\n")

    print("可达的节点已保存到 'json/V2Ray'.")
