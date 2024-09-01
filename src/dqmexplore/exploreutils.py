from dqmexplore.dataproc import generate_me_dict
import pandas as pd

def check_empty_lss(me_df, thrshld=0):
    me_dict = generate_me_dict(me_df)
    empty_me_dict = {}
    for me in list(me_dict.keys()):
        empty_me_dict[me] = {}
        empty_me_dict[me]["empty_lss"] = []
        for i, entries in enumerate(me_dict[me]["entries"]):
            if entries <= thrshld:
                empty_me_dict[me]["empty_lss"].append(i + 1)
    return pd.DataFrame(empty_me_dict).T
