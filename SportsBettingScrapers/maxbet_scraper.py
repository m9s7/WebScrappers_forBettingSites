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


url = "https://www.maxbet.rs/ibet/offer/sportsAndLeagues/-1.json"

querystring = {"v": "4.48.18", "locale": "sr"}
cookie = get_cookie_playwright()

headers = {"cookie": f"SESSION={cookie}; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}
response = r.request("GET", url, headers=headers, params=querystring)

# print(response.text)
print(response.json())

# TODO: extract 'name' and for every sport name extract 'betLeagueId' that are played
