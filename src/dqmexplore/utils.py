def check_empty_ls(me_dict, thrshld = 10):
    empty_me_dict = {}
    for me in list(me_dict.keys()):
        empty_me_dict[me] = {}
        empty_me_dict[me]["empty_lss"] = []
        for i, entries in enumerate(me_dict[me]["entries"]):
            if entries < thrshld:
                empty_me_dict[me]["empty_lss"].append(i + 1)
    return empty_me_dict