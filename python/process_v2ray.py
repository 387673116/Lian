import requests
import base64
import subprocess

# 定义链接
links = [
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless",
    "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt",
]

# 创建一个空的最终文件
output_file = 'json/v2ray'
with open(output_file, 'w') as f:
    for link in links:
        response = requests.get(link)
        if response.status_code == 200:
            try:
                # Base64 解码
                content = base64.b64decode(response.text).decode('utf-8')
                # 逐行处理
                for line in content.splitlines():
                    # 提取地址并 ping 通
                    address = line.split('://')[1].split(':')[0]  # 提取地址
                    try:
                        # 检查地址是否可 ping 通
                        subprocess.run(['ping', '-c', '1', address], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        f.write(line + '\n')  # 如果 ping 通，写入文件
                    except Exception as e:
                        print(f"Ping failed for {address}: {e}")
            except Exception as e:
                print(f"Failed to decode content from {link}: {e}")

print(f"V2Ray subscription file updated at {output_file}")
