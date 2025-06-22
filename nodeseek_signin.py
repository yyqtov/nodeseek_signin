import os
import requests
import random
import time
import cloudscraper


def sign_in_with_cloudscraper():
    cookies = os.getenv('NODESEEK_COOKIE')
    if not cookies:
        raise ValueError("环境变量 NODESEEK_COOKIE 未设置")

    cookie_list = cookies.split('&')
    url = 'https://www.nodeseek.com/api/attendance?random=false'

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    for idx, cookie in enumerate(cookie_list):
        print(f"使用第 {idx + 1} 个账号进行签到...")

        random_delay = random.randint(20 * 60, 59 * 60)
        print(f"账号 {idx + 1} 之前将等待 {random_delay // 60} 分钟 {random_delay % 60} 秒...")
        time.sleep(random_delay)

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Length': '0',
            'Origin': 'https://www.nodeseek.com',
            'Referer': 'https://www.nodeseek.com/board',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }

        cookie_dict = {}
        for item in cookie.strip().split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                cookie_dict[key.strip()] = value.strip()

        try:
            response = scraper.post(url, headers=headers, cookies=cookie_dict, timeout=30)

            print(f"账号 {idx + 1} 的 Status Code:", response.status_code)
            print(f"账号 {idx + 1} 的 Response Content:", response.text)

            if response.status_code == 200:
                print(f"账号 {idx + 1} 签到成功")
            else:
                fail_message = f"NODESEEK账号 {idx + 1} 签到失败，响应内容：{response.text[:100]}"
                print(fail_message)
                send_tg_notification(fail_message)

        except Exception as e:
            error_message = f"NODESEEK账号 {idx + 1} 签到过程中发生异常: {e}"
            print(error_message)
            send_tg_notification(error_message)


def send_tg_notification(message):
    TELEGRAM_TOKEN = os.getenv('TG_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TG_USER_ID')

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


if __name__ == "__main__":
    try:
        sign_in_with_cloudscraper()
    except Exception as e:
        print(f"签到失败: {e}")
