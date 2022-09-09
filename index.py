from dash import dcc
from dash import html
from app import server
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
# from app import server
from app import app
from app import server
# import all pages in the app
from apps import dashboard, forecast1, overview, policy, home, data, outliers

# building the navigation bar
dropdown = dbc.DropdownMenu(
    children=[
        # dcc.Link("Game", href="/apps/game"),
        dbc.DropdownMenuItem("Dashboard", href="/dashboard"),
        dbc.DropdownMenuItem("Overview", href="/overview"),
        dbc.DropdownMenuItem("Forecast Model", href="/forecast1"),
        dbc.DropdownMenuItem("Data View", href="/data"),
        dbc.DropdownMenuItem("Data Integrity", href="/outliers"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore Pages",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/dkit_logo.png", height="60px")),
                        dbc.Col(dbc.NavbarBrand("Suicide Analysis Dashboard", className="ml-2")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
            html.A(dbc.Row(
                    [                        
                        dbc.DropdownMenuItem("About Us", className="ml-2"),
                    ],
                    align="center",
                ),href="/home#aboutme",),
                 html.A(dbc.Row(
                    [                        
                        dbc.DropdownMenuItem("Privacy Policy", className="ml-2"),
                    ],
                    align="center",
                ),href="/policy",),
        ]
    ),sticky="top",
    color="dark",
    dark=True,
    className="mb-4",
)
row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
            ]
        ),
    ]
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output("navbar-collapse"+str(i),"is_open"),
        [Input("navbar-toggler"+str(i),"n_clicks")],
        [State("navbar-collapse"+str(i),"is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/policy':
        return policy.layout
    elif pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/overview':
        return overview.layout
    elif pathname == '/forecast1':
        return forecast1.layout
    elif pathname == '/data':
        return data.layout
    elif pathname == '/outliers':
        return outliers.layout
    
    else:
        return home.layout


if __name__ != '__main__':
    pass
else:
    app.run_server(port=8008, debug=True)