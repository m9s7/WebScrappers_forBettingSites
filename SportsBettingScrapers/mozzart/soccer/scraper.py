import pandas as pd

from models.common_functions import print_to_file
from requests_to_server.mozzart_requests import get_odds, get_match_ids


def ug_condition_satisfied(subgame):
    return subgame.startswith('0-') or subgame.startswith('1-') or subgame.endswith("+") or subgame == "0"


def get_game_name(header):
    if len(header['gameName']) != 1:
        print("FINALLY FOUND AN INCONSISTENCY IN MOZZART DATA STRUCTURE")
        exit(1)
    return header['gameName'][0]['name']


def get_focused_soccer_subgames(offers):
    focused_subgames = set()

    for offer in offers:

        # ug
        if offer['name'] == "Ukupno golova na meču":
            for header in offer['regularHeaders']:
                game = get_game_name(header)

                if game == "Ukupno golova na meču":
                    for subgame in header['subGameName']:
                        if ug_condition_satisfied(subgame['name']):
                            focused_subgames.add(subgame['id'])

                if game == "Tačan broj golova na meču":
                    [focused_subgames.add(subgame['id']) for subgame in header['subGameName'] if subgame['name'] == '0']

        # ug tim 1, ug tim 2
        if offer['name'] == "Oba tima daju gol":
            for header in offer['regularHeaders']:
                game = get_game_name(header)
                if game in ["Tim 1 daje gol", "Tim 2 daje gol"]:
                    for subgame in header['subGameName']:
                        if ug_condition_satisfied(subgame['name']):
                            focused_subgames.add(subgame['id'])

        # ug1p, ug1p tim 1, ug1p tim 2
        if offer['name'] == "Prvo poluvreme":
            for header in offer['regularHeaders']:
                game = get_game_name(header)

                if game == "Tačan broj golova prvo poluvreme":
                    [focused_subgames.add(subgame['id']) for subgame in header['subGameName'] if subgame['name'] == '0']

                if game in ["Ukupno golova prvo poluvreme", "Tim 1 golovi prvo poluvreme",
                            "Tim 2 golovi prvo poluvreme"]:
                    for subgame in header['subGameName']:
                        if ug_condition_satisfied(subgame['name']):
                            focused_subgames.add(subgame['id'])

        # ug2p, ug2p tim 1, ug2p tim 2
        if offer['name'] == "Drugo poluvreme":
            for header in offer['regularHeaders']:
                game = get_game_name(header)

                if game == "Tačan broj golova drugo poluvreme":
                    [focused_subgames.add(subgame['id']) for subgame in header['subGameName'] if subgame['name'] == '0']

                if game in ["Ukupno golova drugo poluvreme", "Tim 1 golovi drugo poluvreme",
                            "Tim 2 golovi drugo poluvreme"]:
                    for subgame in header['subGameName']:
                        if ug_condition_satisfied(subgame['name']):
                            focused_subgames.add(subgame['id'])

    return list(focused_subgames)


def init_export_help(matches_response):
    export_help = {}
    for match in matches_response:
        if match['specialType'] != 0 or len(match['participants']) != 2:
            continue
        e = [match['participants'][0]['name'], match['participants'][1]['name']]
        export_help[match['id']] = e

    return export_help


def scrape_soccer(soccer_id, all_subgames_json):

    subgames = get_focused_soccer_subgames(all_subgames_json[str(soccer_id)])
    matches_response = get_match_ids(soccer_id).json()['matches']

    export_help = init_export_help(matches_response)
    export = []

    # For testing with Insomnia
    # print(soccer_id)
    # print(list(export.keys())[1:10], " - ", subgames)

    odds = get_odds(list(export_help.keys()), subgames).json()
    for o in odds:
        if "kodds" not in o:
            continue

        match_id = o['id']
        tip1 = {}
        tip2 = {}
        for sg in o['kodds'].values():
            if sg is None:
                continue

            if "subGame" not in sg:
                raise KeyError("kodds instance doesn't have subgame field ??")

            # Konačan ishod
            game = sg['subGame']['gameShortName']
            subgame = sg['subGame']['subGameName']
            # print(game, subgame)

            interested_subgames = ['1tm2', '1tm1', '2tm2', '1ug', 'ug', '2ug', 'tm1', '2tm1', 'tm2']
            if game in interested_subgames:
                if subgame.startswith('0-') or subgame == '0':
                    tip1[(game, subgame)] = sg['value']
                if subgame.startswith('1-') or subgame.endswith('+'):
                    tip2[(game, subgame)] = sg['value']

        for t1_game, t1_subgame in tip1:
            if t1_subgame == '0':
                for t2_game, t2_subgame in tip2:
                    if t2_game == t1_game and t2_subgame == '1+':
                        e = export_help[match_id] + [" ".join([t1_game, t1_subgame]), tip1[t1_game, t1_subgame],
                                                     " ".join([t2_game, t2_subgame]), tip2[t2_game, t2_subgame]]
                        # print(e)
                        export.append(e)
            if t1_subgame.startswith('0-') and len(t1_subgame) == 3:
                x = int(t1_subgame[2])
                for t2_game, t2_subgame in tip2:
                    if t2_game == t1_game and t2_subgame == f'{x + 1}+':
                        e = export_help[match_id] + [" ".join([t1_game, t1_subgame]), tip1[t1_game, t1_subgame],
                                                     " ".join([t2_game, t2_subgame]), tip2[t2_game, t2_subgame]]
                        # print(e)
                        export.append(e)
    df = pd.DataFrame(export, columns=['1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val'])
    print_to_file(df.to_string(), f"mozz_soccer.txt")

    return df
