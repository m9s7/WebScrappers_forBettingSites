import requests

# TOKEN = "5649589726:AAHu4l02-AA0EsmSn5k-hQqnDQ6jgBoSNqg"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())

# chat_id: 1678076367

TOKEN = "5649589726:AAHu4l02-AA0EsmSn5k-hQqnDQ6jgBoSNqg"
chat_id = "1678076367"
message = "hello from your telegram bot"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json())