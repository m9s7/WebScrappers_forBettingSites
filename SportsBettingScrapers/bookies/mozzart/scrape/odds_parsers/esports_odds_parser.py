import pandas as pd

from common.models import scraper_columns
from bookies.mozzart.scrape.helper_functions import init_export_help, get_subgame_ids
from requests_to_server.mozzart_requests import get_odds, get_match_ids


def scrape_esports(esports_id, all_subgames_json):
    print("...scraping mozz - esports")

    subgames = get_subgame_ids(all_subgames_json[str(esports_id)], ['ki'])
    matches_response = get_match_ids(esports_id)['matches']
    while matches_response is None:
        print("Stuck on MOZZ betOffer2")
        matches_response = get_match_ids(esports_id)['matches']

    export = []
    export_help = init_export_help(matches_response)

    # TODO: make debugging mode
    # For testing with Insomnia
    # print(tennis_id)
    # print(list(export_help.keys())[1:10], " - ", subgames)

    odds = get_odds(list(export_help.keys()), subgames)
    for o in odds:
        if "kodds" not in o:
            continue

        match_id = o['id']
        print(f"\r{match_id}", end='')
        
        e1 = export_help[match_id]
        export_match_helper = {}

        for sg in o['kodds'].values():
            if sg is None:
                continue
            if "subGame" not in sg:
                raise KeyError("kodds instance doesn't have subgame field ??")

            game = sg['subGame']['gameShortName']
            subgame = sg['subGame']['subGameName']
            val = sg['value']

            if game == 'ki':

                if game not in export_match_helper:
                    export_match_helper[game] = [None, None, None, None]

                if subgame == '1':
                    # noinspection PyTypeChecker
                    export_match_helper[game][0] = ' '.join([game, subgame])
                    export_match_helper[game][1] = val
                elif subgame == '2':
                    # noinspection PyTypeChecker
                    export_match_helper[game][2] = ' '.join([game, subgame])
                    export_match_helper[game][3] = val
                else:
                    raise AttributeError(
                        f"Mozzart: Two-outcome game with third outcome {game} {subgame} found, value={val}")

        for e2 in export_match_helper.values():
            e = e1 + e2
            export.append(e)

    df = pd.DataFrame(export, columns=scraper_columns)

    print("Matches scraped: ", len(list(export_help.keys())))
    return df
