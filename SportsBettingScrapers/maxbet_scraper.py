import sys
import pandas as pd

from playwright.sync_api import sync_playwright

from models.match_model import Subgames
from requests_to_server.maxbet_requests import get_sport_data, get_curr_sidebar_sports_and_leagues


def get_cookie_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.maxbet.rs/", timeout=0)
        # page.click("button-2-style cookie-notification-button  ng-binding")

        cookies = context.cookies()
        cookie_for_requests = next(c['value'] for c in cookies if c['name'] == 'SESSION')

        browser.close()
    return cookie_for_requests


def parse_sidebar_sports(sidebar_sports_json):
    sports = []

    for sport in sidebar_sports_json:
        my_sport = {
            'name': sport['name'],
            'leagues': [],
        }
        for league_dict in sport['leagues']:
            if str(league_dict['name']).startswith("Max Bonus Tip"):
                continue
            my_sport['leagues'].append((league_dict['name'], league_dict['betLeagueId']))

        if len(my_sport['leagues']) != 0:
            sports.append(my_sport)
            # print(json.dumps(my_sport, indent=4, separators=(',', ': ')))
    return sports


def parse_sport_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:
            e = [match['home'], match['away'], None, None]
            for i in match['odBetPickGroups']:
                for j in i['tipTypes']:
                    if j['tipType'] == "KI_1":
                        e[Subgames.KI_1] = j['value']
                    elif j['tipType'] == "KI_2":
                        e[Subgames.KI_2] = j['value']
                    else:
                        continue
            export[match['id']] = e

    columns = ['1', '2', 'KI_1', 'KI_2']
    index = list(export.keys())

    # , index = index
    df = pd.DataFrame(list(export.values()), columns=columns)

    # print(df.to_string())
    return df


def print_to_file(data):
    original_stdout = sys.stdout
    with open('maxb_tennis.txt', 'w', encoding="utf-8") as f:
        sys.stdout = f
        print(data)
        sys.stdout = original_stdout


def scrape():
    cookie = get_cookie_playwright()
    sidebar_sports_response_json = get_curr_sidebar_sports_and_leagues(cookie).json()

    # parsed sidebar_sports is a list of dictionaries
    # {
    #     "name": string,                   # Sport name
    #     "leagues": [(string, int)]        # list of pairs < League_name, League ID >
    # }
    sidebar_sports = parse_sidebar_sports(sidebar_sports_response_json)

    # Get data for every sport or just IDs for every sport

    sport_ids = {}
    for i, sport in enumerate(sidebar_sports):
        # print(f"{i}: ", sport['name'])
        sport_ids[sport['name']] = i
        # res_json = get_sport_data(sport, cookie).json()

    sport_data_response_json = get_sport_data(sidebar_sports[sport_ids['Tenis']], cookie).json()

    result = parse_sport_data(sport_data_response_json)

    print_to_file(result.to_string())
    return result
