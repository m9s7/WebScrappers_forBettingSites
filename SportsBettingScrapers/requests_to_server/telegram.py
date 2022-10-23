import sys
import requests

# Very simple
# https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2

# TOKEN = "5649589726:AAHu4l02-AA0EsmSn5k-hQqnDQ6jgBoSNqg"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())

# chat_id: 1678076367

TOKEN = "5649589726:AAHu4l02-AA0EsmSn5k-hQqnDQ6jgBoSNqg"
chat_id = "1678076367"


# message = "hello from your telegram bot"
# url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
# print(requests.get(url).json())

def broadcast_to_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    res = requests.get(url).json()
    if res['ok'] is not True:
        print("A U KURAC NIJE SE POSLALA PORUKE")
        sys.exit(1)
