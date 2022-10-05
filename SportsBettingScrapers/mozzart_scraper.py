# don't need cookies for mozart
import sys

from models.match_model import Match, Participant, Subgame
from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames, get_match_ids, \
    get_odds


# Get a specific "sport" that is currently offered
def get_sport_with_name(name):
    for sport in sidebar_sports:
        if sport['name'] == name:
            # Can return list of ( sportId, sportName ) pairs, because IDs are needed to get subgames
            print(name, " id: ", sport['id'])
            return sport
    return None


# Focused subgames are subgames I plan on comparing with other betting sites
def get_focused_subgames_for_sport_id(sport_id):
    all_subgames_dictionary = get_all_subgames().json()
    # Format:
    # all_subgames_dictionary is a map where keys are ordered integers [1..77]
    # and values are lists which contain subgame dictionaries

    offer_list = all_subgames_dictionary[str(sport_id)]
    focused_subgames = []

    for offer in offer_list:
        if offer['name'] != "Konačan ishod":
            continue
        # offer_id = offer['id']
        # print("Offer name ", offer['name'])

        for header in offer['regularHeaders']:
            if len(header['gameName']) != 1:
                print("KONACNO SMO NASLI ODSTUPANJE OD OVE GLUPE STRUKTURE")
                exit(1)
            game = header['gameName'][0]
            # game_id = game['id']
            short_name = game['shortName']
            if short_name != 'ki':
                continue
            for subgame in header['subGameName']:
                subgame_id = subgame['id']
                focused_subgames.append(subgame_id)
                # subgame_name = subgame['name']
                # subgame_desc = subgame['description']
                # print(subgame_id, " - ", subgame_name, " (", subgame_desc, ")")

    return focused_subgames


sidebar_sports = get_curr_sidebar_sports_and_leagues().json()

# Košarka nema kodds?
# Limit yourself to tennis
tennis = get_sport_with_name("Tenis")
if tennis is None:
    print("Send email")
    exit(1)
tennisID = tennis['id']

# Get subgameIds za "Konacan ishod"
subgames = get_focused_subgames_for_sport_id(tennisID)
# print(subgames)


# Get matches and participants
matches_response = get_match_ids(tennisID).json()['matches']
matches = {}
for match in matches_response:
    if match['specialType'] != 0:
        continue

    m = Match(match['id'], match['startTime'])
    for p in match['participants']:
        m.participants.append(Participant(p['id'], p['name']))
    matches[match['id']] = m
    # print(m)


# Get odds for chosen matches and subgames
odds = get_odds(list(matches.keys()), subgames).json()
for o in odds:
    for sg in o['kodds'].values():
        s = Subgame(
            game_name=sg['subGame']['gameName'],
            game_shortname=sg['subGame']['gameShortName'],
            subgame_name=sg['subGame']['subGameName'],
            subgame_description=sg['subGame']['subGameDescription'],
            value=sg['value']
        )
        # print(s)
        matches[o['id']].subgames.append(s)

# # Print results
# for m in matches.values():
#     print(m)

original_stdout = sys.stdout
with open('mozz_tennis.txt', 'w', encoding="utf-8") as f:
    sys.stdout = f
    for m in matches.values():
        print(m)
    sys.stdout = original_stdout
