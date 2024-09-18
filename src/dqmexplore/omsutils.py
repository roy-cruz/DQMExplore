import pandas as pd
import plotly.graph_objects as go
import numpy as np
from cmsdials.filters import OMSFilter, OMSPage


def makeDF(json):
    datadict = json["data"][0]["attributes"]
    keys = datadict.keys()

    datasetlist = []

    for i in range(len(json["data"])):
        values = json["data"][i]["attributes"].values()
        datasetlist.append(values)
    return pd.DataFrame(datasetlist, columns=keys)


def get_rate(dials, runnb, dataset_name, extrafilters=[], rtrn_np=True):
    filters = [
        OMSFilter(attribute_name="run_number", value=runnb, operator="EQ"),
        OMSFilter(attribute_name="dataset_name", value=dataset_name, operator="EQ"),
    ]

    data = dials.oms.query(
        endpoint="datasetrates", 
        filters=filters,
        pages=[OMSPage(attribute_name="limit", value=5000)],
    )
    
    data_df = makeDF(data)
    data_df.sort_values(by="last_lumisection_number", inplace=True)

    if rtrn_np:
        return data_df["rate"].to_numpy()
    else:
        return data_df


def plot_rate(trigrate_df, norm=False, show=False):
    runnb = trigrate_df["run_number"].unique()[0]

    fig = go.Figure()

    rate = np.array(trigrate_df["rate"])
    if norm:
        rate = rate / rate.sum()

    fig.add_trace(
        go.Scatter(x=trigrate_df["last_lumisection_number"], y=rate, mode="lines")
    )

    fig.update_layout(
        title=f"Trigger rate (Run {runnb})",
        xaxis_title="Lumisection",
        yaxis_title="Trigger rate",
    )

    fig.update_yaxes(range=[0, rate.max() + rate.max() * 0.1])
    fig.update_xaxes(range=[1, trigrate_df["last_lumisection_number"].max()])

    if show:
        fig.show()
    else:
        return fig
