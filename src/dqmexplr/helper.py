import pandas as pd
import numpy as np
import cmsdials

def extractdata(queryrslt: cmsdials.clients.h2d.models.PaginatedLumisectionHistogram2DList, rtn_arr=False) -> np.array:
    data_df = pd.DataFrame(queryrslt.dict()["results"])
    data_df.sort_values("ls_number", inplace=True)

    if rtn_arr:
        if len(data_df["me"].unique()) == 1:
            data_arr = data_df["data"].to_numpy(dtype=np.ndarray)
            data_arr = np.array([np.array(x) for x in data_arr])

        else:
            data_arr = []
            for me in data_df["me"].unique():
                me_arr = data_df[data_df["me"] == me]["data"].to_numpy(dtype=np.ndarray)
                me_arr = np.array([np.array(x) for x in me_arr])
                data_arr.append(me_arr)
            data_arr = np.array(data_arr)
        
        return (data_arr, data_df)
    else:
        return data_df