from requests_to_server.soccerbet_requests import get_curr_sidebar_league_ids


def parse_get_curr_sidebar_league_ids(response):
    league_ids = []
    for r in response:
        league_ids.append(r['CompetitionId'])
    return league_ids


def parse_get_league_matches_info(response):
    matches = []
    for match in response:
        matches.append({
            'match_id': match['Id'],
            'home': match['HomeCompetitorName'],
            'away': match['AwayCompetitorName'],
            'kickoff': match['StartDate']
        })
    return matches


def create_sidebar(master_data, sport_dict):
    response = get_curr_sidebar_league_ids()
    while response is None:
        print("Stuck on soccerbet, get_curr_sidebar_league_ids()")
        response = get_curr_sidebar_league_ids()

    league_ids = parse_get_curr_sidebar_league_ids(response)

    sidebar = {}
    for league in master_data['CompetitionsData']['Competitions']:
        if league['Id'] in league_ids:
            sport_name = sport_dict[league['SportId']]
            if sport_name not in sidebar:
                sidebar[sport_name] = []
            sidebar[sport_name].append(league)

    return sidebar


def get_sport_dict(master_data):
    result = {}
    for sport in master_data['CompetitionsData']['Sports']:
        result[sport['Id']] = sport['Name']
    return result


def get_betgame_dict(master_data):
    result = {}
    for bet_game in master_data['BetGameOutcomesData']['BetGames']:
        result[bet_game['Id']] = bet_game
    return result


def get_betgame_outcome_dict(master_data):
    result = {}
    for bet_game_outcome in master_data['BetGameOutcomesData']['BetGameOutcomes']:
        result[bet_game_outcome['Id']] = bet_game_outcome
    return result


def get_betgame_groups_dict(master_data):
    result = {}
    for bet_game_group in master_data['BetGameOutcomesData']['BetGameGroups']:
        result[bet_game_group['Id']] = bet_game_group
    return result
