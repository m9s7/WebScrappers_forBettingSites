import json

import requests

url = "https://www.maxbet.rs/ibet/offer/leagues//-1/0.json"

querystring = {"v": "4.48.18", "locale": "sr", "token": "193931", "ttgIds": ""}

payload = ""
headers = {
    # SESSION=521adc42-49a5-4b98-aad9-d1d52c5cdfc6;
    "cookie": "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(json.dumps(response.json(), indent=4, separators=(',', ': ')))
print(len(response.json()))
