def standardize_basketball_tip_name(tip_name):
    if tip_name == 'FT_OT_1':
        return 'KI_1_w/OT'
    if tip_name == 'FT_OT_2':
        return 'KI_2_w/OT'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_esports_tip_name(tip_name):
    if tip_name in ['KI_1', 'KI_2']:
        return tip_name
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_tennis_tip_name(tip_name):
    if tip_name in ['KI_1', 'KI_2', 'TIE_BREAK_YES', 'TIE_BREAK_NO']:
        return tip_name
    if tip_name == 'S1_1':
        return 'FST_SET_1'
    if tip_name == 'S1_2':
        return 'FST_SET_2'
    if tip_name == 'S2_1':
        return 'SND_SET_1'
    if tip_name == 'S2_2':
        return 'SND_SET_2'
    if tip_name == 'TIE_BREAK_S1_YES':
        return 'TIE_BREAK_FST_SET_YES'
    if tip_name == 'TIE_BREAK_S1_NO':
        return 'TIE_BREAK_FST_SET_NO'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_table_tennis_tip_name(tip_name):
    if tip_name in ['KI_1', 'KI_2']:
        return tip_name
    if tip_name == 'S1_1':
        return 'FST_SET_1'
    if tip_name == 'S1_2':
        return 'FST_SET_2'
    raise ValueError(f'Unexpected tip_name: {tip_name}')


def standardize_soccer_tip_name(tip_name):
    tip = tip_name.strip()
    tip_len = len(tip)

    # # UKUPNO GOLOVA
    if tip.startswith('ug '):
        # ug 0-x
        if tip.startswith('ug 0-') and tip_len == 6:
            return tip.upper()
        # ug x+
        if tip.startswith('ug ') and tip.endswith('+') and tip_len == 5:
            return tip.upper()

    # # UKUPNO GOLOVA PRVO POLUVREME
    if tip.startswith('ug 1P'):
        # ug 1P0-x
        if tip.startswith('ug 1P0-') and tip_len == 8:
            return 'UG_1P_0-' + tip[7]
        # ug 1Px+
        if tip.startswith('ug 1P') and tip.endswith('+') and tip_len == 7:
            return 'UG_1P_' + tip[5] + '+'
        # ug 1PT0
        if tip == 'ug 1PT0':
            return 'UG_1P_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME
    if tip.startswith('ug 2P'):
        # ug 2P0-x
        if tip.startswith('ug 2P0-') and tip_len == 8:
            return 'UG_2P_0-' + tip[6]
        # ug 1Px+
        if tip.startswith('ug 2P') and tip.endswith('+') and tip_len == 7:
            return 'UG_2P_' + tip[5] + '+'
        # ug 1PT0
        if tip == 'ug 2PT0':
            return 'UG_2P_T0'

    # # UKUPNO GOLOVA DOMACIN (TIM1)
    if tip.startswith('D'):
        # D0-x
        if tip.startswith('D0-') and tip_len == 4:
            return 'UG_TIM1_0-' + tip[3]
        # Dx+
        if tip.startswith('D') and tip.endswith('+') and tip_len == 3:
            return 'UG_TIM1_' + tip[1] + '+'
        if tip == 'D0':
            return 'UG_TIM1_T0'

    # # UKUPNO GOLOVA PRVO POLUVREME DOMACIN (TIM1)
    if tip.startswith('1D'):
        # 1D0-x
        if tip.startswith('1D0-') and tip_len == 5:
            return 'UG_1P_TIM1_0-' + tip[4]
        # 1D2+
        if tip.startswith('1D') and tip.endswith('+') and tip_len == 4:
            return 'UG_1P_TIM1_' + tip[2] + '+'
        # 1D0
        if tip == '1D0':
            return 'UG_1P_TIM1_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME DOMACIN (TIM1)
    if tip.startswith('2D'):
        # 2D0-x
        if tip.startswith('2D0-') and tip_len == 5:
            return 'UG_2P_TIM1_0-' + tip[4]
        # 2D2+
        if tip.startswith('2D') and tip.endswith('+') and tip_len == 4:
            return 'UG_2P_TIM1_' + tip[2] + '+'
        # 2D0
        if tip == '2D0':
            return 'UG_2P_TIM1_T0'

    # # UKUPNO GOLOVA GOST (TIM2)
    if tip.startswith('G'):
        # G0-x
        if tip.startswith('G0-') and tip_len == 4:
            return 'UG_TIM2_0-' + tip[3]
        # Gx+
        if tip.startswith('G') and tip.endswith('+') and tip_len == 3:
            return 'UG_TIM2_' + tip[1] + '+'
        # G0
        if tip == 'G0':
            return 'UG_TIM2_T0'

    # # UKUPNO GOLOVA PRVO POLUVREME GOST (TIM2)
    if tip.startswith('1G'):
        # 1G0-x
        if tip.startswith('1G0-') and tip_len == 5:
            return 'UG_1P_TIM2_0-' + tip[4]
        # 1G2+
        if tip.startswith('1G') and tip.endswith('+') and tip_len == 4:
            return 'UG_1P_TIM2_' + tip[2] + '+'
        # 1G0
        if tip == '1G0':
            return 'UG_1P_TIM2_T0'

    # # UKUPNO GOLOVA DRUGO POLUVREME GOST (TIM2)
    if tip.startswith('2G'):
        # 2G0-x
        if tip.startswith('2G0-') and tip_len == 5:
            return 'UG_2P_TIM2_0-' + tip[4]
        # 2G2+
        if tip.startswith('2G') and tip.endswith('+') and tip_len == 4:
            return 'UG_2P_TIM2_' + tip[2] + '+'
        # 2G0
        if tip == '2G0':
            return 'UG_2P_TIM2_T0'

    raise ValueError(f'Unexpected tip_name: |{tip_name}|')
