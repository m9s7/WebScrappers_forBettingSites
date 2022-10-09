import requests as r
from datetime import datetime


# # Get every "sport" currently offered in the sidebar and all leagues in that "sport"
# # it's possible to pass a list of sportIDs and leagueIDs and subGameIDs
# # url = "https://www.mozzartbet.com/getRegularGroups"
# # returns: [Sport dictionary]
#
# # Description of a Sport dictionary
# # "id": int           # Sport ID ex. 2
# # "name": string      # Sport name ex. "Košarka"
# # "count": int        # Num of matches currently offered in that sport ex. 61
# # "compets": []       # List of league dictionaries those matches are played in
# #
# # # Description of a League dictionary
# # "id": int           # League id ex. 26
# # "name": string      # League name ex. "EVROLIGA"
# # "shortName": string # League short name ex. "EVRL"
# # "count": int        # Num of matches curr offered in that league ex. 9
#
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

    return response


# # Gets a dictionary of all possible bets (subgames) you can potentially place for every sport (in general, not currently)
# # url = "https://www.mozzartbet.com/getAllGames"
# # returns a dictionary: key = sportID but as a string, value = [subgameSet dictionary]
#
# # Description of subgameSet dictionary
# # "id": string                      # subgameSet ID ex. "5ada3fc8df923343c250512b"
# # "name": string                    # subgameSet name ex. "Kompletna ponuda"
# # "subgameIds": []                  # list of all subgameIDs for that subgameSet
# # "prioritySubgameIds": []          # list of subgameIDs shown on the front page without having to expand the menu
# # "priorityHeaders": []             #
# # "regularHeaders": []              # list of headers and basically header = (game + subgames) wrapper
# #
# # ex.
# # Sport = Football (id = 1)
# #   subgameSet = "Kompletna ponuda" (id = 5ada3fc8df923343c250512b, spec for football)
# #       [header]
# #           game = "Konačan ishod" (id = -776604)
# #           subgame = "X" (id = 1001001002)
# #
# # # Header dictionary
# # "sportId": int                    # sportID ex. 1 for Football
# # "gameName": []                    # list - assume it contains only one Game dictionary
# # "subGameName": []                 # list which contains subgame dictionaries for that game
# # "specialOddValueType": "NONE",
# # "priority": false
# #
# # # Game dictionary
# # "id": -776604,
# # "languageCode": "sr",
# # "name": "Konačan ishod",
# # "shortName": "ki",
# # "description": null
# #
# # # Subgame dictionary
# # "id": 1001001002,
# # "languageCode": "sr",
# # "name": "X",
# # "shortName": null,
# # "description": "Meč će se završiti nerešenim rezultatom"
#
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

    return response


# # match id, start time, participants and their ids
# # url = "https://www.mozzartbet.com/betOffer2"
# # returns a {matches: [match dict], total: total_num_of_matches}
# #
# # # Match dictionary description
# # "id": int,                                      # match id ex. 6700725
# # "startTime": 1664935500000,                     # match start time in sec since epoch
# # "specialType": 0                                # interested only if specialType=0 else it's an unusable bonus pick
# # "competition_name_sr": "ATP  TOKIO  TVRDA",     # league name
# # "participants": []                              # list of 2 participant dict
# # irrelevant:
# # matchNumber, gameCounts, countKodds, oddsCount, mainMatch, competition
#
# # Participants dict desc
# # "id": 102475,
# # "description": "Kwon S.",
# # "name": "Kwon S.",
# # "shortName": "Kwon S."
#
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

    return response


# # Get odds for given matches and subgames
# # url = "https://www.mozzartbet.com/getBettingOdds"
# # returns a list of dictionaries, one for every match
# # Dictionary description
# # "id": int,                # match ID ex. 6698170
# # "gameCounts": {}          # irrelevant
# # "kodds": {}               # key = str(subgameID), val = subgame odds dict
# #
# # # Subgame odds dictctionary description
# # "id": 509689274,                  # irrelevant
# # "specialOddValue": "-1",          # irrelevant
# # "matchId": 6698170,               # irrelevant
# # "value": string,                  # string representation of subgame odds ex. "1.22"
# # "winStatus": "ACTIVE",            # irrelevant
# # "subGame":
# # {
# # "id": 1005017001,                                     # irrelevant
# # "subGameId": 1,                                       # irrelevant
# # "gameId": 17,                                         # irrelevant
# # "gameName": "Konačan ishod",                          # Game name
# # "subGameName": "1",                                   # Subgame name
# # "gameShortName": "ki",
# # "subGameDescription": "Shapovalov D. će pobediti na meču",
# # "specialOddValueType": "NONE",                        # irrelevant
# # "priority": false                                     # irrelevant
# # }
#
def get_odds(matches, subgames):
    url = "https://www.mozzartbet.com/getBettingOdds"

    payload = {
        "matchIds": matches,
        "subgames": subgames
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

    return response
