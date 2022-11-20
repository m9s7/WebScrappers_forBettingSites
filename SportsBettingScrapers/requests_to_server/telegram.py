import json
import sys
import requests


# Very simple
# https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2


def init_token():
    token_file_path = r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\requests_to_server\telegram_token'
    with open(token_file_path) as f:
        _TOKEN = f.readline().strip()
    return _TOKEN


TOKEN = init_token()
chat_id = "1678076367"


def broadcast_to_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "text": msg,
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": chat_id
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.ok is not True:
        print("A U KURAC NIJE SE POSLALA PORUKA")
        print(json.dumps(response, indent=4))
        sys.exit(1)
