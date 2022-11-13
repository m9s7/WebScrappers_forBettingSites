import requests as r

from models.common_functions import nice_print_json


# SOCC GetCompetitionFilter
# params: timeFrameOption idk what that is
# # # res:
# [
#     {
# 		"CompetitionId": 8,  id of league that is active
# 		"MatchCount": 14     how many matches are in that league, never 0
# 	},
# ]

def get_curr_sidebar_league_ids():
    url = "https://soccerbet.rs/api/Prematch/GetCompetitionFilter"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers)

    return response.json()


# SOCC GetMasterData
# no params
# # # res:
# {
# CompetitionsData:
# {
#  Sports [{"Id": -2, "Name": "EURO 2016"}] This gives all sports not just active ones
#  Countries [] i dont care
#  Competitions [] all of them not just active
# }
# BetGameOutcomesData:
# {
#  BetGameGroups [{"Id": 80, "Name": "KOMPLETNA PONUDA"}] ali ima vise kompletnih ponuda sa razl. Id-jem tkd zajebi grupe
#  BetGames [
#         {
#             "Id": 701,
#             "Name": "Konačni Ishod",  ali opet ima ih milion i razlikju se samo po ID-ju i BetGameGroupId-ju tkd nista
#             "OrderId": 100,
#             "BetParamName": null,
#             "BetParamShortName": null,
#             "HasHandicapOrTotalBetParam": false,
#             "HasScoreBetParam": false,
#             "HasPeriodBetParam": false,
#             "HasAdditionalBetParam": false,
#             "BetGameGroupId": 19
#         },
#  ]
#  BetGamesBetGameOutcomes [
#         {
#             "Id": 13300,
#             "Name": "1",
#             "Description": "Domaćin pobeđuje na meču", opet ih ima milion wtf
#             "OrderId": 100,
#             "CodeForPrinting": "KI 1",
#             "BetGameId": 3193
#         },
#  ]
# }
# PeriodsData [
#     {
#         "Id": 1,
#         "Name": "Prvih 15 min.", takodje not unique
#         "ShortName": "15",
#         "OrderId": 1
#     },
# ]

# }
def get_master_data():
    url = "https://soccerbet.rs/api/MasterData/GetMasterData"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers)

    return response.json()


# SOCC GetCompetitionMatches
# params: competitionID
# # # res: get a list of these babies
# "Id": 3079381, // aka MatchID
# "HomeCompetitorName": "Milano",
# "AwayCompetitorName": "Virtus",
#       "Code": 1001,
#       "ExternalId": 34868509,
#       "StreamId": null,
# "StartDate": "2022-11-09T20:30:00",
#       "Status": 0,
#       "CompetitionId": 92,
# "SportId": 2, -  am I going to have to use this ??
#       "FavouriteBets": [],
#       "AllBets": null
def get_league_matches_info(league_id):
    url = "https://soccerbet.rs/api/Prematch/GetCompetitionMatches"

    querystring = {"competitionId": str(league_id)}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers, params=querystring)

    return response.json()


# SOCC GetMatchBets
# params: matchId
# # # res: A list of all odds, one odd looks like this
# {
# "Id": 1090167167, This is odd ID, and I need it because there is no odd name here
# "Odds": 1.45,
# "IsEnabled": true,
# "HandicapOrTotalParam": null, Ako je over/under ili je hendikep ovde pise kolka je granica
# "ScoreParam": null,
# "PeriodParam": null,
# "AdditionalParam": null,
# "BetGameOutcomeId": 7000 nznm sta je ovo
# }
def get_match_odd_values(match_id):
    url = "https://soccerbet.rs/api/Prematch/GetMatchBets"

    querystring = {"matchId": str(match_id)}
    headers = {
        "cookie": "ASP.NET_SessionId=kl2d4ouy2rvsbmdhtmni1q3o",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,bs;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://soccerbet.rs/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = r.request("GET", url, headers=headers, params=querystring)

    return response.json()


# need to merge these get_match_odd_values and odd_names from GetMasterData
# and I still didn't find out how to get sport names and ids
# mozda ce morati stvarno da se radi scraping ovde da se dobije sport_name - league_name

# ne ok iz GetMasterData(CompetitionsData -> Sports) imas sport-sport_id - odatle uzimas koji id ti je za sport koji trazis
#       iz GetMasterData(CompetitionsData -> Competitions) dobijes sve moguce lige i filtrirs po sport_id i league_id iz get_curr_sidebar_league_ids
# sad imas sport koji te zanima - lige koje pripadaju tom sportu
# saljes te lige u get_league_matches_info dobijas imena home away i match_ids
# match_ids saljes u get_match_odd_values
# to sad matchujes
#   BetGameOutcomeId sa  GetMasterData -> BetGameOutcomesData -> BetGameGroups -> Id = Name:"ISHOD MEČA" ili sta god
# ali to cemo sutra

# nice_print_json(get_curr_sidebar_league_ids())

