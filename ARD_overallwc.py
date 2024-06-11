import pandas as pd #type: ignore
import plotly.express as px #type: ignore
import ARD_functions as fun #type: ignore
from plotly import data #type: ignore
import dash #type:ignore
import dash_bootstrap_components as dbc #type: ignore
import plotly.graph_objs as go #type:ignore
from dash.exceptions import PreventUpdate #type:ignore
from dash.exceptions import CallbackException #type:ignore

from dash.dependencies import Input, Output #type:ignore
from dash import dcc, html, Dash #type: ignore

men_dir_path = './links/men'
women_dir_path = './links/women'
Men = fun.new_dict(men_dir_path)

rename_athlete = {"Name + Surname" : "Athlete"}
for i, df in enumerate(Men):
        single_df = f"df_{i}"
        globals()[single_df] = df
        df.rename(columns = rename_athlete, inplace = True)

MenWinners = pd.DataFrame()
for df in Men:
    distance_from_2nd = df.loc[df["Rank"] == 1, "Points"].values[0] - df.loc[df["Rank"] == 2, "Points"].values[0]
    df["distance from 2nd"] = distance_from_2nd
    main_opponent = df.loc[df["Rank"] == 2, 'Athlete'].values[0]
    df["main_opponent"] = main_opponent
    tmp = df[df["Rank"] == 1]
    MenWinners = pd.concat([MenWinners, tmp], ignore_index=True)

MenWinners['Races'] = MenWinners.apply(fun.fill_value_m, axis=1)
MenWinners = MenWinners.apply(fun.update_top3_m, axis=1)
MenWinners = MenWinners.apply(fun.update_top10_m, axis=1)

for element in MenWinners:
    MenWinners['Races'] = MenWinners.Races.astype(int)
    MenWinners['Wins'] = MenWinners.Wins.astype(int)
    MenWinners['Top3'] = MenWinners.Top3.astype(int)
    MenWinners['Avg_Points_per_race'] = MenWinners['Points'] / MenWinners['Races']
    MenWinners['Avg_Points_per_race'] = MenWinners['Avg_Points_per_race'].round(3)
    MenWinners['WinRate'] = MenWinners['Wins'] / MenWinners['Races']
    MenWinners['PodiumRate'] = MenWinners['Top3'] / MenWinners['Races']
MenWinners.drop(columns=['Rank'], inplace=True)

Women = fun.new_dict(women_dir_path)

for i, df in enumerate(Women):
        single_df = f"df_{i}"
        globals()[single_df] = df
        df.rename(columns = rename_athlete, inplace = True)

WomenWinners = pd.DataFrame()
for df in Women:
    tmp = pd.DataFrame()
    distance_from_2nd = df.loc[df["Rank"] == 1, "Points"].values[0] - df.loc[df["Rank"] == 2, "Points"].values[0]
    df["distance from 2nd"] = distance_from_2nd
    main_opponent = df.loc[df["Rank"] == 2, 'Athlete'].values[0]
    df["main_opponent"] = main_opponent
    tmp = df[df["Rank"] == 1]
    WomenWinners = pd.concat([WomenWinners, tmp], ignore_index=True)

WomenWinners['Races'] = WomenWinners.apply(fun.fill_value_f, axis=1)
WomenWinners = WomenWinners.apply(fun.update_top3_f, axis=1)
WomenWinners = WomenWinners.apply(fun.update_top10_f, axis=1)

for element in WomenWinners:
    WomenWinners['Races'] = WomenWinners.Races.astype(int)
    WomenWinners['Wins'] = MenWinners.Wins.astype(int)
    WomenWinners['Top3'] = MenWinners.Top3.astype(int)
    WomenWinners['Avg_Points_per_race'] = WomenWinners['Points'] / WomenWinners['Races']
    WomenWinners['Avg_Points_per_race'] = WomenWinners['Avg_Points_per_race'].round(3)
    WomenWinners['WinRate'] = WomenWinners['Wins'] / WomenWinners['Races']
    WomenWinners['PodiumRate'] = WomenWinners['Top3'] / WomenWinners['Races']
WomenWinners.drop(columns=['Rank'], inplace=True)

custom_colors = ['#0000FF', '#607D3B', '#FF0000', '#FFD700', '#FF00FF', '#99CBFF', '#00FF00', '#800000', '#808000', '#800080',
    '#008080', '#020181', '#03C04A', '#E5BE01', '#FFC0CB', '#B57FDD', '#6A76FC', '#FF9900']
