import sys

from playwright.sync_api import sync_playwright

from models.match_model import Match, Participant, Subgame
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
            my_sport['leagues'].append((league_dict['name'], league_dict['betLeagueId']))

        if len(my_sport['leagues']) != 0:
            sports.append(my_sport)
            # print(json.dumps(my_sport, indent=4, separators=(',', ': ')))
    return sports


cookie = get_cookie_playwright()
response = get_curr_sidebar_sports_and_leagues(cookie).json()

# parsed sidebar_sports is a list of dictionaries
# {
#     "name": string,                   # Sport name
#     "leagues": [(string, int)]        # list of pairs < League_name, League ID >
# }
sidebar_sports = parse_sidebar_sports(response)

# Get data for every sport

# for sport in sports:
#     # print(sport['name'])
#     res_json = get_sport_data(sport, cookie).json()

# basket id = 4
tenisID = 6

res_json = get_sport_data(sidebar_sports[tenisID], cookie).json()

# class Match:
#     def __init__(self, match_id, start_time, participants=None, subgames=None):

matches = {}
for league in res_json:
    # print("LEAGUE NAME: ", league['name'])
    # print("matchList length: ", len(league['matchList']))
    for match in league['matchList']:
        # print(match['id'])
        m = Match(
            match_id=match['id'],
            start_time=match['kickOffTime'],
            participants=[
                Participant(match['homeId'], match['home']),
                Participant(match['awayId'], match['away'])
            ]
        )
        # print('HOME: ', match['home'], " - vs - ", "AWAY: ", match['away'])
        # print(match['kickOffTime'], " is ", match['kickOffTimeString'])
        for i in match['odBetPickGroups']:
            for j in i['tipTypes']:
                # maybe j['value'] != 0 is bad
                if j['value'] != 0 and (j['tipType']).startswith("KI_"):
                    s = Subgame(
                        game_name=i['name'],
                        game_shortname=j['tipType'],
                        subgame_name=j['name'],
                        subgame_description=j['description'],
                        value=j['value']
                    )
                    m.subgames.append(s)
                    # print(i['name'])
                    # print(j['tipType'], " -  ", j['name'], " - ", j['value'])
        matches[match['id']] = m
        # print(m)

# # Print results
# for m in matches.values():
#     print(m)

original_stdout = sys.stdout
with open('maxb_tennis.txt', 'w', encoding="utf-8") as f:
    sys.stdout = f
    for m in matches.values():
        print(m)
    sys.stdout = original_stdout
