"""CSC110 Fall 2021 Project: Graphing the Data

This Python module contains the functions that format and graph the relevant COVID-19, marriage,
and birth data from the COVID19 Data and Vital Events Data by Month datasets using Plotly. The
graphs include the actual data, approximated sinusoidal curves, and differences between these two,
for marriages and births.

This file is Copyright (c) 2021 Cosette Li, Amelia Riddell, and Jamie Yuan.
"""
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from extract_data import covid19_data, marriage_data, birth_data
from compute_on_data import calculate_sinusoid, marriage_difference, birth_difference


def graph_data() -> None:
    """Graph the COVID19 Data and Vital Events Data by Month data using Plotly. Format and graph
    the differences between the actual and expected values (based on the calculated sinusoidal
    equations) for marriages and births, using Plotly.
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    data_dict = format_graph_data()
    fig.add_trace(go.Scatter(x=data_dict['dates'], y=data_dict['cases rescaled'],
                             name='Cases (rescaled)', line=dict(color='black')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data_dict['dates'], y=data_dict['marriages actual'],
                             name='Marriages (actual)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data_dict['dates'], y=data_dict['births actual'],
                             name='Births (actual)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data_dict['dates'], y=data_dict['marriages sinusoid'],
                             name='Marriages (sinusoid)', line=dict(dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data_dict['dates'], y=data_dict['births sinusoid'],
                             name='Births (sinusoid)', line=dict(dash='dot')), row=1, col=1)
    fig.add_vline(x='2020-01', line_width=2, line_dash='dash', line_color='brown', row=1, col=1)
    # mark the approximate discovery of COVID-19

    fig.add_trace(go.Scatter(x=data_dict['dates'], y=list(marriage_difference().values()),
                             name='Marriages (difference)', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=data_dict['dates'], y=list(birth_difference().values()),
                             name='Births (difference)', line=dict(color='green')), row=2, col=1)
    fig.add_vline(x='2020-01', line_width=2, line_dash='dash', line_color='brown', row=2, col=1)
    # mark the approximate discovery of COVID-19

    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_yaxes(title_text='Number', row=1, col=1)
    fig.update_yaxes(title_text='Difference', row=2, col=1)
    fig.update_layout(title='Number of New COVID-19 Cases, Marriages, and Births in Canada',
                      height=800)

    fig.show()


def format_graph_data() -> dict[str, list]:
    """Format and rescale the COVID19 Data and Vital Events Data by Month data to be used in Plotly
    by the graph_data function.
    """
    cases19cases_1819 = [0] * 24  # no COVID cases in 2018 or 2019
    num_covid19cases = cases19cases_1819 + [(num / 800) for num in covid19_data().values()]
    # rescaled to adjust for num_covid19cases being greater than num_marriages and num_births by a
    # factor, to more easily visually compare the graphs

    return {'dates': list(birth_data().keys()),
            'cases rescaled': num_covid19cases,
            'marriages actual': list(marriage_data().values()),
            'births actual': list(birth_data().values()),
            'marriages sinusoid': format_sinusoid_data(marriage_data()),
            'births sinusoid': format_sinusoid_data(birth_data())}


def format_sinusoid_data(data: dict[str, int]) -> list[float]:
    """Format the sinusoid data approximating the marriage or birth data to be used in Plotly by
    the graph_data function.
    """
    a, b, c, d = calculate_sinusoid(data)

    sinusoid = []
    for x in range(36):  # adjust based on the graph of the curve
        if data == marriage_data():
            sinusoid.append((a * math.sin(b * (x - c)) + d) + 1750)
        elif data == birth_data():
            sinusoid.append((a * math.sin(b * (x - c)) + d) + 1000)

    return sinusoid


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     python_ta.check_all(config={
#         'extra-imports': ['math', 'plotly.subplots', 'plotly.graph_objects', 'python_ta.contracts'],
#         'max-line-length': 100,
#         'disable': ['R1705', 'C0200']
#     })
