
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pytz import country_names


df = pd.read_csv("assets/processed_data/output.csv")
# df = df.iloc[10:1000]
columnss=list(df.columns)
country_names = df['country'].unique()


from app import app

{'Albania': '#000000', 'Austria': '#FFFF00', 'Belgium': '#1CE6FF',
    'Bosnia and Herzegovina': '#FF34FF','Bulgaria': '#FF4A46', 'Croatia': '#008941',
    'Czech Republic': '#006FA6', 'Denmark': '#A30059', 'Finland': '#FFDBE5',
    'France': '#7A4900', 'Germany': '#0000A6', 'Greece': '#63FFAC', 'Hungary': '#B79762',
    'Iceland': '#8FB0FF', 'Ireland': '#004D43','Italy': '#997D87', 'Montenegro': '#5A0007',
    'Netherlands': '#809693', 'Norway': '#FEFFE6', 'Poland': '#1B4400','Portugal': '#4FC601',
    'Romania': '#3B5DFF', 'Serbia': '#4A3B53', 'Slovak Republic': '#FF2F80',
    'Slovenia': '#61615A','Spain': '#BA0900', 'Sweden': '#6B7900', 'Switzerland': '#00C2A0',
    'Turkey': '#FFAA92','United Kingdom': '#FF90C9'}


layout = html.Div([
################### start of first row #######################   
                html.H1('Suicide Statistics Countrywise',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),
                dbc.Row(children=[
                    dbc.Col(children=[
                    html.Label('Select Countries'),
                    dcc.Dropdown(id='country_drop',
                                options=[{'label': i, 'value': i}
                                        for i in country_names],
                                value=country_names,
                                multi=True,
                                style={
                                    # 'textAlign': 'center',
                                    'color': '#1c1818',
                                }
                    )
                    ], className='ml-2 mb-2'),  
                        dbc.Col(html.Div([
                                dbc.Col(children=[
                                html.Label('Select Suicide Range'),
                                dcc.RangeSlider(id='suicides_slider',
                                    min=0,
                                    max=180,
                                    value=[0,180],
                                    step= 1,
                                    marks={
                                        0: '0',
                                        50: '50',
                                        100: '100',
                                        178: '178',
                                    },
                                )
                                ]),
                                ],className='pb-2')
                        ),
                    ]),

################### End of first row #######################   
            dbc.Row([
                dbc.Col(html.Div(children=[
                    dcc.Graph(id="distance_graph")],className='ml-3 mt-3')
                    ,className='col-6 col-sm-6 col-md-6'),
                dbc.Col(html.Div(children=[
               
                    dcc.Graph(id="scat_graph")],className='mr-3 mt-3')
                    ,className='col-6 col-sm-6 col-md-6'),

            ], 
            className='text-center pt-2 pb-2',
            style={}),

################### End of second row #######################    
            dbc.Row([
                 dbc.Col(html.Div(children=[
                dcc.Graph(id="count_dist_graph")],className='mt-3 ml-3')
                ,className='col-6 col-sm-6 col-md-6'),
                dbc.Col(html.Div(children=[
                    dcc.Graph(id="shot_graph")],style={}, className='mt-3 mr-3')
                    ,className='col-6 col-sm-6 col-md-6'),
            ], 
            className='text-center pt-2 pb-2',
            style={}),

################### start of footer row #######################   
        
        dbc.Row([
            dbc.Col(children=[
                    dbc.Col(html.H5(children='Copyright © 2022, Dundalk Institute of Technology. All Rights Reserved',
                    className="text-center pt-2 pb-2"),
                                        
            ),
            dbc.Col(children=[
                    dbc.Col(
                    html.H5(children='Mob : +353 89 273 8178',
                    className="text-center pb-2"),
                                  
                )

            ]),
            dbc.Col(children=[
                    dbc.Col(
                    html.H5(children='Email : d00242726@student.dkit.ie',
                    className="text-center pb-2"),
                                  
                )

            ])

    ]),
    ],className="pt-2")

])

@app.callback(
    [Output(component_id='distance_graph', component_property='figure'),
     Output(component_id='count_dist_graph', component_property='figure'),
     Output(component_id='shot_graph', component_property='figure'),
     Output(component_id='scat_graph', component_property='figure'),],
    [Input(component_id='country_drop', component_property='value'),
     Input(component_id='suicides_slider', component_property='value'),
    ]
)

def update_line_chart(country_names, range_chosen):
    if not (country_names or range_chosen):
        return dash.no_update
    d = df[(df['sucid_in_hundredk'] >= range_chosen[0]) & (df['sucid_in_hundredk'] <= range_chosen[1])]
    data =[]
    for j in country_names:
            data.append(d[d['country'] == j])
    dff = pd.DataFrame(np.concatenate(data), columns=columnss)
    dff=dff.infer_objects()
    mask = dff.country.isin(country_names)
    tempdf = dff[mask]
    for_plot = tempdf.groupby(["year", "country_code", "country"])["sucid_in_hundredk"].sum()
    ndf = pd.DataFrame()
    yrs = []
    cc = []
    c =[]
    sd = []
    for key, values in for_plot.items():
        yrs.append(key[0])
        cc.append(key[1])
        c.append(key[2])
        sd.append(values)

    ndf["year"] = yrs
    ndf["country_code"] = cc
    ndf["country"] = c
    ndf["sucid_in_hundredk"] = sd

    fig= px.choropleth(ndf,               
              locations="country_code", color="sucid_in_hundredk",
              hover_name="country",  
              animation_frame="year")
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False)
    mask2 = dff.country.isin(country_names)
    fig2 = px.histogram(dff[mask2],x="sex", y="population", color='country')

    mask1 = dff.country.isin(country_names)
    # fig1 = px.bar(dff[mask1],x="country", y="population", color='population')
    fig1 = px.sunburst(dff[mask1], path=['sex', 'country', 'country_code'], values='suicides')

    # fig3 = px.scatter(dff[mask3],x="sucid_in_hundredk", y="population", color='sex')
    dfff=dff.groupby(["country"], as_index=False)[["sucid_in_hundredk","gdp_per_capita"]].mean()
    mask3 = dfff.country.isin(country_names)

    fig3 = px.scatter(
            data_frame=dfff[mask3],
            x="sucid_in_hundredk",
            y="gdp_per_capita",
            hover_data=['country'],
            text="country",labels={"sucid_in_hundredk": "Suicide per hundred thousand","gdp_per_capita": "GDP Per capita",})
    return [fig, fig1, fig3, fig2]





