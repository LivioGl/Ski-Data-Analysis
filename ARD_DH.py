import pandas as pd #type: ignore
import plotly.express as px #type: ignore
import ARD_functions as fun #type: ignore
from plotly import data #type: ignore
import dash #type:ignore
import dash_bootstrap_components as dbc #type: ignore
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash.exceptions import CallbackException

from dash.dependencies import Input, Output
from dash import dcc, html, Dash #type: ignore
filepath_list = ["./ARD_links/MenDH/bormio.txt", "./ARD_links/MenDH/beavercreek.txt", "./ARD_links/MenDH/wengen.txt", "./ARD_links/MenDH/kitzbuhel.txt", "./ARD_links/MenSL/campiglioSL.txt"]

# Dictionary with last 10 races in Bormio
Bormio_dict = fun.Dict(filepath_list[0])

# Dictionary with last 10 races in Beaver Creek
BC_dict = fun.Dict(filepath_list[1])

# Dictionary with last 10 races in Wengen
Wengen_dict = fun.Dict(filepath_list[2])

# Dictionary with last 10 races in Kitzbuhel
Kitz_dict = fun.Dict(filepath_list[3])

# Dictionary with last 10 races in Campiglio
Camp_dict = fun.Dict(filepath_list[4])

# pass to the function date of the race and coordinates where it took place
#fun.Data("2023-12-28", 46.4672, 10.3701)
rename_athlete = {"Name + Surname" : "Athlete"}
list = [BC_dict, Bormio_dict, Wengen_dict, Kitz_dict]
for element in list:
    for i, df in enumerate(element):
        single_df = f"df_{i}"
        globals()[single_df] = df
        df.rename(columns = rename_athlete, inplace = True)
            
# ParisVsFeuz = pd.DataFrame()



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

@app.callback(
    dash.dependencies.Output('output-graph', 'children'),
    [Input('button-confirm', 'n_clicks'), Input('location-dropdown', 'value'), Input('athlete-select-1', 'value'), Input('athlete-select-2', 'value')]
)

def update_selected_athletes(n, location, selected_athlete_1, selected_athlete_2):
    if(n is not None and n > 0):
        try: 
            if location == "Beaver Creek":
                Ath1VsAth2 = pd.DataFrame()
                BC = pd.DataFrame()
                for df in BC_dict:
                    df.Athlete.astype(str)
                    mask = ((df['Athlete'] == selected_athlete_1) | (df['Athlete'] == selected_athlete_2))
                    BC = df[mask]
                    Ath1VsAth2 = pd.concat([Ath1VsAth2, BC], ignore_index=True)
                Ath1VsAth2['location'] = location
                Ath1VsAth2 = fun.DeleteData(Ath1VsAth2)
                Ath1VsAth2['season'] = Ath1VsAth2.season.astype(str).astype(int)
                Ath1VsAth2.sort_values(by='season')
                    
            elif location == "Bormio":
                Ath1VsAth2 = pd.DataFrame()
                Bormio = pd.DataFrame()
                for df in Bormio_dict:
                    mask = ((df['Athlete'] == selected_athlete_1) | (df['Athlete'] == selected_athlete_2))
                    Bormio = df[mask]
                    Ath1VsAth2 = pd.concat([Ath1VsAth2, Bormio], ignore_index=True)
                Ath1VsAth2['location'] = location
                Ath1VsAth2 = fun.DeleteData(Ath1VsAth2)
                Ath1VsAth2['season'] = Ath1VsAth2.season.astype(str).astype(int)
                Ath1VsAth2.sort_values(by='season')
                    
            elif location == "Wengen":
                Ath1VsAth2 = pd.DataFrame()
                Wengen = pd.DataFrame()
                for df in Wengen_dict:
                    mask = ((df['Athlete'] == selected_athlete_1) | (df['Athlete'] == selected_athlete_2))
                    Wengen = df[mask]
                    Ath1VsAth2 = pd.concat([Ath1VsAth2, Wengen], ignore_index=True)
                Ath1VsAth2['location'] = location
                Ath1VsAth2 = fun.DeleteData(Ath1VsAth2)
                Ath1VsAth2['season'] = Ath1VsAth2.season.astype(str).astype(int)
                Ath1VsAth2.sort_values(by='season')
                    
            elif location == "Kitzbuhel":
                Ath1VsAth2 = pd.DataFrame()
                Kitz = pd.DataFrame()
                for df in Kitz_dict:
                    mask = ((df['Athlete'] == selected_athlete_1) | (df['Athlete'] == selected_athlete_2))
                    Kitz = df[mask]
                    Ath1VsAth2 = pd.concat([Ath1VsAth2, Kitz], ignore_index=True)
                Ath1VsAth2['location'] = location
                Ath1VsAth2 = fun.DeleteData(Ath1VsAth2)
                Ath1VsAth2['season'] = Ath1VsAth2.season.astype(str).astype(int)
                Ath1VsAth2.sort_values(by='season') 
            mask1 = Ath1VsAth2['Athlete'] == selected_athlete_1
            mask2 = Ath1VsAth2['Athlete'] == selected_athlete_2
            Ath1 = pd.DataFrame()
            Ath2 = pd.DataFrame()
            Ath1 = Ath1VsAth2[mask1]
            Ath2 = Ath1VsAth2[mask2]
            return html.Div(
                style={
                    'width':'800px', 
                    'height':'600px',
                    'justify':'center',
                    'max-width': 'fit-content',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                    },
                children=[
                    html.H1(selected_athlete_1+" vs "+selected_athlete_2),
                    dcc.Graph(
                        id='line-chart',
                        style={'font-size':'25px'},
                        figure={
                            'data': [
                                go.Scatter(
                                    x=Ath1['season'],
                                    y=Ath1['Rank'],
                                    mode='lines+markers',
                                    line=dict(color='red'),
                                    name=selected_athlete_1
                                ),
                                go.Scatter(
                                    x=Ath2['season'],
                                    y=Ath2['Rank'],
                                    mode='lines+markers',
                                    line=dict(color='blue'),
                                    name=selected_athlete_2
                                )
                            ],
                            'layout': go.Layout(
                                title='Confronto tra due atleti',
                                xaxis={'title': 'Stagione',
                                    },
                                yaxis={'title': 'Risultato', 
                                    'showline': False,   # Nasconde la linea dell'asse Y
                                    'showticklabels': False,  # Nasconde le etichette dei tick dell'asse Y
                                    'autorange': 'reversed'},
                            )
                        }
                    )
                ]
            )
        except CallbackException:
            pass
    else:
        raise PreventUpdate
            
