import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
from dash_table import DataTable, FormatTemplate
import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, dash_table
from app import app


#data for the Suicide plots

df = pd.read_csv("assets/processed_data/output.csv")

#data for the Suicide plots
#data for the region plot
# df = pd.read_csv('assets/cleaned_data1.csv')
dat_columns = df.columns



layout = html.Div([
            dbc.Col(children=[
                html.H1('Suicide Data',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    },
                className='text-center pb-3'
                ),

            ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dash_table.DataTable(
                df.to_dict('records'),
                [{"name": i, "id": i} for i in df.columns],
                cell_selectable=False,
                # Add sorting
                sort_action='native',
                # Add filtering
                filter_action='native',
                page_action='native',
                # Start on the first page
                page_current=0,
                # Render 7 items per page
                page_size=10,
                ),
    
        ],style={
                    'textAlign': 'center',
                    'color': '#131414',
                },className='text-center pb-3'),
    ],className="pt-2"),
])