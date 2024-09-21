import requests
import json

# 指定包含 JSON 数据的 URL
url = "https://coscup.org/2024/json/session.json"  # 替换为实际的 URL

# 发送 GET 请求获取数据
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    try:
        # 解析 JSON 数据
        data = response.json()

        # 将 JSON 数据保存到文件
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print("JSON 数据已成功保存到 data.json 文件中")
    except json.JSONDecodeError as e:
        print(f"解析 JSON 数据时出错: {e}")
else:
    print(f"无法从 URL 获取数据, 状态码: {response.status_code}")
