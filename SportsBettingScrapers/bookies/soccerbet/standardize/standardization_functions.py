import calendar
import time

from common.models import SoccbetNames


def standardize_kickoff_time_string(start_date_socc_string):
    return calendar.timegm(time.strptime(start_date_socc_string, '%Y-%m-%dT%H:%M:%S'))


def standardize_basketball_tip_name(tip_name):
    if tip_name is None:
        return None

    if tip_name == 'KI 1':
        return 'KI_1_w/OT'
    if tip_name == 'KI 2':
        return 'KI_2_w/OT'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_tennis_tip_name(tip_name):
    if tip_name is None:
        return None

    # MATCH OUTCOME
    if tip_name == 'KI 1':
        return 'KI_1'
    if tip_name == 'KI 2':
        return 'KI_2'

    # FIRST SET OUTCOME
    if tip_name == 'Iset 1':
        return 'FST_SET_1'
    if tip_name == 'Iset 2':
        return 'FST_SET_2'

    # TIE BREAK IN MATCH
    if tip_name == 'TB DA':
        return 'TIE_BREAK_YES'
    if tip_name == 'TB NE':
        return 'TIE_BREAK_NO'

    # Soccbet doesn't offer these tips:

    # # SECOND SET OUTCOME
    # if tip_name == '2s 1':
    #     return 'SND_SET_1'
    # if tip_name == '2s 2':
    #     return 'SND_SET_2'

    # # TIE BREAK FIRST SET
    # if tip_name == 'ug1s da 13':
    #     return 'TIE_BREAK_FST_SET_YES'
    # if tip_name == 'ug1s ne 13':
    #     return 'TIE_BREAK_FST_SET_NO'

    # # TIE BREAK SECOND SET
    # if tip_name == 'ug2s da 13':
    #     return 'TIE_BREAK_SND_SET_YES'
    # if tip_name == 'ug2s ne 13':
    #     return 'TIE_BREAK_SND_SET_NO'

    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_table_tennis_tip_name(tip_name):
    if tip_name == 'KI 1':
        return 'KI_1'
    if tip_name == 'KI 2':
        return 'KI_2'
    # nemaju:
    # if tip_name == 'S1_1':
    #     return 'FST_SET_1'
    # if tip_name == 'S1_2':
    #     return 'FST_SET_2'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_soccer_tip_name(tip_name):
    if tip_name is None:
        return None

    tip = tip_name.strip()
    tip_len = len(tip)

    # # UKUPNO GOLOVA
    if tip.startswith('UG '):
        # ug 0-x
        if tip.startswith('UG 0-') and tip_len == 6:
            return 'UG_0-' + tip[5]
        # ug x+
        if tip.startswith('UG ') and tip.endswith('+') and tip_len == 5:
            return 'UG_' + tip[3] + '+'

    # # UKUPNO GOLOVA PRVO POLUVREME
    if tip.startswith('UG I'):
        # 1ug 0-x
        if tip.startswith('UG I0-') and tip_len == 7:
            return 'UG_1P_0-' + tip[6]
        # 1ug x+
        if tip.startswith('UG I') and tip.endswith('+') and tip_len == 6:
            return 'UG_1P_' + tip[4] + '+'
        # 1ug 0
        if tip == 'UG I0':
            return 'UG_1P_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME
    if tip.startswith('UG II'):
        # 2ug 0-x
        if tip.startswith('UG II0-') and tip_len == 8:
            return 'UG_2P_0-' + tip[7]
        # 2ug x+
        if tip.startswith('UG II') and tip.endswith('+') and tip_len == 7:
            return 'UG_2P_' + tip[5] + '+'
        # 2ug 0
        if tip == 'UG II0':
            return 'UG_2P_T0'

    # # UKUPNO GOLOVA DOMACIN (TIM1)
    if tip.startswith('D '):
        # tm1 0-x
        if tip.startswith('D 0-') and tip_len == 5:
            return 'UG_TIM1_0-' + tip[4]
        # tm1 x+
        if tip.startswith('D ') and tip.endswith('+') and tip_len == 4:
            return 'UG_TIM1_' + tip[2] + '+'
        # tm1 0
        if tip == 'D 0':
            return 'UG_TIM1_T0'

    # # UKUPNO GOLOVA PRVO POLUVREME DOMACIN (TIM1)
    if tip.startswith('D I'):
        # 1tm1 0-x
        if tip.startswith('D I0-') and tip_len == 6:
            return 'UG_1P_TIM1_0-' + tip[5]
        # 1tm1 x+
        if tip.startswith('D I') and tip.endswith('+') and tip_len == 5:
            return 'UG_1P_TIM1_' + tip[3] + '+'
        # 1tm1 0
        if tip == 'D I0':
            return 'UG_1P_TIM1_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME DOMACIN (TIM1)
    if tip.startswith('D II'):
        # 2tm1 0-x
        if tip.startswith('D II0-') and tip_len == 7:
            return 'UG_2P_TIM1_0-' + tip[6]
        # 2tm1 x+
        if tip.startswith('D II') and tip.endswith('+') and tip_len == 6:
            return 'UG_2P_TIM1_' + tip[4] + '+'
        # 2tm1 0
        if tip == 'D II0':
            return 'UG_2P_TIM1_T0'

    # # UKUPNO GOLOVA GOST (TIM2)
    if tip.startswith('G '):
        # tm2 0-x
        if tip.startswith('G 0-') and tip_len == 5:
            return 'UG_TIM2_0-' + tip[4]
        # tm2 x+
        if tip.startswith('G ') and tip.endswith('+') and tip_len == 4:
            return 'UG_TIM2_' + tip[2] + '+'
        # tm2 0
        if tip == 'G 0':
            return 'UG_TIM2_T0'

    # # UKUPNO GOLOVA PRVO POLUVREME GOST (TIM2)
    if tip.startswith('G I'):
        # 1tm2 0-x
        if tip.startswith('G I0-') and tip_len == 6:
            return 'UG_1P_TIM2_0-' + tip[5]
        # 1tm2 x+
        if tip.startswith('G I') and tip.endswith('+') and tip_len == 5:
            return 'UG_1P_TIM2_' + tip[3] + '+'
        # 1tm2 0
        if tip == 'G I0':
            return 'UG_1P_TIM2_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME GOST (TIM2)
    if tip.startswith('G II'):
        # 2tm2 0-x
        if tip.startswith('G II0-') and tip_len == 7:
            return 'UG_2P_TIM2_0-' + tip[6]
        # 2tm2 x+
        if tip.startswith('G II') and tip.endswith('+') and tip_len == 6:
            return 'UG_2P_TIM2_' + tip[4] + '+'
        # 2tm2 0
        if tip == 'G II0':
            return 'UG_2P_TIM2_T0'

    raise ValueError(f'Unexpected tip_name: |{tip_name}|')


def get_standardization_func_4_tip_names(sport):
    if sport == SoccbetNames.tennis:
        return standardize_tennis_tip_name
    if sport == SoccbetNames.tabletennis:
        return standardize_table_tennis_tip_name
    # if sport == SoccbetNames.esports:
    #     return standardize_esports_tip_name
    if sport == SoccbetNames.basketball:
        return standardize_basketball_tip_name
    if sport == SoccbetNames.soccer:
        return standardize_soccer_tip_name
    raise TypeError('No tip name standardization function for sport enum: ', sport)
