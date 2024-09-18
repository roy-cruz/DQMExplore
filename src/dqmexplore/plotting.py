import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dqmexplore.dataproc import generate_me_dict, normalize, integrate, trig_normalize


# Plotting function
def plot1DMEs(
    me_data,
    fig_title="",
    ax_labels=None,
    trigger_rates=None,
    ref_df=None,
    norm=False,
    show=False,
    hspace=0.05,
    vspace=0.15,
    width=1600,
    height=1600,
):
    """
    Create interactive per-LS plotly figure from monitoring element(s) dataframe. Just for one run and for 1D MEs.
    """

    # Check
    if ref_df is not None:
        if not norm:
            raise ValueError("To display reference, you must normalize the MEs.")

    # Extraction
    if isinstance(me_data, pd.DataFrame):
        me_dict = generate_me_dict(me_data)
    elif isinstance(me_data, dict):
        me_dict = me_data
    else:
        raise ValueError("Wrong type for me_data.")

    # Processing
    if trigger_rates is not None:
        me_dict = trig_normalize(me_dict, trigger_rates)
    if norm:
        me_dict = normalize(me_dict)

    # Integrate reference data if given
    if ref_df is not None:
        ref_dict = generate_me_dict(ref_df)
        ref_dict = integrate(ref_dict)
        ref_dict = normalize(ref_dict)
    else:
        ref_dict = None

    # Plotting
    fig = create_plot(
        me_dict,
        fig_title=fig_title,
        hspace=hspace,
        vspace=vspace,
        width=width,
        height=height,
        ax_labels=ax_labels,
        ref_dict=ref_dict,
    )

    if show:
        fig.show()
    else:
        return fig


def plot2DMEs(
    me_df,
    fig_title="",
    hspace=0.05,
    vspace=0.15,
    width=1600,
    height=1600,
    ax_labels=None,
    trigger_rates=None,
    show=False,
):

    # Extraction
    me_dict = generate_me_dict(me_df)

    # Processing
    if trigger_rates is not None:
        me_dict = trig_normalize(me_dict, trigger_rates)

    # Plotting
    fig = create_plot(
        me_dict,
        fig_title=fig_title,
        ax_labels=ax_labels,
        hspace=hspace,
        vspace=vspace,
        width=width,
        height=height,
    )

    if show:
        fig.show()
    else:
        return fig


def create_plot(
    me_dict, fig_title, hspace, vspace, width, height, ref_dict=None, ax_labels=None
):
    """
    Creates plotly interactive per-LS plot
    """

    all_1D = np.array([(me_info["dim"] == 1) for me_info in me_dict.values()]).all()
    if (not all_1D) and (ref_dict is not None):
        raise ValueError(
            "Reference data given for invalid ME type(s). Plot 2D reference MEs separately."
        )

    # Getting info about data
    num_mes = len(me_dict)
    num_lss = len(me_dict[list(me_dict.keys())[0]]["data"])
    num_rows = (num_mes + 1) // 2
    num_cols = 2 if num_mes > 1 else 1
    mes = list(me_dict.keys())

    # Making subplot and traces
    fig = make_subplots(
        rows=num_rows,
        cols=num_cols,
        subplot_titles=mes,
        vertical_spacing=vspace,
        horizontal_spacing=hspace,
    )
    fig.update_annotations(font_size=10)

    traces = []

    for i, me in enumerate(mes):
        row = (i // num_cols) + 1
        col = (i % num_cols) + 1
        for ls in range(num_lss):
            if me_dict[me]["dim"] == 1:
                trace = go.Bar()
                trace.x = me_dict[me]["x_bins"]
                trace.y = me_dict[me]["data"][ls]
            elif me_dict[me]["dim"] == 2:
                trace = go.Heatmap()
                trace.x = me_dict[me]["x_bins"]
                trace.y = me_dict[me]["y_bins"]
                trace.z = me_dict[me]["data"][ls]
            trace.name = me

            trace.visible = ls == 0
            traces.append(trace)
            fig.add_trace(traces[-1], row=row, col=col)

    steps = []
    for i in range(num_lss):
        step = {
            "method": "restyle",
            "args": [
                {"visible": [False] * num_mes * num_lss + [True] * len(mes)},
            ],
            "label": f"LS {i+1}",
        }
        for j in range(num_mes):
            step["args"][0]["visible"][i + j * num_lss] = True
        steps.append(step)

    sliders = [
        {
            "active": 0,
            "currentvalue": {"prefix": "LS: "},
            "pad": {"t": 50},
            "steps": steps,
        }
    ]

    # Making plots a bit prettier
    fig.update_layout(
        sliders=sliders,
        title_text=fig_title,
        title_font={"size": 24},
        bargap=0,
        showlegend=False,
        width=width,
        height=height,
    )

    for i, me in enumerate(mes):

        row = (i // num_cols) + 1
        col = (i % num_cols) + 1

        max_data = me_dict[me]["data"].max()
        if me_dict[me]["dim"] == 1:
            fig.update_yaxes(range=[0, max_data], row=row, col=col)

        if me_dict[me]["dim"] == 2:
            fig.update_traces(showscale=False)

        if ax_labels is not None:
            fig.update_xaxes(title_text=ax_labels[i]["x"], row=row, col=col)
            fig.update_yaxes(title_text=ax_labels[i]["y"], row=row, col=col)

        if ref_dict is not None:
            trace_ref = go.Scatter()
            trace_ref.name = me + "-Reference"
            trace_ref.x = ref_dict[me]["x_bins"]
            trace_ref.y = ref_dict[me]["data"][0]
            trace_ref.opacity = 0.6
            trace_ref.line = dict(shape="hvh")
            fig.add_trace(trace_ref, row=row, col=col)

    return fig
