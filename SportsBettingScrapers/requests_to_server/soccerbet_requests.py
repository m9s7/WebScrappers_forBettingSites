import requests as r
from requests import JSONDecodeError

from requests_to_server.telegram import broadcast_to_dev


def get_curr_sidebar_league_ids():
    url = "https://soccerbet.rs/api/Prematch/GetCompetitionFilter"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers)
    if not response.ok:
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError as e:
        print(e)
        broadcast_to_dev("JSONDecodeError u get_curr_sidebar_league_ids (socc)\n")
        broadcast_to_dev(str(e))
        return None
    except Exception as e:
        print(e)
        broadcast_to_dev(str(e))
        return None


def get_master_data():
    url = "https://soccerbet.rs/api/MasterData/GetMasterData"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers)
    if not response.ok:
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError as e:
        print(e)
        broadcast_to_dev("JSONDecodeError u get_master_data (socc)\n")
        broadcast_to_dev(str(e))
        return None
    except Exception as e:
        print(e)
        broadcast_to_dev(str(e))
        return None


def get_league_matches_info(league_id):
    url = "https://soccerbet.rs/api/Prematch/GetCompetitionMatches"

    querystring = {"competitionId": str(league_id)}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError as e:
        print(e)
        broadcast_to_dev("JSONDecodeError u get_league_matches_info (socc)\n")
        broadcast_to_dev(str(e))
        return None
    except Exception as e:
        print(e)
        broadcast_to_dev(str(e))
        return None


def get_match_odd_values(match_id):
    url = "https://soccerbet.rs/api/Prematch/GetMatchBets"

    querystring = {"matchId": str(match_id)}
    headers = {
        "cookie": "ASP.NET_SessionId=kl2d4ouy2rvsbmdhtmni1q3o",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    print(f"\r{match_id}", end='')

    response = r.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        return None

    try:
        result = response.json()
        return result
    except JSONDecodeError as e:
        print(e)
        broadcast_to_dev("JSONDecodeError u get_match_odd_values (socc)\n")
        broadcast_to_dev(str(e))
        return None
    except Exception as e:
        print(e)
        broadcast_to_dev(str(e))
        return None
