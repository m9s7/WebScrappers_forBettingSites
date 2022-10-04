import requests as r


# # # Get every "sport" currently offered in the sidebar and all leagues in that "sport"
# # # there are no parameters
# # # url = "https://www.maxbet.rs/ibet/offer/sportsAndLeagues/-1.json"
# # # returns: list of dictionaries
# # "name": string,           # "Sport" name ex. "Strelac na mecu" ili "Tenis"
# # "leagues": []             # List of league dictionaries matches are played in
# # "sportType": string       # irrelevant enum
# #
# # # League dictionary description
# # "betLeagueId": 182879,              # League ID
# # "name": string,                     # League name ex. "Košarka EUROLEAGUE"
# # "leagueCode": 50684,                # idk?
# # "numOfMatches": int,                # Num of matches curr offered in that league ex. 9
# # irrelevant league attr:
# # flagId, leagueType, prepaymentDisabled, sortValue, sportName, imatchCBL,blocked, single, orderNumber, favorite, active, sport, description
#
def get_curr_sidebar_sports_and_leagues(session_cookie):
    url = "https://www.maxbet.rs/ibet/offer/sportsAndLeagues/-1.json"
    querystring = {"v": "4.48.18", "locale": "sr"}
    headers = {
        "cookie": f"SESSION={session_cookie}; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}

    response = r.request("GET", url, headers=headers, params=querystring)

    return response


# # # Get a list of dictionaries, on for every league in the "sport" (sport_dict arg),
# # # request_url = "https://www.maxbet.rs/ibet/offer/leagues//-1/0.json"
# # # returns: [League super dictionaries]
# #
# # # League super dictionaries description
# # "betLeagueId": 193931,            # league ID
# # "name": "ATP Nur-Sultan",         # league name
# # "matchList": [match dict]         # list od match dictionaries containing all the needed info
# # irrelevant:
# #   leagueCode, description, sport, active, favorite, orderNumber, singleblocked, imatchCBL
# #   flagId, numOfMatches, leagueType, prepaymentDisabled, sortValue, sportName
# #
# # # Match dictionary description
# # "id": 17528635,                           # match id
# # "home": "Cilic M.",                       # home team name
# # "away": "Otte O.",                        # away team name
# # "kickOffTime": 1664951400000,             # kickoff time in sec since epoch
# # "kickOffTimeString": "05.10. 08:30",      # kickoff time as string
# # "odBetPickGroups": []                     # list of odBetPickGroup dictionaries
# # "homeId": 206773,
# # "awayId": 790338,
# # irrelevant:
# #     round, matchCode, leagueId, status, single, blocked, favorite, iMatchCBL, odds, params
# #     haveOdds, leagueCode, sport, tipTypeGroupsCount, leagueName, sportName, oddsCount, leagueType
# #     leagueShortName, countryCode, brMatchId, virtualSport, ticketPrintType, matchInfo, leagueRiskLevel
# #     leagueSortValue, bonusDisabled
# #
# # # odBetPickGroup dictionary description
# # "name": "Konačan ishod",          # game name
# # "tipTypes": [subgame dict]        # list of subgame dicts
# # "handicapParamValue": string,     # null if not applicable ex. "22.5"
# # "handicapParamName": null,        # handicap parameter name ex. "overUnderGames" (null if not applicable)
# # irrelevant:
# #     id, description, sport, handicapParam, active, favorite, orderNumber, handicapParamDisplay, lastChangedTime
# #     showOnMain, showOnMobileMain, showOnSpecial, handicapParamMulti(?), specialBetValueType, formatCode, lineCode
# #     hideHeader, specialValuePosition, picksPerRow, instanceCode, sportTypeValue, showOnSuper, tmstmp,
# #     hidePicksWithoutOdd, betMedTranslation, picks, displaySpecifiers, showOnHeader
# #
# # # Subgame dictionary description
# # "description": string,              # ex. "Ukupan broj gemova na meču će biti veći od ponuđene granice"
# # "value": 1.32,                      # value as string ex. 1.85
# # "tipType": "KI_1",                  # tipType, name and caption are similar but can all slightly differ
# # "name": "1",
# # "caption": "1",
# # irrelevant: tipTypeId, tipTypeTag, mainType
#
def get_sport_data(sport_dict, session_cookie):
    request_url = "https://www.maxbet.rs/ibet/offer/leagues//-1/0.json"
    token = '#'.join([str(pair[1]) for pair in sport_dict['leagues']])
    query = {"v": "4.48.18", "locale": "sr", "token": token, "ttgIds": ""}
    header = {
        "cookie": f"SESSION={session_cookie}; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=sr"}

    sport_data_response = r.request("GET", request_url, headers=header, params=query)

    return sport_data_response
