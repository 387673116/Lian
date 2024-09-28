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
            decoded_content = base64.b64decode(response.text).decode('utf-8')
            decoded_nodes.extend(decoded_content.splitlines())
    return decoded_nodes

def parse_vmess_or_vless(config):
    try:
        # 如果是 VMess
        if config.startswith("vmess://"):
            decoded_bytes = base64.b64decode(config[8:])  # 去掉前缀 "vmess://"
            return json.loads(decoded_bytes.decode('utf-8'))
        
        # 如果是 VLESS
        elif config.startswith("vless://"):
            decoded_bytes = base64.b64decode(config[8:])  # 去掉前缀 "vless://"
            return json.loads(decoded_bytes.decode('utf-8'))
        
    except Exception as e:
        print(f"解析失败: {e}")
        return None

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
            ["ping", "-c", "1", host],  # 对于 Windows 可以改成 ["ping", "-n", "1", host]
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # 使输出为字符串而不是字节
        )
        if result.returncode == 0:
            return True
        else:
            print(f"Ping失败: {result.stderr}")  # 打印错误信息
            return False
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
        config = parse_vmess_or_vless(node)
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
