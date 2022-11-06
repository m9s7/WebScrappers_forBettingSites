import pandas as pd

from models.match_model import scraper_columns, ExportIDX
from mozzart.scrape.helper_functions import init_export_help, get_subgame_ids
from mozzart.standardize.standardization_functions import standardize_basketball_tip_name
from requests_to_server.mozzart_requests import get_odds, get_match_ids


def scrape_basketball(basketball_id, all_subgames_json):
    print("...scraping mozz - basketball")

    subgames = get_subgame_ids(all_subgames_json[str(basketball_id)], ['pobm'])
    matches_response = get_match_ids(basketball_id)['matches']

    export = []
    export_help = init_export_help(matches_response)

    # TODO: make debugging mode
    # For testing with Insomnia
    # print(basketball_id)
    # print(list(export_help.keys())[1:10], " - ", subgames)

    odds = get_odds(list(export_help.keys()), subgames)
    for o in odds:
        if "kodds" not in o:
            continue

        match_id = o['id']
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

            if game == 'pobm':

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

    # Standardize tip names
    col_name = df.columns[ExportIDX.TIP1_NAME]
    df[col_name] = df[col_name].map(standardize_basketball_tip_name)
    col_name = df.columns[ExportIDX.TIP2_NAME]
    df[col_name] = df[col_name].map(standardize_basketball_tip_name)

    print("Matches scraped: ", len(list(export_help.keys())))
    return df
