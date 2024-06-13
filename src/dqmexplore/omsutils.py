import pandas as pd
import plotly.graph_objects as go
import numpy as np

def makeDF(json):
    datadict = json["data"][0]["attributes"]
    keys = datadict.keys()

    datasetlist = []

    for i in range(len(json["data"])):
        values = json["data"][i]["attributes"].values()
        datasetlist.append(values)
    return pd.DataFrame(datasetlist, columns=keys)

def get_rate(
        oms_fetch,
        runnb,
        dataset_name,
        extrafilters=[],
        dataframe = True
):
    filters = [
        dict(attribute_name="dataset_name", value=dataset_name, operator="EQ"),
        dict(attribute_name="run_number", value=runnb, operator="EQ")
    ]
    filters.extend(extrafilters)
    
    query = oms_fetch.query("datasetrates")
    query.filters(filters)
    query.per_page = 2000

    omstrig_df = makeDF(query.data().json())

    if dataframe:
        return omstrig_df
    else:
        return omstrig_df["rate"].to_numpy()

def plot_rate(trigrate_df, norm=False, show=False):
    runnb = trigrate_df["run_number"].unique()[0]
    
    fig = go.Figure()

    rate = np.array(trigrate_df["rate"])
    if norm:
        rate = rate / rate.sum()

    fig.add_trace(
        go.Scatter(
            x = trigrate_df["last_lumisection_number"],
            y = rate,
            mode="lines"
        )
    )

    fig.update_layout(
        title = f"Trigger rate (Run {runnb})",
        xaxis_title = "Lumisection",
        yaxis_title = "Trigger rate",
    )

    fig.update_yaxes(range=[0, rate.max()])
    fig.update_xaxes(range=[1, trigrate_df["last_lumisection_number"].max()])

    if show:
        fig.show()
    else:
        return fig