import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plotinteractive1D(data: np.array, bin_locs: list[float], title: str, x_label: str, y_label: str, plot: bool = True) -> plotly.graph_objs._figure.Figure | None:
    """
    Data assumed to be in order of LS.
    """
    fig = go.Figure()

    max_y = data.max()

    fig = go.Figure(
        data=[
            go.Bar(
                x=bin_locs,
                y=data[0,:],
                visible=True,
                width=np.diff(bin_locs)
            )
        ],
    )

    # Building steps
    steps = []
    for i in range(len(data)):
        step = {
            "method": "restyle",
            "args": [{"y": [data[i, :]]}],
            "label": str(i+1),
        }
        steps.append(step)

    # Building slider using steps defined above
    sliders = [
        {
            "active": 0,
            "currentvalue": {"prefix": "LS: "},
            "pad": {"t": 50},
            "steps": steps,
        }
    ]

    # Passing all of this into the figure
    fig.update_layout(
        sliders=sliders,
        title=title,
        xaxis={
            "title": x_label
        },
        yaxis={
            "range": [0, max_y + 10],
            "title": y_label
        },
        bargap=0,
    )

    if plot:
        fig.show()
    else:
        return fig
    
def plotinteractive2D(data: np.array, title: str, x_label: str, y_label: str, plot: bool = True) -> plotly.graph_objs._figure.Figure | None:
    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=data[0], 
            colorscale="Viridis",
            zmin=data.min(),
            zmax=data.max()
        )
    )

    # Building steps
    steps = []
    for i in range(len(data)):
        step = {
            "method": "restyle",
            "args": [{"z": [data[i]]}],
            "label": str(i + 1)
        }
        steps.append(step)

    sliders = [
        {
            "active": 0,
            "currentvalue": {"prefix": "LS: "},
            "pad": {"t": 10},
            "steps": steps,
        }
    ]

    fig.update_layout(
        sliders=sliders,
        title_text = title,
        title_font = {"size": 24},
        xaxis={
            "title": x_label
        },
        yaxis={
            "title": y_label
        },
        height=750,
        width=750,
    )

    if plot:
        fig.show()
    else:
        return fig