# print(MenWinners)
# print(WomenWinners)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# @app.callback(
#     Output("output_graph_men", 'figure'),
#     Input('select_parameter_men', 'value')
# )
@app.callback(
    Output('graph_men', 'figure'),
    [Input('select_parameter_men', 'value')]
)
# def choose_parameter_men(selected_parameter_men):
#     if(selected_parameter_men == 'distance from 2nd'):
#         return px.bar(MenWinners, x='season', y='distance from 2nd', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'distance from 2nd': True}, width=550, height=450)
#     elif(selected_parameter_men == 'Avg points per race'):
#         return px.bar(MenWinners, x='season', y='Avg_Points_per_race', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'Avg_Points_per_race':True}, width=550, height=450)
#     elif(selected_parameter_men == 'Win Rate'):
#         return px.bar(MenWinners, x='season', y='WinRate', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'WinRate':True}, width=550, height=450)
#     else:
#         return px.bar(MenWinners, x='season', y='PodiumRate', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'PodiumRate':True}, width=550, height=450)
def choose_parameter_men(selected_parameter_men):
    if selected_parameter_men == 'distance from 2nd':
        fig = px.bar(MenWinners, x='season', y='distance from 2nd', color='Athlete',
                        color_discrete_sequence=custom_colors,
                        hover_data={'Wins': True, 'distance from 2nd': True})
    elif selected_parameter_men == 'Avg points per race':
        fig = px.bar(MenWinners, x='season', y='Avg_Points_per_race', color='Athlete',
                     color_discrete_sequence=custom_colors,
                     hover_data={'Wins': True, 'Avg_Points_per_race': True})
    elif selected_parameter_men == 'Win Rate':
        fig = px.bar(MenWinners, x='season', y='WinRate', color='Athlete',
                     color_discrete_sequence=custom_colors,
                     hover_data={'Wins': True, 'WinRate': True})
    else:
        fig = px.bar(MenWinners, x='season', y='PodiumRate', color='Athlete',
                     color_discrete_sequence=custom_colors,
                     hover_data={'Wins': True, 'PodiumRate': True})
    
    # Aggiornamento del layout per ridurre la dimensione della legenda
    fig.update_layout(
        legend=dict(
            font=dict(size=10),
            itemsizing='constant'  # Riduce anche la dimensione dei quadratini della legenda
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(255, 255, 255, 0.8)',  
        paper_bgcolor='rgba(255, 255, 255, 0.5)' 
    )
    return fig


@app.callback(
    Output("graph_women", 'figure'),
    Input('select_parameter_women', 'value')
)

def choose_parameter_women(selected_parameter_women):
    if selected_parameter_women == 'distance from 2nd':
        fig = px.bar(WomenWinners, x='season', y='distance from 2nd', color='Athlete',
                        color_discrete_sequence=custom_colors,
                        hover_data={'Wins': True, 'distance from 2nd': True})
    elif selected_parameter_women == 'Avg points per race':
        fig = px.bar(WomenWinners, x='season', y='Avg_Points_per_race', color='Athlete',
                     color_discrete_sequence=custom_colors,
                     hover_data={'Wins': True, 'Avg_Points_per_race': True})
    elif selected_parameter_women == 'Win Rate':
        fig = px.bar(WomenWinners, x='season', y='WinRate', color='Athlete',
                     color_discrete_sequence=custom_colors,
                     hover_data={'Wins': True, 'WinRate': True})
    else:
        fig = px.bar(WomenWinners, x='season', y='PodiumRate', color='Athlete',
                     color_discrete_sequence=custom_colors,
                     hover_data={'Wins': True, 'PodiumRate': True})
    
    # Aggiornamento del layout per ridurre la dimensione della legenda
    fig.update_layout(
        legend=dict(
            font=dict(size=10),
            itemsizing='constant'  # Riduce anche la dimensione dei quadratini della legenda
        ),
        margin=dict(l=20, r=20, t=20, b=20),  # Imposta margini piccoli per un migliore adattamento
        plot_bgcolor='rgba(255, 255, 255, 0.8)',  # Colore di sfondo del grafico con trasparenza
        paper_bgcolor='rgba(255, 255, 255, 0.5)',
        
    )
    return fig


# def choose_parameter_women(selected_parameter_women):
#     if(selected_parameter_women == 'distance from 2nd'):
#         return px.bar(WomenWinners, x='season', y='distance from 2nd',color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'distance from 2nd': True}, width=550, height=450)
#     elif(selected_parameter_women == 'Avg points per race'):
#         return px.bar(WomenWinners, x='season', y='Avg_Points_per_race', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'Avg_Points_per_race': True}, width=550, height=450)
#     elif(selected_parameter_women == 'Win Rate'):
#         return px.bar(WomenWinners, x='season', y='WinRate', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'WinRate': True}, width=550, height=450)
#     else:
#         return px.bar(WomenWinners, x='season', y='PodiumRate', color='Athlete', color_discrete_sequence = custom_colors, hover_data={'Wins':True, 'PodiumRate': True}, width=550, height=450)
bg_img = 'bg_img.jpg'
app.layout = html.Div(
    style={
        'background-image': f'url("/assets/{bg_img}")',
        'background-size': 'cover',
        'background-position': 'center',
        'background-repeat': 'no-repeat',
        'height': '100vh',
    },
    children=[
        dbc.Container([
            dbc.Row([
                html.H1("Ski Data: Overall World Cup Winners", style={'text-align':'center','font-size':'30px', 'color':'white'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.H1("Men", style={'text-align':'center', 'font-size':'20px', 'color':'white'})
                ),
                dbc.Col(
                    html.H1("Women", style={'text-align':'center', 'font-size':'20px', 'color':'white'})                    
                )
            ], style={'color':'white'}),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='select_parameter_men',
                        options=[
                            {'label': 'Distance from 2nd', 'value': 'distance from 2nd'},
                            {'label': 'Avg points per race', 'value': 'Avg points per race'},
                            {'label': 'Win Rate', 'value': 'Win Rate'},
                            {'label': 'Podium Rate', 'value': 'PodiumRate'}
                        ],
                        value='distance from 2nd'
                    ),
                    html.Div(
                        dcc.Graph(id='graph_men'),
                        style={'width': '100%', 'height': '100%', 'display': 'inline-block'}
                    )
                ], style={'width': '50%', 'display': 'inline-block'}),
                dbc.Col([
                    dcc.Dropdown(
                        id='select_parameter_women',
                        options=[
                            {'label': 'Distance from 2nd', 'value': 'distance from 2nd'},
                            {'label': 'Avg points per race', 'value': 'Avg points per race'},
                            {'label': 'Win Rate', 'value': 'Win Rate'},
                            {'label': 'Podium Rate', 'value': 'PodiumRate'}
                        ],
                        value='distance from 2nd'
                    ),
                    html.Div(
                        dcc.Graph(id='graph_women'),
                        style={'width': '100%', 'height': '100%', 'display': 'inline-block'}
                    )
                ]) 
            ])
        ],  fluid=True)]
)

