import requests
import base64
import subprocess

# 定义要获取的链接
urls = [
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless",
    "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt"
]

# 存储可达的地址
reachable_nodes = []

# 获取内容并解码
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        decoded_data = base64.b64decode(response.text).decode('utf-8')

        # 按行分割
        lines = decoded_data.splitlines()
        
        # 检查每一行地址的可达性
        for line in lines:
            if line.strip():  # 确保不是空行
                # 使用 ping 命令检查地址可达性
                result = subprocess.run(["ping", "-c", "1", line], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    reachable_nodes.append(line)

    except Exception as e:
        print(f"Error processing {url}: {e}")

# 将可达地址保存到新的文件
with open('V2Ray_subscriptions.txt', 'w') as f:
    for node in reachable_nodes:
        f.write(f"{node}\n")

print("可达的节点已保存到 'V2Ray_subscriptions.txt'.")
