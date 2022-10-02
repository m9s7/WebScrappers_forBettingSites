import requests as r

from playwright.sync_api import sync_playwright


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


def get_sports(session_cookie):
    url = "https://www.maxbet.rs/ibet/offer/sportsAndLeagues/-1.json"
    querystring = {"v": "4.48.18", "locale": "sr"}
    headers = {
        "cookie": f"SESSION={session_cookie}; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}

    response = r.request("GET", url, headers=headers, params=querystring)

    return response


def get_sport_data(sport_dict, session_cookie):
    request_url = "https://www.maxbet.rs/ibet/offer/leagues//-1/0.json"
    token = '#'.join([str(pair[1]) for pair in sport_dict['leagues']])
    query = {"v": "4.48.18", "locale": "sr", "token": token, "ttgIds": ""}
    header = {
        "cookie": f"SESSION={session_cookie}; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}

    sport_data_response = r.request("GET", request_url, headers=header, params=query)

    return sport_data_response


# Program

cookie = get_cookie_playwright()

get_sports_response_json = get_sports(cookie).json()

# Parse response

sports = []
for i in get_sports_response_json:
    sport = {
        'name': i['name'],
        'leagues': [],
    }
    for league in i['leagues']:
        sport['leagues'].append((league['name'], league['betLeagueId']))

    if len(sport['leagues']) != 0:
        sports.append(sport)
        # print(json.dumps(sport, indent=4, separators=(',', ': ')))

# Get data for every sport

for sport in sports:
    # print(sport['name'])
    res_json = get_sport_data(sport, cookie).json()

    # Playing around
    # res_json = get_sport_data(sports[10], cookie).json()
    for league in res_json:
        print("LEAGUE NAME: ", league['name'])
        print("matchList length: ", len(league['matchList']))
        for match in league['matchList']:
            print('HOME: ', match['home'], " - vs - ", "AWAY: ", match['away'])
            print(match['kickOffTime'], " is ", match['kickOffTimeString'])
            print('\n')
            for i in match['odBetPickGroups']:
                for j in i['tipTypes']:
                    if j['value'] != 0:
                        print(i['name'])
                        print(j['tipType'], " -  ", j['name'], " - ", j['value'])
        print('\n\n')

# TODO: Decide how to organize and store data for arbitrage after seeing how data from MOZART looks like
