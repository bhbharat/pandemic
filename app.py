
import pandas as pd 
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)
# Creating Dash app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

h=pd.read_csv('time-series-splitted/TIME_serie_donnees-hospitalieres-Number_of_people_currently_hospitalized.csv')
h=h.melt(id_vars=['Unnamed: 0','code','DEPARTMENT'])
h=h.groupby(['DEPARTMENT','variable'])['value'].sum().reset_index()
# Generating 3 Plots from the pandemic dataset
import plotly.express as px
fig1 = px.scatter(h, x="variable", y="value", color="DEPARTMENT").update_traces(mode='lines+markers').update_layout(dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=700,
        xaxis={
            "showline": True,
            "zeroline": False,
            "title": "Date",
        },
        yaxis={
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(h["value"].iloc[-1] / 10)),
            "title":"Number_of_people_currently_hospitalized",
        },
    ))

p=pd.read_csv('time-series-splitted/TIME_serie_donnees-hospitalieres-Total_amount_of_patient_that_returned_home.csv')
p=p.melt(id_vars=['Unnamed: 0','code','DEPARTMENT'])
p=p.groupby(['DEPARTMENT','variable'])['value'].sum().reset_index()
# Generating 2nd Plot
import plotly.express as px
fig2 = px.scatter(p, x="variable", y="value", color="DEPARTMENT").update_traces(mode='lines+markers').update_layout(dict(
        height=350,
        width=400,
    xaxis={
            "showline": True,
            "zeroline": False,
            "title": "Date",
        },
        yaxis={
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "title":"Number_of_people_returned_home",
        },
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        autosize=False,
        showlegend=False,
    ))


d=pd.read_csv('time-series-splitted/TIME_serie_donnees-hospitalieres-Total_amout_of_deaths_at_the_hospital.csv')
d=d.melt(id_vars=['Unnamed: 0','code','DEPARTMENT'])
d=d.groupby(['DEPARTMENT','variable'])['value'].sum().reset_index()
# Generating 3rd Plot
import plotly.express as px
fig3 = px.scatter(d, x="variable", y="value", color="DEPARTMENT").update_traces(mode='lines+markers').update_layout(dict(
        height=350,
        width=400,
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        xaxis={
            "title": "Date",
            "showgrid": False,
            "showline": False,
            "fixedrange": True,
        },
        yaxis={
            "showgrid": False,
            "showline": False,
            "zeroline": False,
            "title": "Number of deaths_at_the_hospital",
            "fixedrange": True,
        },
        autosize=True,
        bargap=0.01,
        bargroupgap=0,
        hovermode="closest",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "xanchor": "center",
            "y": 1,
            "x": 0.5,
        },showlegend=False,
    ))


# Defining the layout of the web app
app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("PANDEMIC DASHBOARD", className="app__header__title"),
                        html.P(
                            "This app takes the data from pandemic dataset and plots the live updates.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6('Number of people currently hospitalized'.upper(), className="graph__title")]
                        ),
                        dcc.Graph(
                            id="wind-speed",
                            figure=fig1
                        ),
                        dcc.Interval(
                            id="wind-speed-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ],
                    className="two-thirds column wind__speed__container",
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "patients returned home".upper(),
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="wind-histogram",
                                    figure=fig2
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "deaths at hospital".upper(), className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="wind-direction",
                                    figure=fig3
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)

if __name__=='__main__':
    app.run_server(debug=True)
