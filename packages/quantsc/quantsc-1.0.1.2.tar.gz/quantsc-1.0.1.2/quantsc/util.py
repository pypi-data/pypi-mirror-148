import pandas as pd
from dateutil import parser

import quantsc as qsc


def change_plot_backend(backend):
    if backend not in qsc.config.config['supported_plot_backend']:
        raise("Plotting backend must be in " + str(qsc.config.config['supported_plot_backend']))
    qsc.config.config['plot_backend'] = backend

def update_plotly_param():
    if 'get_ipython().__class__.__name__' == 'ZMQInteractiveShell':
        import plotly.offline as pyo
        pyo.init_notebook_mode()

# def round_dates(date_):
def round_dates(dates_array,freq = 'D',parse=True):
    rounded_arr = []
    for time in dates_array:
        if parse:
            time = parser.parse(time)
        time_pd = pd.Timestamp(time).round(freq=freq)
        rounded_arr.append(time_pd)
    return rounded_arr