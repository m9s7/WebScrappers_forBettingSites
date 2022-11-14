from common.common_functions import eprint


def raise_not_2_outcome_game_error(game, outcome_name, outcome_desc, outcome_code, value):
    eprint(game, ' - ', outcome_desc)
    eprint(outcome_name, ' - ', outcome_code)
    eprint(f"value={value}")
    raise AttributeError("Mozzart: Two-outcome game with third outcome\n")