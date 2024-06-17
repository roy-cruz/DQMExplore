import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from statistics import stdev


def calc_trends(histbins, ls, max_value, trigger_rate, norm=False):
    """
    Calculates ~peak value, std error on mean, and list of empty LS.
    Also normalises by trigger rate if norm=True

    Parameters:
    histbins: data in the form of numpy array
    ls: list of lumisections
    max_value: maximum value of the quantity being measured along x-axis
    trigger_rate: np array obtained from oms
    norm: Boolean (default False)

    Returns:
    list_means: position of peak. It's not precise because the distributions are not Gaussian
    list_std: standard error on mean
    list_good_ls: non-zero LS
    empty_ls:
    """
    list_means = []  # peak
    list_std = []
    list_good_ls = []
    empty_ls = []
    good_trigger = []
    for i in range(len(histbins)):
        ls_num = ls[i]
        # Calculate Mean and Std Error on Mean

        if any(histbins[i]):
            n_bins = len(histbins[i])
            actual_values = np.linspace(0, max_value, n_bins, endpoint=True)

            peak_value = np.average(
                actual_values, weights=histbins[i]
            )  # needs modification to get actual peak?? Fit a Landau/Langaus and get the MPV
            std_dev = stdev(histbins[i])
            sem = std_dev / np.sqrt(
                n_bins
            )  # standard error on mean = (standard deviation)/sqrt(n)

            list_good_ls.append(ls_num)
            list_means.append(peak_value)
            list_std.append(sem)
            good_trigger.append(trigger_rate[i])
        else:
            peak_value = 0
            std_dev = 0
            empty_ls.append(ls_num)

    if norm:

        list_means = np.divide(list_means, good_trigger)
        list_std = np.divide(list_std, good_trigger)

    return list_means, list_std, list_good_ls, empty_ls


def plot_trends(list_raw, list_norm, list_good_ls, title, me_name, runnb, write=False):

    plot = go.Figure()
    custom_ticks = [x for x in list_good_ls]
    plot.add_trace(go.Scatter(x=list(range(len(list_raw))), y=list_raw, visible=True))

    plot.add_trace(
        go.Scatter(x=list(range(len(list_norm))), y=list_norm, visible=False)
    )

    # Add dropdown
    plot.update_layout(
        title=title + ", " + me_name + ", Run: " + str(runnb),
        xaxis_title="LS",
        xaxis=dict(tickvals=list(range(len(list_good_ls))), ticktext=custom_ticks),
        updatemenus=[
            dict(
                buttons=list(
                    [
                        dict(
                            args=[{"visible": [True, False]}],
                            label="Raw",
                            method="restyle",
                        ),
                        dict(
                            args=[{"visible": [False, True]}],
                            label="Normalised",
                            method="restyle",
                        ),
                    ]
                ),
                direction="down",
            ),
        ],
    )

    plot.show()

    if write:
        html_content = pio.to_html(plot, include_plotlyjs="cdn")

        # Write the HTML content to a file
        name_hist = str(runnb) + "_" + me_name.split("/")[-1] + "_" + title + ".html"
        with open(name_hist, "w") as f:
            f.write(html_content)
        # pio.write_html(fig, name_hist)
