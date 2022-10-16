# Focused subgames are subgames I plan on comparing with other betting sites
from models.match_model import MozzNames


def get_2_outcome_subgames(offers, sport_name):
    focused_subgames = []

    for offer in offers:
        # Maybe switch to 'Kompletna ponuda' because there is everything there but idk
        if offer['name'] != "Konačan ishod":
            continue

        for header in offer['regularHeaders']:
            if len(header['gameName']) != 1:
                print("FINALLY FOUND AN INCONSISTENCY IN MOZZART DATA STRUCTURE")
                exit(1)
            game = header['gameName'][0]
            short_name = game['shortName']

            if sport_name == MozzNames.tennis or sport_name == MozzNames.esports:
                if short_name != 'ki':
                    continue
                for subgame in header['subGameName']:
                    focused_subgames.append(subgame['id'])

            if sport_name == MozzNames.basketball:
                if short_name != 'pobm':
                    continue
                for subgame in header['subGameName']:
                    focused_subgames.append(subgame['id'])

    return focused_subgames
