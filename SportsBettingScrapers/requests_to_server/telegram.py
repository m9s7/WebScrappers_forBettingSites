import json
import sys
import requests


def init_token():
    token_file_path = r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\requests_to_server\telegram_token'
    with open(token_file_path) as f:
        _TOKEN = f.readline().strip()
    return _TOKEN


TOKEN = init_token()

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "disable_web_page_preview": False,
    "disable_notification": False,
    "reply_to_message_id": None,
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

dev_chat_id = "1678076367"
free_channel_id = "-1001875397817"
premium_channel_id = "-1001701172026"


def _broadcast_to_telegram(msg, chat_id):
    payload["text"] = msg
    payload["chat_id"] = chat_id

    response = requests.post(url, json=payload, headers=headers)

    if response.ok is not True:
        print("A U KURAC NIJE SE POSLALA PORUKA")
        print(json.dumps(response, indent=4))
        sys.exit(1)


def broadcast_to_free(msg):
    _broadcast_to_telegram(msg, free_channel_id)


def broadcast_to_premium(msg):
    _broadcast_to_telegram(msg, premium_channel_id)


def broadcast_to_dev(msg):
    _broadcast_to_telegram(msg, dev_chat_id)
