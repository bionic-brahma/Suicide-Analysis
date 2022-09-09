import dash
from dash import html
import dash_bootstrap_components as dbc
from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
                dbc.Row([
           dbc.Col(dbc.CardImg(src=app.get_asset_url('/wall_paper.jpg'), className = 'text-center'),
            style={"maxWidth": "100%"})
        ]),
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            # dbc.Col(html.Img(src = '/assets/wall_paper.jpg', height= "500px", className="text-center")),
            dbc.Col(html.H1("Welcome DKIT Suicide dashboard", className="text-center")
                    , className="mb-5 mt-5")            
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This iteration is a deep dive into the suicide dataset to learn much more about the reasons for the thousands of suicides that occur each year around the world. Even though various studies on suicide have already been done previously, such as John et al. (2018), this study aimed to produce new insights that can help government bodies better grasp the problems that lie beneath them. This research could also benefit them in developing new strategies to minimize mortality rates over time. This research will look at a variety of suicide attributes and predict how many more fatalities will occur in various countries in the next years.'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='The goal of this research is to figure out why people commit suicide in each country. Every year, 800,000 individuals commit suicide, according to Wikipedia (2012). Suicide, for example, is becoming a more prevalent and serious problem in India, according to the World Health Organization (WHO). To address these issues, we must examine various patterns and clusters in the data and determine what circumstances cause someone to consider suicide. In addition, a web-based system will be developed that may offer dynamically illuminating visualizations of the suicide dataset, as well as opportunities for page administrators to submit new suicides to the dataset.'
                )
                    , className="mb-5")
        ]),

        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Abount Me',
                                               className="text-center",id='aboutme'),
                                             dbc.Col(html.H5(children='Motivated, teamwork-oriented, and responsible Data Analyst with       significant experience in increasıng Comprehension of report and presentations by the average professional. Highly educated, possessing a Bachelors, a Masters, and 6 years professional         experience in IT. Bilingual in English, Malayalam, and Tamil, with an intermediate understanding of Hindi'
                )
                                     , className="mb-5",style={"minHeight": "100px"}),
                                    dbc.Button("Connect  Sujil Kumar K.M",
                                    href="https://www.linkedin.com/in/sujil/", target="_blank",
                                    # color="primary",
                                    className="mt-3 btn btn-danger"),
                                    
                                       ],
                             
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='About DKIT',
                                               className="text-center"),
                                       dbc.Col(html.H5(children='Dundalk Institute of Technology is an institute of technology based in Dundalk within country Louth, Ireland. Created as Dundalk Regional Technical College, students were first enrolled in the college in 1971 and was later re-defined as an institute of technology in January, 1998.'
                )
                                     , className="mb-5",style={"minHeight": "100px"}),
                                       dbc.Button("Dundalk Institute of Technology (DKIT)",
                                                  href="https://dkit.ie", target="_blank",
                                                  color="primary",
                                                  className="mt-3 btn btn-success"),
                                      
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4")

        ], className="mb-5"),
         dbc.Row([
            # 2 columns of width 6 with a border
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

    ])
    ])

])
])