
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
countries = list(set(df.country.to_list()))
columnss=list(df.columns)
country_names = df['country'].unique()


from app import app


layout = html.Div([
################### start of first row #######################   
                html.H5('Data Integrity Check Via Periodic Ouliers Detection',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),

                dbc.Row(children=[


                    dbc.Col(html.Div(children=[
                            dcc.Graph(id="outlier_graph")
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
        Output(component_id='outlier_graph', component_property='figure'),
     ],
    [
        Input(component_id='country_dropdown', component_property='value'),
        Input(component_id='year_range', component_property='value'),
    ]
)


def update_line_chart(country_dropdown, year_range):
    if not (country_dropdown or year_range):
        return dash.no_update
    possible_years = [str(y) for y in range(year_range[0], year_range[1])]

    raw_data = pd.read_csv("assets/processed_data/output.csv")
    outliers = pd.read_csv("assets/processed_data/outliers.csv")
    
    raw_data = raw_data[["year","sucid_in_hundredk", "country"]]
    outliers = outliers[["year","sucid_in_hundredk","country"]]

    raw_data["year_of_focus"] = raw_data.year.apply(lambda x: str(x).split("-")[0])
    outliers["year_of_focus"] = outliers.year.apply(lambda x: str(x).split("-")[0])

    new_df = pd.DataFrame()
    new_df["year_of_focus"] = possible_years

    new_raw_df = pd.merge(new_df,raw_data, on = "year_of_focus", how = "left")
    new_outlier_df = pd.merge(new_df,outliers, on = "year_of_focus", how = "left")
    new_raw_df = new_raw_df[new_raw_df.country == country_dropdown]
    new_outlier_df = new_outlier_df[new_outlier_df.country == country_dropdown]

    new_outlier_df["outlier"] = "Outlier"
    print(new_outlier_df)
    print(new_raw_df)
    new_raw_df = pd.merge(new_raw_df,new_outlier_df, on = ["year_of_focus","sucid_in_hundredk","country"], how = "left")

    outliers_label = []
    for i in new_raw_df.outlier.to_list():
        if i == "Outlier":
            outliers_label.append("Outlier Point")
        else:
            outliers_label.append("Good Point")

    new_raw_df["Outlier Detection"] = outliers_label

    fig = px.scatter(
            data_frame=new_raw_df,
            y="sucid_in_hundredk",
            x="year_of_focus",
            color = "Outlier Detection",
            labels={"sucid_in_hundredk": "Suicide per hundred thousand","year_of_focus": "Year",})


    return [fig]





