# don't need cookies for mozart

import requests as r
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d')


def get_football():
    for sport in list_of_curr_sports_dictionaries:
        if sport['name'] == 'Fudbal':
            # Can return list of ( sportId, sportName ) pairs, because IDs are needed to get subgames
            print("Football id: ", sport['id'])
            return sport
    return None


def get_curr_sports():
    url = "https://www.mozzartbet.com/getRegularGroups"
    payload = {
        "date": date,
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


list_of_curr_sports_dictionaries = get_curr_sports().json()

# # Description of a Sport dictionary
# "id": int           # sport ID
# "name": string      # sport name
# "count": int        # total games curr offered for that sport
# "compets": []       # list of league dictionaries
#
# # Description of a League dictionary
# "id": int           # league id
# "name": string      # league name
# "shortName": string # league short name
# "count": int        # num of games curr played in that league

# Get football

football = get_football()

if football is None:
    print("Send email")
    exit(1)

# Get subgameIds za "Konacan ishod"

all_subgames_dictionary = get_all_subgames().json()
# Fomat:
# all_subgames_dictionary is a map where keys are ordered integers [1..77]
# and values are lists which contain subgame dictionaries


# Sport = Football (id = 1)
#   Offer = "Kompletna ponuda" (id = 5ada3fc8df923343c250512b, spec for football)
#       header
#           game = "Konačan ishod" (id = -776604)
#           subgame = "X" (id = 1001001002)

# # Description of subgame dictionary
# "id": string                      # subgame ID ex. "5ada3fc8df923343c250512b"
# "name": string                    # subgame name ex. "Kompletna ponuda"
# "subgameIds": []                  # just a list of subgameIDs, no idea why they are grouped there
# "prioritySubgameIds": []          # list of subgameIDs shown on the front page without having to expand menu
# "priorityHeaders": []             #
# "regularHeaders": []              # list of headers and basically header = game wrapper

# # Header dictionary
# "sportId": int                    # sportID ex. 1 for Football
# "gameName": []                    # list which usually contains one Game dictionary
# "subGameName": []                 # list which contains Subgame dictionaries for that game
# "specialOddValueType": "NONE",
# "priority": false

# # Game dictionary
# "id": -776604,
# "languageCode": "sr",
# "name": "Konačan ishod",
# "shortName": "ki",
# "description": null

# # Subgame dictionary
# "id": 1001001002,
# "languageCode": "sr",
# "name": "X",
# "shortName": null,
# "description": "Meč će se završiti nerešenim rezultatom"

footballID = football['id']

offerList = all_subgames_dictionary[str(footballID)]

for offer in offerList:
    if offer['name'] != "Konačan ishod":
        continue
    offerID = offer['id']
    print("Offer name ", offer['name'])
    for header in offer['regularHeaders']:
        for game in header['gameName']:
            gameID = game['id']
            gameName = game['name']  # postoji i shortName (ex. Konačan ishod = ki)
            if gameName != "Konačan ishod":
                continue
            print("Game name: ", gameName)
        print("Subgames: ")
        for subgame in header['subGameName']:
            subgameID = subgame['id']
            subgameName = subgame['name']
            subgameDesc = subgame['description']
            print(subgameID, " - ", subgameName, " (", subgameDesc, ")")

# TODO: separate response data structure documentation into a separate file
# TODO: switch first implementation from football to tennis because its even simpler
