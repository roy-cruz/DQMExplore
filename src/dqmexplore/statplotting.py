import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dqmexplore.dataproc import generate_me_dict, normalize, integrate, trig_normalize

def plotMEs1D_static(
        me_df,
        fig_title = "",
        ax_labels = None,
        ls_filter = [],
        trigger_rates = None,
        norm = False,
        ref_df = None,
        show = False
    ):
    
    me_dict = generate_me_dict(me_df)

    # Check that all given MEs are either 1D or 2D
    all_1D = np.array([me_info["me_id"] <= 95 for me_info in me_dict.values()]).all()
    if (not all_1D) and (ref_df is not None):
        raise ValueError("Reference data given for invalid ME type(s). Plot 2D reference MEs separately.")
        
    # Generate reference dict if reference is given
    if (ref_df is not None):
        if norm == False:
            raise ValueError("To plot with reference, you must normalize")
        ref_dict = generate_me_dict(ref_df)
        ref_dict = integrate(ref_dict)
        ref_dict = normalize(ref_dict)
    else:
        ref_dict = None
    
    # Normalize by trig rate if trig rate is given
    if trigger_rates is not None:
        me_dict = trig_normalize(me_dict, trigger_rates=trigger_rates)

    # Integrate, and filter any undesired LSs
    me_dict = integrate(me_dict, ls_filter=ls_filter) 
    
    if norm:
        me_dict = normalize(me_dict)
    
    fig = create_plot_static(me_dict, fig_title=fig_title, ref_dict=ref_dict, ax_labels=ax_labels)

    if show:
        fig.show()
    else:
        return fig


def create_plot_static(me_dict, fig_title="", ref_dict=None, ax_labels=None):
    mes = list(me_dict.keys())
    num_mes = len(mes)

    num_rows = (num_mes + 1) // 2
    num_cols = 2 if num_mes > 1 else 1

    fig = make_subplots(
        rows=num_rows, cols=num_cols,
        subplot_titles=mes,
        vertical_spacing = 0.1,
        horizontal_spacing = 0.1
    )

    for i, me in enumerate(mes):
        row = (i // 2) + 1
        col = (i % 2) + 1
        if me_dict[me]["me_id"] <= 95:
            trace = go.Bar()
            trace.x = me_dict[me]["x_bins"]
            trace.y = me_dict[me]["data"][0]
            trace.name = me
        elif me_dict[me]["me_id"] >= 96:
            trace = go.Heatmap()
            trace.x = me_dict[me]["x_bins"]
            trace.y = me_dict[me]["y_bins"]
            trace.z = me_dict[me]["data"][0]
            trace.name = me
        fig.add_trace(trace, row=row, col=col)

    fig.update_layout(
        title_text=fig_title,
        title_font={"size": 24},
        bargap=0,
        showlegend=True,
        width=1500,
        height=1500,
    )

    for i, me in enumerate(mes):
        
        row = (i // num_cols) + 1
        col = (i % num_cols) + 1
        
       
        if me_dict[me]["me_id"] <= 95:
            ref_max = 0 if ref_dict is None else ref_dict[me]["data"].max()
              
            max_data = max([me_dict[me]["data"].max(), ref_max]) + (0.01 if me_dict[me]["data"].max() < 1 else 10)
            fig.update_yaxes(range=[0, max_data], row=row, col=col)
            
        if me_dict[me]["me_id"] >= 96:
            fig.update_traces(showscale=False)
            
        if ax_labels is not None:
            fig.update_xaxes(title_text=ax_labels[i]["x"], row=row, col=col)
            fig.update_yaxes(title_text=ax_labels[i]["y"], row=row, col=col)
            
        if ref_dict is not None:
            trace_ref = go.Scatter()
            trace_ref.name = me+"-Reference"
            trace_ref.x = ref_dict[me]["x_bins"]
            trace_ref.y = ref_dict[me]["data"][0]
            trace_ref.opacity=0.6
            trace_ref.line=dict(shape='hvh')
            fig.add_trace(trace_ref, row=row, col=col)

    return fig

def plotheatmaps1D(
    me_df,
    fig_title = "",
    ax_labels = None,
    trigger_rates = None,
    norm = False,
    show = False,
    ):
    
    me_dict = generate_me_dict(me_df)
    
    if trigger_rates is not None:
        trig_normalize(me_dict, trigger_rates)
    if norm:
        me_dict = normalize(me_dict)
        
    fig = create_heatmap(me_dict, fig_title=fig_title, ax_labels=ax_labels)
    
    if show:
        fig.show()
    else:
        return fig

def create_heatmap(me_dict, fig_title="", ax_labels=None):
    
    mes = list(me_dict.keys())
    num_mes = len(mes)
    num_rows = (num_mes + 1) // 2
    num_cols = 2 if num_mes > 1 else 1
    
    # Making figure object
    fig = make_subplots(
        rows=num_rows, cols=num_cols, 
        subplot_titles = mes,
        vertical_spacing = 0.1,
        horizontal_spacing = 0.1
    )

    # Adding heatmap trace to figure
    for i, me in enumerate(mes):
        row = (i // 2) + 1
        col = (i % 2) + 1
        fig.add_trace(
            go.Heatmap(z=me_dict[me]["data"], x=me_dict[me]["x_bins"], showscale=False),
            row=row, col=col,
        )
        if ax_labels is not None:
            fig.update_xaxes(title_text=ax_labels[i]["x"], row=row, col=col)
            fig.update_yaxes(title_text=ax_labels[i]["y"], row=row, col=col)

    # Adding layour elements to figure
    fig.update_layout(
        title_text=fig_title,
        title_font={"size": 24},
        height=1100,
        width=1100,
        annotations = [dict(text = me, font={"size": 14}, showarrow=False) for me in mes],
    )

    fig.update_yaxes(autorange="reversed")

    return fig