athletes = ["Aleksander Aamodt Kilde", "Dominik Paris", "Cyprien Sarrazin", "Niels Hintermann", "Vincent Kriechmayr", "James (Jack) Crawford", "Johan Clarey", "", "Adrien Theaux", "Mattia Casse", "Florian Schieder", "Cameron Alexander", "Ryan Cochran-Siegle", "Nils Allegre", "Stefan Babinsky", "Maxence Muzaton", "Bryce Bennett", "Andreas Sander"]

app.layout = html.Div(
    style={'text-align':'center', 'margin-top':'25px'},  # Centra gli elementi all'interno del div
    children=[
        html.H1("Compare two athletes", style={'font-size':'25px'}),
        html.Div(
            style={'width': '50%', 'margin': 'auto', 'margin-top':'15px'},
            children = [
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id='location-dropdown',
                            options=[
                                {'label': 'Beaver Creek', 'value':'Beaver Creek'},
                                {'label': 'Bormio', 'value':'Bormio'},
                                {'label': 'Wengen', 'value':'Wengen'},
                                {'label': 'Kitzbuhel', 'value':'Kitzbuhel'}
                            ],
                            value='option1'
                        )
                    )
                ],
                className="mt-4",
                justify="center"
                ),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id='athlete-select-1',
                            options=[{'label' : athlete, 'value': athlete} for athlete in athletes],
                        )
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='athlete-select-2',
                            options=[{'label' : athlete, 'value': athlete} for athlete in athletes],
                        )
                    )
                ],
                className="mt-4",
                justify="center"
                ),
                dbc.Row(
                    dbc.Button(
                        "Calculate Graph", 
                        outline=True, 
                        color="success", 
                        className="me-1", 
                        id='button-confirm', 
                        n_clicks=0
                    ),
                    className="mt-4",
                    justify="center"
                )
            ]
        ),
        html.Div(
            style={'width': '50%', 'margin': 'auto'},  # Imposta la larghezza del div e lo centra
            children=[
                html.Div(
                    style={'max-width': 'fit-content','margin-left': 'auto','margin-right': 'auto'},
                    id='output-graph'
                )
            ]
        )
    ]
)
app.run_server(debug=True)