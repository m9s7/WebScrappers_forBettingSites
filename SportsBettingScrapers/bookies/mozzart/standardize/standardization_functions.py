from common.models import MozzNames


def standardize_basketball_tip_name(tip_name):
    if tip_name is None:
        return None

    if tip_name == 'pobm 1':
        return 'KI_1_w/OT'
    if tip_name == 'pobm 2':
        return 'KI_2_w/OT'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_esports_tip_name(tip_name):
    if tip_name is None:
        return None

    # MATCH OUTCOME
    if tip_name == 'ki 1':
        return 'KI_1'
    if tip_name == 'ki 2':
        return 'KI_2'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_tennis_tip_name(tip_name):
    if tip_name is None:
        return None

    # MATCH OUTCOME
    if tip_name == 'ki 1':
        return 'KI_1'
    if tip_name == 'ki 2':
        return 'KI_2'

    # FIRST SET OUTCOME
    if tip_name == '1s 1':
        return 'FST_SET_1'
    if tip_name == '1s 2':
        return 'FST_SET_2'

    # SECOND SET OUTCOME
    if tip_name == '2s 1':
        return 'SND_SET_1'
    if tip_name == '2s 2':
        return 'SND_SET_2'

    # TIE BREAK FIRST SET
    if tip_name == 'ug1s da 13':
        return 'TIE_BREAK_FST_SET_YES'
    if tip_name == 'ug1s ne 13':
        return 'TIE_BREAK_FST_SET_NO'

    # TIE BREAK SECOND SET
    if tip_name == 'ug2s da 13':
        return 'TIE_BREAK_SND_SET_YES'
    if tip_name == 'ug2s ne 13':
        return 'TIE_BREAK_SND_SET_NO'

    # TIE BREAK IN MATCH
    if tip_name == 'tb da':
        return 'TIE_BREAK_YES'
    if tip_name == 'tb ne':
        return 'TIE_BREAK_NO'

    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_soccer_tip_name(tip_name):
    if tip_name is None:
        return None

    tip = tip_name.strip()
    tip_len = len(tip)

    # # UKUPNO GOLOVA
    if tip.startswith('ug '):
        # ug 0-x
        if tip.startswith('ug 0-') and tip_len == 6:
            return 'UG_0-' + tip[5]
        # ug x+
        if tip.startswith('ug ') and tip.endswith('+') and tip_len == 5:
            return f"UG_{tip[3]}+"

    # # UKUPNO GOLOVA PRVO POLUVREME
    if tip.startswith('1ug '):
        # 1ug 0-x
        if tip.startswith('1ug 0-') and tip_len == 7:
            return 'UG_1P_0-' + tip[6]
        # 1ug x+
        if tip.startswith('1ug ') and tip.endswith('+') and tip_len == 6:
            return f"UG_1P_{tip[4]}+"
        # 1ug 0
        if tip == '1ug 0':
            return 'UG_1P_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME
    if tip.startswith('2ug '):
        # 2ug 0-x
        if tip.startswith('2ug 0-') and tip_len == 7:
            return 'UG_2P_0-' + tip[6]
        # 2ug x+
        if tip.startswith('2ug ') and tip.endswith('+') and tip_len == 6:
            return f"UG_2P_{tip[4]}+"
        # 2ug 0
        if tip == '2ug 0':
            return 'UG_2P_T0'

    # # UKUPNO GOLOVA DOMACIN (TIM1)
    if tip.startswith('tm1 '):
        # tm1 0-x
        if tip.startswith('tm1 0-') and tip_len == 7:
            return 'UG_TIM1_0-' + tip[6]
        # tm1 x+
        if tip.startswith('tm1 ') and tip.endswith('+') and tip_len == 6:
            return f"UG_TIM1_{tip[4]}+"
        # tm1 0
        if tip == 'tm1 0':
            return 'UG_TIM1_T0'

    # # UKUPNO GOLOVA PRVO POLUVREME DOMACIN (TIM1)
    if tip.startswith('1tm1 '):
        # 1tm1 0-x
        if tip.startswith('1tm1 0-') and tip_len == 8:
            return 'UG_1P_TIM1_0-' + tip[7]
        # 1tm1 x+
        if tip.startswith('1tm1 ') and tip.endswith('+') and tip_len == 7:
            return f"UG_1P_TIM1_{tip[5]}+"
        # 1tm1 0
        if tip == '1tm1 0':
            return 'UG_1P_TIM1_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME DOMACIN (TIM1)
    if tip.startswith('2tm1 '):
        # 2tm1 0-x
        if tip.startswith('2tm1 0-') and tip_len == 8:
            return 'UG_2P_TIM1_0-' + tip[7]
        # 2tm1 x+
        if tip.startswith('2tm1 ') and tip.endswith('+') and tip_len == 7:
            return f"UG_2P_TIM1_{tip[5]}+"
        # 2tm1 0
        if tip == '2tm1 0':
            return 'UG_2P_TIM1_T0'

    # # UKUPNO GOLOVA GOST (TIM2)
    if tip.startswith('tm2 '):
        # tm2 0-x
        if tip.startswith('tm2 0-') and tip_len == 7:
            return 'UG_TIM2_0-' + tip[6]
        # tm2 x+
        if tip.startswith('tm2 ') and tip.endswith('+') and tip_len == 6:
            return f"UG_TIM2_{tip[4]}+"
        # tm1 0
        if tip == 'tm2 0':
            return 'UG_TIM2_T0'

    # # UKUPNO GOLOVA PRVO POLUVREME DOMACIN (TIM1)
    if tip.startswith('1tm2 '):
        # 1tm2 0-x
        if tip.startswith('1tm2 0-') and tip_len == 8:
            return 'UG_1P_TIM2_0-' + tip[7]
        # 1tm2 x+
        if tip.startswith('1tm2 ') and tip.endswith('+') and tip_len == 7:
            return f"UG_1P_TIM2_{tip[5]}+"
        # 1tm2 0
        if tip == '1tm2 0':
            return 'UG_1P_TIM2_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME DOMACIN (TIM1)
    if tip.startswith('2tm2 '):
        # 2tm2 0-x
        if tip.startswith('2tm2 0-') and tip_len == 8:
            return 'UG_2P_TIM2_0-' + tip[7]
        # 2tm2 x+
        if tip.startswith('2tm2 ') and tip.endswith('+') and tip_len == 7:
            return f"UG_2P_TIM2_{tip[5]}+"
        # 2tm2 0
        if tip == '2tm2 0':
            return 'UG_2P_TIM2_T0'

    raise ValueError(f'Unexpected tip_name: |{tip_name}|')


def standardize_tabletennis_tip_name(tip_name):
    if tip_name == 'ki 1':
        return 'KI_1'
    if tip_name == 'ki 2':
        return 'KI_2'
    # nemaju:
    # if tip_name == 'S1_1':
    #     return 'FST_SET_1'
    # if tip_name == 'S1_2':
    #     return 'FST_SET_2'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_kickoff_time_string(kickoff_time):
    return kickoff_time // 1000


def get_standardization_func_4_tip_names(sport):
    if sport == MozzNames.tennis:
        return standardize_tennis_tip_name
    if sport == MozzNames.esports:
        return standardize_esports_tip_name
    if sport == MozzNames.basketball:
        return standardize_basketball_tip_name
    if sport == MozzNames.soccer:
        return standardize_soccer_tip_name
    if sport == MozzNames.tabletennis:
        return standardize_tabletennis_tip_name
    raise TypeError('No tip name standardization function for sport enum: ', sport)
