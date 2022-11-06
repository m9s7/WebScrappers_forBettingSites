import pandas as pd

from models.match_model import scraper_columns, ExportIDX
from mozzart.scrape.helper_functions import get_subgame_ids, init_export_help
from mozzart.standardize.standardization_functions import standardize_tennis_tip_name
from requests_to_server.mozzart_requests import get_odds, get_match_ids


def scrape_tennis(tennis_id, all_subgames_json):
    print("...scraping mozz - tennis")

    subgames = get_subgame_ids(all_subgames_json[str(tennis_id)], ['ki', '1s', 'ug1s', 'ug2s', 'tb'])
    matches_response = get_match_ids(tennis_id)['matches']

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

            if game in ['ki', '1s']:

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

            if game in ['ug1s', 'ug2s', 'tb']:

                if game not in export_match_helper:
                    export_match_helper[game] = [None, None, None, None]

                if subgame == 'da 13' or subgame == 'da':
                    # noinspection PyTypeChecker
                    export_match_helper[game][0] = ' '.join([game, subgame])
                    export_match_helper[game][1] = val
                elif subgame == 'ne 13' or subgame == 'ne':
                    # noinspection PyTypeChecker
                    export_match_helper[game][2] = ' '.join([game, subgame])
                    export_match_helper[game][3] = val
                else:
                    continue

        for e2 in export_match_helper.values():
            e = e1 + e2
            export.append(e)

    df = pd.DataFrame(export, columns=scraper_columns)

    # Standardize tip names
    col_name = df.columns[ExportIDX.TIP1_NAME]
    df[col_name] = df[col_name].map(standardize_tennis_tip_name)
    col_name = df.columns[ExportIDX.TIP2_NAME]
    df[col_name] = df[col_name].map(standardize_tennis_tip_name)

    print("Matches scraped: ", len(list(export_help.keys())))
    return df
