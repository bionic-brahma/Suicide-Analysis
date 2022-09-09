#import packages to create app
from locale import locale_alias
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import numpy as np



#get unique continents
# cont_names = gapminder['continent'].unique()
#data for the region plot
#data for the Suicide plots

loc_data = pd.read_csv("assets/processed_data/output.csv")
df = loc_data
loc_cols=list(loc_data.columns)
cols=list(loc_data.columns)
# loc_data = loc_data.iloc[10:1000]
country_names = loc_data['country'].unique()

cont_names = loc_data['continent'].unique()


# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#303030 !important',
    'text': '#ffffff'
} 
color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 'Americas': '#00CC96',
    'Europe': '#AB63FA', 'Oceania': '#FFA15A'}


# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Global Suicide Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Suicide Rate vs GDP per Capita for different Countries from 1985 to 2005
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),
    html.Div([
        html.Div([

            ################### start of first row #######################   
                html.H1('Suicide Statistics Countrywise',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),
                dbc.Row(children=[
                    dbc.Col(children=[
                    html.Label('Select Continent'),
                    dcc.Dropdown(id='cont_dropdown',
                                options=[{'label': i, 'value': i}
                                        for i in cont_names],
                                value=cont_names,
                                multi=True,
                                style={
                                    # 'textAlign': 'center',
                                    'color': '#1c1818',
                                }
                    )
                    ], className='ml-2 mb-2'),  
                        dbc.Col(dbc.Col(children=[
                                html.Label('Select Suicide Range'),
                             dcc.RangeSlider(id='pop_range',
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
                                ], className='ml-2 mb-2'),
                        ),
                    ]),

        
        ]),
            ################### End of first row #######################  
                dbc.Row([
                dbc.Col(html.Div(children=
                    [
                        dcc.Graph(id='LifeExpVsGDP',
                        responsive=True,
                        style={
                            "width": "100%",
                            "height": "100%",
                        },),               
                    ],className=''),className='col-11 col-sm-11 col-md-11 mr-3 mt-3'),

                ],className='pt-2 pb-2',
                    style={"width": "100%",
                    "height": "500px",
                    "display": "inline-block",
                    "padding-left": "15px",
                    "padding-right": "15px",
                    "overflow": "hidden",
                    "align":"center"}),

            ################### End of second row #######################    
                dbc.Row([
                dbc.Col(html.Div(children=
                    [
                        dcc.Dropdown(id='y_dropdown',
                        options=[                    
                            {'label': 'Suicide', 'value': 'sucid_in_hundredk'},
                            {'label': 'Population', 'value': 'population'},
                            {'label': 'GDP per Captia', 'value': 'gdp_per_capita'}],
                        value='sucid_in_hundredk',
                        style={'width':'50%',
                               'color': '#1c1818',},
                        ),               
                    ],className='ml-3 mr-3 mt-3'),className='col-11 col-sm-12 col-md-12'),

            ], 
            className='text-center pb-3',
            style={}),

            ################### End of third row #######################   
                    dbc.Row([
                        dbc.Col(html.Div(children=
                            [
                                html.Div([
                                    dcc.Graph(id='LifeExp')
                                    ],className=' mr-3 ml-3',
                                    style={}),    
                            ]),className='col-6 col-sm-6 col-md-6'),

                       
                        dbc.Col(html.Div(children=
                            [
                                html.Div([
                                    dcc.Graph(id='LifeExpOverTime',)
                                    ],className=' mr-3 ml-3',
                                    style={}),    
                            ]),className='col-6 col-sm-6 col-md-6'),

                         ],className='text-center pb-3',style={}),

            ################### End of fourth row #######################         


])
])
@app.callback(
    Output(component_id='LifeExpVsGDP', component_property='figure'),
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='pop_range', component_property='value')]
)
def update_graph(selected_cont,rangevalue):
    if not selected_cont:
        return dash.no_update
    data =[]
    d = loc_data[(loc_data['sucid_in_hundredk'] >= rangevalue[0]) & (loc_data['sucid_in_hundredk'] <= rangevalue[1])]
    # d = gapminder[(gapminder['population'] >= rangevalue[0]) & (gapminder['population'] <= rangevalue[1])]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="gdp_per_capita", y="sucid_in_hundredk",
                size="sucid_in_hundredk", color="continent",hover_name="country",
                # different colour for each country
                color_discrete_map=color_discrete_map, 
                #add frame by year to create animation grouped by country
                animation_frame="year",animation_group="country",
                #specify formating of markers and axes
                # log_x = True, size_max=60, range_x=[100,100000], range_y=[28,92],
                log_x = True, size_max=60, range_x=[100,100000], range_y=[28,92],
                # change labels
                labels={'population':'Population','year':'Year','continent':'Continent',
                        'country':'Country','suicides':'Suicide','gdp_per_capita':"GDP/Capita"})
    # Change the axis titles and add background colour using rgb syntax
    scat_fig.update_layout({'xaxis': {'title': {'text': 'log(GDP Per Capita)'}},
                  'yaxis': {'title': {'text': 'Suicide'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    return scat_fig



@app.callback(
    [Output(component_id='LifeExp', component_property='figure'),
    Output(component_id='LifeExpOverTime', component_property='figure')],
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='pop_range', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_map(selected_cont,rangevalue,yvar):
    if not (selected_cont or rangevalue or yvar):
        return dash.no_update
    d = loc_data[(loc_data['sucid_in_hundredk'] >= rangevalue[0]) & (loc_data['sucid_in_hundredk'] <= rangevalue[1])]
    data =[]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    map_fig= px.choropleth(df,locations="country_code", color=df[yvar],
            hover_name="country",hover_data=['continent','sucid_in_hundredk'],animation_frame="year",    
            color_continuous_scale='Turbo',range_color=[df[yvar].min(), df[yvar].max()],
            labels={'sucid_in_hundredk':'Suicide in hundredk','year':'Year','continent':'Continent',
                'country':'Country','suicides':'Suicide'})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    line_fig = px.line(data_frame=df, 
                x="year",  y = df[yvar] , color='continent',line_group="country", 
                hover_data=['sucid_in_hundredk','year'],
                 # Add bold variable in hover information
                  hover_name='country',color_discrete_map=color_discrete_map,
                 # change labels
                 labels={'sucid_in_hundredk':'Population','year':'Year','continent':'Continent',
                     'country':'Country','suicides':'Suicide'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [map_fig, line_fig]

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8097,debug=True)
