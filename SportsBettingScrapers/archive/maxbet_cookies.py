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


def load_cookie():
    with open('persistent_data/cookie.txt') as f:
        lines = f.readlines()
        print(len(lines))
        if len(lines) == 0:
            cookie = get_cookie_playwright()
        else:
            cookie = lines[0]

    return cookie
