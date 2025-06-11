import os
from curl_cffi import requests
import random
import time

# 从环境变量获取 COOKIE，多个cookie用&分隔
cookies = os.getenv('NODESEEK_COOKIE')
# 从环境变量获取 TG_BOT_TOKEN和TG_USER_ID
TELEGRAM_TOKEN = os.getenv('TG_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_USER_ID')
# Telegram通知函数
def send_tg_notification(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            params = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print("Telegram通知发送成功")
            else:
                print(f"Telegram通知发送失败: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Telegram通知发送失败: {e}")
    else:
        print("Telegram配置不完整，无法发送通知")

if not cookies:
    raise ValueError("环境变量 NODESEEK_COOKIE 未设置")

# 将多个cookie以&为分隔符拆分成一个列表
cookie_list = cookies.split('&')

# 设置请求的URL
url = 'https://www.nodeseek.com/api/attendance?random=false'

# 设置请求头
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Length': '0',  # 请求体为空
    'Origin': 'https://www.nodeseek.com',
    'Referer': 'https://www.nodeseek.com/board',
    'Sec-CH-UA': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 遍历多个账号的cookie进行签到
for idx, cookie in enumerate(cookie_list):
    print(f"使用第 {idx+1} 个账号进行签到...")
    # 在每次请求前随机生成一个 20 到 59 分钟之间的延迟（单位为秒）
    random_delay = random.randint(20 * 60, 59 * 60)
    print(f"账号 {idx+1} 之前将等待 {random_delay // 60} 分钟 {random_delay % 60} 秒...")
    
    # 加入延迟
    time.sleep(random_delay)
    # 设置当前cookie
    headers['Cookie'] = cookie.strip()  # 去掉空格，设置Cookie头
    
    try:
        # 发起POST请求
        response = requests.post(url, headers=headers, impersonate="chrome110")
        
        # 输出返回的状态码和响应内容
        print(f"账号 {idx+1} 的 Status Code:", response.status_code)
        print(f"账号 {idx+1} 的 Response Content:", response.text)
        
        # 根据响应内容判断签到状态
        if response.status_code == 200:
            print(f"账号 {idx+1} 签到成功")
        else:
            # 截断响应内容
            fail_message = f"NODESEEK账号 {idx+1} 签到失败，响应内容：{response.text[:100]}" if len(response.text) > 100 else f"NODESEEK账号 {idx+1} 签到失败，响应内容：{response.text}"
            print(fail_message)
            # 失败时发送 Telegram 通知
            send_tg_notification(fail_message)
    
    except Exception as e:
        error_message = f"NODESEEK账号 {idx+1} 签到过程中发生异常: {e}"
        print(error_message)
        # 异常时发送 Telegram 通知
        send_tg_notification(error_message)
