import os
import requests
import base64
import json
import subprocess
import re

# 定义要获取内容的链接（去除了指定的链接）
urls = [
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless"
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
                        decoded_nodes.append(decoded_line.decode('utf-8'))
                    except Exception as e:
                        print(f"解码失败: {line}，错误信息: {e}")
                else:
                    print(f"跳过无效的 Base64 字符串: {line}")
    return decoded_nodes

def is_base64(s):
    return re.match(r'^[A-Za-z0-9+/=]+$', s) is not None

def extract_host(node):
    match = re.search(r'@([\w.-]+):', node)
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
    reachable_nodes = []
    unreachable_nodes = []

    for node in all_nodes:
        if '@' not in node:
            print(f"剔除不包含 '@' 的节点: {node}")
            continue

        host = extract_host(node)

        if host:
            if check_ping(host):
                reachable_nodes.append(node)
                print(f"可达的节点: {node}")
            else:
                unreachable_nodes.append(node)
                print(f"不可达的节点: {node}")

    # 保存可达和不可达的节点
    with open("json/V2Ray", "w") as f:
        f.write("可达的节点:\n")
        for node in reachable_nodes:
            f.write(node + "\n")
        f.write("\n不可达的节点:\n")
        for node in unreachable_nodes:
            f.write(node + "\n")

    print("可达和不可达的节点已保存到 'json/V2Ray'.")
