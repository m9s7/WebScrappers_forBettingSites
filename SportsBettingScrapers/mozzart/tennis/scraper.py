import pandas as pd

from models.common_functions import print_to_file
from models.match_model import Subgames, MozzNames
from mozzart.helper_functions import init_export_with_matches
from mozzart.subgames_parsers.two_outcome_ki_subgame_parser import get_2_outcome_subgames
from requests_to_server.mozzart_requests import get_odds, get_match_ids


def scrape_tennis(tennis_id, all_subgames_json):
    print("...scraping mozz - tennis")

    # TODO: program breaks if that sport is not there
    subgames = get_2_outcome_subgames(all_subgames_json[str(tennis_id)], MozzNames.tennis)

    matches_response = get_match_ids(tennis_id).json()['matches']

    export = init_export_with_matches(matches_response)

    # TODO: make debugging mode
    # For testing with Insomnia
    # print(tennis_id)
    # print(list(export.keys())[1:10], " - ", subgames)

    odds = get_odds(list(export.keys()), subgames).json()
    for o in odds:
        if "kodds" not in o:
            continue

        match_id = o['id']
        for sg in o['kodds'].values():
            if sg is None:
                continue

            # TODO: Should have try catch blocks to raise exceptions and not break the program
            if "subGame" not in sg:
                raise KeyError("kodds instance doesn't have subgame field ??")

            # Konačan ishod
            if sg['subGame']['gameShortName'] == 'ki':
                if sg['subGame']['subGameName'] == '1':
                    export[match_id][Subgames.KI_1] = sg['value']
                elif sg['subGame']['subGameName'] == '2':
                    export[match_id][Subgames.KI_2] = sg['value']
                else:
                    # TODO: continue working but log it and notify me
                    raise AttributeError(
                        f"Mozzart: Two-outcome game with third outcome {sg['subGame']['subGameName']} found, value={sg['value']}")

    df = pd.DataFrame(list(export.values()), columns=['1', '2', 'KI_1', 'KI_2'])
    print_to_file(df.to_string(), f"mozz_tennis.txt")

    return df
