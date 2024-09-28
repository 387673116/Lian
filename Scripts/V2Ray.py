import os
import requests
import base64
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

def check_ping(nodes):
    reachable_nodes = []
    for node in nodes:
        # 这里假设每个节点是一个 IP 地址或者域名
        if subprocess.run(["ping", "-c", "1", node], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            reachable_nodes.append(node)
    return reachable_nodes

# 主逻辑
if __name__ == "__main__":
    # 创建 json 目录（如果不存在）
    os.makedirs("json", exist_ok=True)

    # 获取并解码节点
    all_nodes = fetch_and_decode_urls(urls)
    print(f"所有节点: {all_nodes}")

    # 检查可达的节点
    reachable_nodes = check_ping(all_nodes)
    print(f"可达的节点: {reachable_nodes}")

    # 将可达节点保存到 json/V2Ray 文件
    with open("json/V2Ray", "w") as f:
        for node in reachable_nodes:
            f.write(node + "\n")

    print("可达的节点已保存到 'json/V2Ray'.")
