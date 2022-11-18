import sys
import requests

# Very simple
# https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2

token_file_path = r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\requests_to_server\telegram_token'
with open(token_file_path) as f:
    TOKEN = f.readline().strip()
chat_id = "1678076367"


def broadcast_to_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    res = requests.get(url).json()
    if res['ok'] is not True:
        print("A U KURAC NIJE SE POSLALA PORUKA")
        sys.exit(1)
