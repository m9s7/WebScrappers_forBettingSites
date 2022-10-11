import pandas as pd

from models.match_model import Subgames
from requests_to_server.maxbet_requests import get_match_data


def parse_basketball_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:

            match_info = get_match_data(match['id']).json()
            e = [match['home'], match['away'], None, None]
            for subgame in match_info['odBetPickGroups']:
                if subgame['name'] != "Konačan ishod sa produžecima":
                    continue
                e[Subgames.FT_OT_1] = subgame['tipTypes'][0]['value']
                e[Subgames.FT_OT_2] = subgame['tipTypes'][1]['value']

            export[match['id']] = e

    columns = ['1', '2', 'KI_1', 'KI_2']
    df = pd.DataFrame(list(export.values()), columns=columns)
    return df
