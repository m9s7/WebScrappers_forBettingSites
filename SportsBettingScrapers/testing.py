import requests as r

matches = [6745657, 6745690, 6747074, 6746227, 6745842, 6747139, 6746779, 6745617, 6746391, 6745828, 6745674, 6747019,
           6747023, 6746489, 6746374, 6746715, 6747124, 6746375, 6746381, 6747026, 6745492, 6745592, 6747160, 6746388,
           6747087, 6747065, 6746218, 6746204, 6746186, 6746192, 6746187, 6746783, 6746801, 6746805, 6746810, 6747028,
           6747054, 6747037, 6745479, 6746344, 6745501, 6745598, 6749757, 6745933]
subgames = [1001003008, 1001131009, 1001131010, 1001131008, 1001003012, 1001003013, 1001008001, 1001131015, 1001131016,
            1001003017, 1001008008, 1001008005, 1001003020, 1001008009, 1001008010, 1001142007, 1001003024, 1001003026,
            1001003027, 1001003034, 1001003001, 1001003002, 1001129001, 1001129002, 1001129003, 1001129004, 1001129005,
            1001129006, 1001129007, 1001142006, 1001128001, 1001128002, 1001128003, 1001128004, 1001128005, 1001128006,
            1001128007, 1001143001, 1001143002, 1001143003, 1001143004, 1001143005, 1001143006, 1001143007, 1001132001,
            1001132002, 1001132003, 1001008002, 1001132008, 1001132009, 1001132010, 1001009001, 1001008003, 1001009005,
            1001009002, 1001132015, 1001132016, 1001009008, 1001009009, 1001009003, 1001009010, 1001142003, 1001142001,
            1001142004, 1001142002, 1001131001, 1001131002, 1001131003, 1001003004, 1001003005, 1001142005, 1001003007]

url = "https://www.mozzartbet.com/getBettingOdds"
headers = {
    "cookie": "i18next=sr; SERVERID=MB-N7",
    "authority": "www.mozzartbet.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,bs;q=0.8",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.mozzartbet.com",
    "referer": "https://www.mozzartbet.com/sr",
    "x-requested-with": "XMLHttpRequest"
}

limit = 10

# Send one
_matches = matches[:limit]
matches = matches[limit:]

payload = {
    "matchIds": _matches,
    "subgames": subgames
}

response = r.request("POST", url, json=payload, headers=headers)
result = response.json()
# print(result, "\n\n\n\n\n")

# Send more if you need
while len(matches) > 0:
    _matches = matches[:limit]
    matches = matches[limit:]

    payload = {
        "matchIds": _matches,
        "subgames": subgames
    }

    response = r.request("POST", url, json=payload, headers=headers)

    # print(response.json(), "\n\n\n\n\n")
    result = result + response.json()

print(result)