# app.layout = html.Div(
#     style={},
#     children=[
#          html.H1("Ski Data: Overall World Cup Winners", style={'text-align':'center','font-size':'30px'}),
#          dbc.Container(
#               children=[
#                    dbc.Row([
#                         dbc.Col(
#                             html.H1("Men", style={'text-align':'center', 'font-size':'20px'}),
#                             className="my-0"
#                         ),
#                         dbc.Col(
#                             html.H1("Women", style={'text-align':'center', 'font-size':'20px'}),
#                             className="my-0"                          
#                         ),
#                    ]),
#                    dbc.Row([
#                         dbc.Col(
#                              children=[
#                                 html.P("Choose a parameter: ", style={'font-size':'15px'}, className="mx-2"),
#                                 dcc.Dropdown(
#                                     id='select_parameter_men',
#                                     options=[
#                                         {'label':'distance from 2nd', 'value': 'distance from 2nd'},
#                                         {'label':'Avg points per race', 'value':'Avg points per race'},
#                                         {'label':'Win Rate', 'value': 'Win Rate'},
#                                         {'label':'Podium Rate', 'value': 'Podium Rate'}
#                                     ],
#                                     style={'width':'50%'},
#                                     className="mr-2"
#                                 )
#                                 ],
#                                 className="d-flex justify-content-center my-0",
#                                 style={'padding':'5px'}
#                         ), 
#                         dbc.Col(
#                             children=[
#                                 html.P("Choose a parameter: ", style={'font-size':'15px'}, className="mx-2"),
#                                 dcc.Dropdown(
#                                     id='select_parameter_women',
#                                     options=[
#                                         {'label':'distance from 2nd', 'value': 'distance from 2nd'},
#                                         {'label':'Avg points per race', 'value':'Avg points per race'},
#                                         {'label':'Win Rate', 'value': 'Win Rate'},
#                                         {'label':'Podium Rate', 'value': 'Podium Rate'}
#                                     ],
#                                     style={'width':'50%'},
#                                     className="mr-2"
#                                 )
#                             ],
#                             className="d-flex justify-content-center my-0"
#                         )
#                    ]),
#                    dbc.Row([
#                         dbc.Col(
#                             children=[
#                                 dcc.Graph(id="output_graph_men")
#                             ],
#                             className="my-0"
#                         ),
#                         dbc.Col(
#                             children=dcc.Graph(id="output_graph_women"),
#                             className="my-0"
#                         )
#                    ], className="d-flex justify-content-center")
#               ], fluid=True
#          )
#     ]
# )


# fig = px.scatter(MenWinners, x='season', y='Points', color='Athlete', color_discrete_sequence=px.colors.qualitative.D3, size='Wins', hover_data={'Wins':True, 'Top3':True, 'Athlete':True}, width=800, height=500)
# # fig2 = px.bar(MenWinners, x='season', y='Points', color='Nat', width=800, height=500)
# # fig3 = px.bar(MenWinners, x='season', y='WinRate', color='Athlete', width=800, height=500)
# fig.show()
app.run_server(debug=True)