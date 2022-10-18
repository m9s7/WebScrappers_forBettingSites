import pandas as pd

from models.common_functions import print_to_file
from models.match_model import MozzNames, ExportIDX
from mozzart.helper_functions import init_export_with_matches
from mozzart.subgames_parsers.two_outcome_ki_subgame_parser import get_2_outcome_subgames
from requests_to_server.mozzart_requests import get_match_ids, get_odds


def scrape_basketball(basketball_id, all_subgames_json):
    print("...scraping mozz - basketball")

    subgames = get_2_outcome_subgames(all_subgames_json[str(basketball_id)], MozzNames.basketball)
    matches_response = get_match_ids(basketball_id).json()['matches']
    export = init_export_with_matches(matches_response)

    # For testing with Insomnia
    # print(esports_id)
    # print(list(export.keys())[1:10], " - ", subgames)

    odds = get_odds(list(export.keys()), subgames).json()
    for o in odds:
        if "kodds" not in o:
            continue

        match_id = o['id']
        for sg in o['kodds'].values():
            if sg is None:
                continue

            if "subGame" not in sg:
                raise KeyError("kodds instance doesn't have subgame field ??")

            # Konačan ishod
            game = sg['subGame']['gameShortName']
            subgame = sg['subGame']['subGameName']
            val = sg['value']

            if game == 'pobm':
                if subgame == '1':
                    export[match_id][ExportIDX.TIP1_NAME] = ' '.join([game, subgame])
                    export[match_id][ExportIDX.TIP1_VAL] = val
                elif subgame == '2':
                    export[match_id][ExportIDX.TIP2_NAME] = ' '.join([game, subgame])
                    export[match_id][ExportIDX.TIP2_VAL] = val
                else:
                    raise AttributeError(
                        f"Mozzart: Two-outcome game with third outcome {game} {subgame} found, value={val}")

    df = pd.DataFrame(list(export.values()), columns=['1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val'])
    print_to_file(df.to_string(), f"mozz_basketball.txt")

    return df
