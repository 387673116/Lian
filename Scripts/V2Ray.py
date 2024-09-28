import os
import requests
import base64
import json
import subprocess
import re

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
            decoded_content = response.text.strip().splitlines()
            for line in decoded_content:
                if is_base64(line):
                    try:
                        decoded_line = base64.b64decode(line)
                        decoded_nodes.append(decoded_line)
                    except Exception as e:
                        print(f"解码失败: {line}，错误信息: {e}")
                else:
                    print(f"跳过无效的 Base64 字符串: {line}")
    return decoded_nodes

def is_base64(s):
    return re.match(r'^[A-Za-z0-9+/=]+$', s) is not None

def parse_proxy(config):
    if config.startswith(b"vless://"):
        return parse_vless(config)
    elif config.startswith(b"ss://"):
        return parse_ss(config)
    elif config.startswith(b"ssr://"):
        return parse_ssr(config)
    elif config.startswith(b"trojan://"):
        return parse_trojan(config)
    else:
        print(f"未知的协议: {config.decode(errors='ignore')}")
        return None

def parse_vless(config):
    try:
        decoded_bytes = base64.b64decode(config[8:])
        return json.loads(decoded_bytes.decode('utf-8'))
    except Exception as e:
        print(f"解析 vless 配置失败: {config.decode(errors='ignore')}，错误信息: {e}")
        return None

def get_ip_or_host(config):
    if config:
        # 提取 IP 或域名
        if "add" in config:
            return config["add"]
        elif "host" in config:
            return config["host"]
    return None

def extract_ip(node):
    match = re.search(r'@(.*?):', node.decode(errors='ignore'))
    return match.group(1) if match else None

def check_ping(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"出现错误: {e}")
        return False

# 主逻辑
if __name__ == "__main__":
    os.makedirs("json", exist_ok=True)

    all_nodes = fetch_and_decode_urls(urls)
    reachable_ips = set()  # 使用集合来存储唯一的可达 IP

    for node in all_nodes:
        config = parse_proxy(node)
        ip_or_host = extract_ip(node)

        if ip_or_host and check_ping(ip_or_host):
            reachable_ips.add(ip_or_host)  # 仅保留唯一的 IP
            print(f"可达的节点: {ip_or_host}")
        else:
            print(f"不可达的节点: {ip_or_host}")

    with open("json/V2Ray", "w") as f:
        for ip in reachable_ips:
            f.write(ip + "\n")

    print("可达的节点已保存到 'json/V2Ray'.")
