import requests as r
from datetime import datetime


def get_curr_sidebar_sports_and_leagues():
    url = "https://www.mozzartbet.com/getRegularGroups"
    payload = {
        "date": datetime.today().strftime('%Y-%m-%d'),
        "sportIds": [],
        "competitionIds": [],
        "sort": "bycompetition",
        "specials": None,
        "subgames": [],
        "size": 1000,
        "mostPlayed": False,
        "type": "betting",
        "numberOfGames": 0,
        "activeCompleteOffer": False,
        "lang": "sr",
        "offset": 0
    }
    headers = {
        "cookie": "i18next=sr; SERVERID=MB-N7",
        "authority": "www.mozzartbet.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,bs;q=0.8",
        "dnt": "1",
        "origin": "https://www.mozzartbet.com",
        "referer": "https://www.mozzartbet.com/sr",
        "x-requested-with": "XMLHttpRequest"
    }

    response = r.request("POST", url, json=payload, headers=headers)
    if not response.ok:
        return None

    return response.json()


def get_all_subgames():
    url = "https://www.mozzartbet.com/getAllGames"
    headers = {
        "cookie": "i18next=sr; SERVERID=MB-N7",
        "authority": "www.mozzartbet.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,bs;q=0.8",
        "referer": "https://www.mozzartbet.com/sr"
    }

    response = r.request("GET", url, headers=headers)
    if not response.ok:
        return None

    return response.json()


def get_match_ids(sport_id=None):
    url = "https://www.mozzartbet.com/betOffer2"

    payload = {
        "date": datetime.today().strftime('%Y-%m-%d'),
        "sportIds": ([sport_id] if sport_id is not None else []),
        "competitionIds": [],
        "sort": "bycompetition",
        "specials": False,
        "subgames": [],
        "size": 1000,
        "mostPlayed": False,
        "type": "betting",
        "numberOfGames": 1000,
        "activeCompleteOffer": False,
        "lang": "sr",
        "offset": 0
    }
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

    response = r.request("POST", url, json=payload, headers=headers)
    if not response.ok:
        return None

    return response.json()


def get_odds(matches, subgames):
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

    limit = 49

    # Send one
    _matches = matches[:limit]
    matches = matches[limit:]

    payload = {
        "matchIds": _matches,
        "subgames": subgames
    }

    response = r.request("POST", url, json=payload, headers=headers)
    result = response.json()

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

    return result
