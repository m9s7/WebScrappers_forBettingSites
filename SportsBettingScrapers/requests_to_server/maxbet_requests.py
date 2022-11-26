import requests as r
from requests import JSONDecodeError

from requests_to_server.telegram import broadcast_to_dev

# add SESSION = {session_cookie}; to header, if cookies ever become necessary
header = {
    "cookie": "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}


def get_curr_sidebar_sports_and_leagues():
    url = "https://www.maxbet.rs/ibet/offer/sportsAndLeagues/-1.json"
    querystring = {"v": "4.48.18", "locale": "sr"}

    response = r.request("GET", url, headers=header, params=querystring)

    if not response.ok:
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError:
        broadcast_to_dev("JSONDecodeError u get_curr_sidebar_sports_and_leagues")
        return None


def get_match_ids(league_list):
    request_url = "https://www.maxbet.rs/ibet/offer/leagues//-1/0.json"
    token = '#'.join([str(league) for league in league_list])
    query = {"v": "4.48.18", "locale": "sr", "token": token, "ttgIds": ""}

    response = r.request("GET", request_url, headers=header, params=query)
    if not response.ok:
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError:
        broadcast_to_dev("JSONDecodeError u get_match_ids")
        return None


def get_match_data(match_id):
    url = f"https://www.maxbet.rs/ibet/offer/special/undefined/{match_id}.json"
    querystring = {"v": "4.48.18", "locale": "sr"}

    print(f"\r{match_id}", end='')

    try:
        response = r.request("GET", url, headers=header, params=querystring)
    except Exception as e:
        print("SKIPPED MATCH: ", match_id)
        print(e)
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError:
        broadcast_to_dev("JSONDecodeError u get_match_data")
        return None
