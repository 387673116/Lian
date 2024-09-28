import base64
import requests
import subprocess
import os

# 确保 json 目录存在
os.makedirs('json', exist_ok=True)

links = [
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless",
    "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt"
]

all_data = ""
for link in links:
    response = requests.get(link)
    all_data += response.text

# 解码 Base64
decoded_data = base64.b64decode(all_data).decode('utf-8')

valid_addresses = []
for line in decoded_data.splitlines():
    try:
        # Ping 地址
        subprocess.run(["ping", "-c", "1", line], check=True)
        valid_addresses.append(line)
    except subprocess.CalledProcessError:
        continue

# 保存有效地址到 json/v2ray.new 文件
with open('json/v2ray.new', 'w') as f:
    f.write('\n'.join(valid_addresses))
