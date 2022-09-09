
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pytz import country_names


#data for the Suicide plots
df = pd.read_csv("assets/processed_data/output.csv")
errors = pd.read_csv("assets/processed_data/error.csv")
#errors.index = errors.country
countries = list(set(errors.country.to_list()))
columnss=list(df.columns)
country_names = df['country'].unique()


from app import app


layout = html.Div([
################### start of first row #######################   
                html.H5('Suicide Forecast Countrywise',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),

                dbc.Row(children=[


                    dbc.Col(html.Div(children=[
                            dcc.Graph(id="distance_graphssss")
                        ],className='ml-3 mt-3')
                        ,className='col-6 col-sm-6 col-md-6'),



                    dbc.Col(html.Div(children=
                        [
                            html.Label('Select Country', className="pt-4 pb-4"),

                            ## drop down start    

                                                      dcc.Dropdown(id='country_dropdown',
                            options=countries,

                            value=countries[0],
                            style={'width':'70%',
                                'color': '#1c1818',},
                            ),


                            html.Label('Select Forecasting Model', className="pt-4 pb-4"),

                            ## drop down start    

                                                      dcc.Dropdown(id='model_dropdown',
                            options=[

                                ##

                                {'label': 'fbprophet', 'value': 'fbprophet'},
                                {'label': 'sarimax', 'value': 'sarimax'},
                                {'label': 'custom AR', 'value': 'AR'}],


                            value='sarimax',
                            style={'width':'70%',
                                'color': '#1c1818',},
                            ),


                            ## drop down ended


                            html.Label('Years', className="pt-4"),
                            dcc.RangeSlider(id='year_range',
                                min=1995,
                                max=2035,
                                value=[1995,2035],
                                step= 1,
                                marks={
                                    1995: '1995',
                                    2010: '2010',
                                    2025: '2025',
                                    2035: '2035',
                                },
                            ),
                         
                        ], className="pt-2 pb-2"
                        )), 

                    ]),

])

@app.callback(
    [
        Output(component_id='distance_graphssss', component_property='figure'),
     ],
    [
        Input(component_id='country_dropdown', component_property='value'),
        Input(component_id='model_dropdown', component_property='value'),
        Input(component_id='year_range', component_property='value'),
    ]
)


def update_line_chart(country_dropdown, model_dropdown, year_range):
    if not (country_dropdown or model_dropdown or year_range):
        return dash.no_update
    possible_years = [str(y) for y in range(year_range[0], year_range[1])]

    data = pd.read_csv("assets/processed_data/country_wise/data/"+country_dropdown+".csv")
    forecasted = pd.read_csv("assets/processed_data/country_wise/forecasted/"+country_dropdown+".csv")
    
    data["year_of_forecast"] = data.year.apply(lambda x: str(x).split("-")[0])
    forecasted["year_of_forecast"] = forecasted.year.apply(lambda x: str(x).split("-")[0])
    forecasted["forecasted"] = "Forcasted"
    new_df = pd.DataFrame()
    new_df["year_of_forecast"] = possible_years

    new_df = pd.merge(new_df,data, on = "year_of_forecast", how = "left")
    new_df = pd.merge(new_df,forecasted, on = "year_of_forecast", how = "left")

    forcasted_label = []
    for i in new_df.forecasted.to_list():
        if i == "Forcasted":
            forcasted_label.append("Forecasted Values")
        else:
            forcasted_label.append("Known Values")
    new_df["forecasted"] = forcasted_label
    

    error = int(100*errors[errors.country == country_dropdown][model_dropdown].to_list()[0])/100
    
    fig3 = px.scatter(
            data_frame=new_df,
            y="sucid_in_hundredk"+"_"+model_dropdown,
            x="year_of_forecast",
            color = "forecasted",
            labels={"sucid_in_hundredk"+"_"+model_dropdown: "Suicide per hundred thousand","year_of_forecast": "Year",})

    fig4 = px.line(
            data_frame=new_df,
            y="sucid_in_hundredk"+"_"+model_dropdown,
            x="year_of_forecast",
            labels={"sucid_in_hundredk"+"_"+model_dropdown: "Suicide per hundred thousand","year_of_forecast": "Year",})

    fig5 = px.scatter(
            data_frame=new_df,
            y="sucid_in_hundredk",
            x="year_of_forecast",
            labels={"sucid_in_hundredk": "Suicide per hundred thousand","year_of_forecast": "Year",})

    fig6 = px.line(
            data_frame=new_df,
            y="sucid_in_hundredk",
            x="year_of_forecast",
            labels={"sucid_in_hundredk": "Suicide per hundred thousand","year_of_forecast": "Year",})

    fig7 = go.Figure(data=fig3.data + fig4.data + fig5.data + fig6.data)

    fig7.update_layout(
    title=model_dropdown+" Model with RMSE: "+str(error),
    xaxis_title="Year",
    yaxis_title="Suicide per hundred thousand",
    
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
        )
    )

    return [fig7]





