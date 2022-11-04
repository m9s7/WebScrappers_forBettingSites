def standardize_soccer_tip_name_old(tip):
    tip = tip.strip()
    tip_len = len(tip)

    # print('converting', tip, " len = ", len(tip))
    res = ""
    if tip.startswith('1') or tip.startswith('2'):
        res += tip[0]
        tip = tip[1:]

    if tip.startswith('D'):
        return res + "tm1 " + tip[1:]
    elif tip.startswith('G'):
        return res + "tm2 " + tip[1:]

    if tip.startswith('ug'):
        if tip_len == 7 and tip[5] == "T":
            return tip[3] + 'ug 0'
        elif tip_len == 8 and tip[4] == 'P':
            return tip[3] + 'ug ' + tip[5:]
        else:
            return tip

    raise ValueError(f'Unexpected tip_name: {tip}')