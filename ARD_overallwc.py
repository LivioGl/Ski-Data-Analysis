import pandas as pd #type: ignore
import plotly.express as px #type: ignore
import ARD_functions as fun #type: ignore
from plotly import data #type: ignore
import dash #type:ignore
import dash_bootstrap_components as dbc #type: ignore
import plotly.graph_objs as go #type:ignore
from dash.exceptions import PreventUpdate #type:ignore
from dash.exceptions import CallbackException #type:ignore

from dash.dependencies import Input, Output, State #type:ignore
from dash import dcc, html, Dash #type: ignore

bg_img = 'bg_img.jpg'
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
    MenWinners['Athlete'] = MenWinners.Athlete.astype("string").astype(str)
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
    WomenWinners['Athlete'] = WomenWinners.Athlete.astype("string").astype(str)
    WomenWinners['Wins'] = MenWinners.Wins.astype(int)
    WomenWinners['Top3'] = MenWinners.Top3.astype(int)
    WomenWinners['Avg_Points_per_race'] = WomenWinners['Points'] / WomenWinners['Races']
    WomenWinners['Avg_Points_per_race'] = WomenWinners['Avg_Points_per_race'].round(3)
    WomenWinners['WinRate'] = WomenWinners['Wins'] / WomenWinners['Races']
    WomenWinners['PodiumRate'] = WomenWinners['Top3'] / WomenWinners['Races']
WomenWinners.drop(columns=['Rank'], inplace=True)

MenSunburst = MenWinners.copy()
MenSunburst['Athlete'] = MenSunburst['Athlete'].apply(lambda x: x[:-4] if isinstance(x, str) else x)

WomenSunburst = WomenWinners.copy()
WomenSunburst['Athlete'] = WomenSunburst['Athlete'].apply(lambda x: x[:-4] if isinstance(x, str) else x)

# Colors used in the barchartss
custom_colors = ['#0000FF', '#607D3B', '#FF0000', '#FFD700', '#FF00FF', '#99CBFF', '#00FF00', '#800000', '#808000', '#800080',
    '#008080', '#020181', '#03C04A', '#E5BE01', '#FFC0CB', '#B57FDD', '#6A76FC', '#FF9900']

sun1 = px.sunburst(MenSunburst, path=['Nat', 'Athlete', 'Points'], values='season')
sun2 = px.sunburst(WomenSunburst, path=['Nat', 'Athlete', 'Points'], values='season')

sun1.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),  
        plot_bgcolor='rgba(255, 255, 255, 0.8)',  
        paper_bgcolor='rgba(255, 255, 255, 0.5)'
)
sun2.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),  
        plot_bgcolor='rgba(255, 255, 255, 0.8)',  
        paper_bgcolor='rgba(255, 255, 255, 0.5)'
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


@app.callback(
    Output('graph_men', 'figure'),
    [Input('select_parameter_men', 'value')]
)

def choose_parameter_men(selected_parameter_men):
    if selected_parameter_men == 'distance from 2nd':
        fig = px.bar(MenWinners, x='season', y='distance from 2nd', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'distance from 2nd': True})
    elif selected_parameter_men == 'Avg points per race':
        fig = px.bar(MenWinners, x='season', y='Avg_Points_per_race', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'Avg_Points_per_race': True})
    elif selected_parameter_men == 'Win Rate':
        fig = px.bar(MenWinners, x='season', y='WinRate', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'WinRate': True})
    else:
        fig = px.bar(MenWinners, x='season', y='PodiumRate', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'PodiumRate': True})
    
    # Adding layout css properties: legend colors, plot border, bg color, border color and plot border shape
    fig.update_layout(
        legend=dict(
            font=dict(size=10, color='black'),
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0.8)',  
            bordercolor='black',        
            borderwidth=2  # 
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(255, 255, 255, 0.8)', 
        paper_bgcolor='rgba(255, 255, 255, 0.3)',
        xaxis=dict(
            title_font=dict(size=10, color='white'),  
            tickfont=dict(size=10, color='white')
        ),
        yaxis=dict(
            title_font=dict(size=10, color='white'),
            tickfont=dict(size=10, color='white')
        ),
        shapes=[  
            dict(
                type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1,
                line=dict(
                    color="black",
                    width=2,
                )
            )
        ]
    )    
    return fig

@app.callback(
    Output("graph_women", 'figure'),
    Input('select_parameter_women', 'value')
)

def choose_parameter_women(selected_parameter_women):
    if selected_parameter_women == 'distance from 2nd':
        fig = px.bar(WomenWinners, x='season', y='distance from 2nd', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'distance from 2nd': True})
    elif selected_parameter_women == 'Avg points per race':
        fig = px.bar(WomenWinners, x='season', y='Avg_Points_per_race', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'Avg_Points_per_race': True})
    elif selected_parameter_women == 'Win Rate':
        fig = px.bar(WomenWinners, x='season', y='WinRate', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'WinRate': True})
    else:
        fig = px.bar(WomenWinners, x='season', y='PodiumRate', color='Athlete', color_discrete_sequence=custom_colors, hover_data={'Wins': True, 'PodiumRate': True})
    
    fig.update_layout(
        legend=dict(
            font=dict(size=10, color='black'),
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0.8)',  
            bordercolor='black',   
            borderwidth=2
        ),
        margin=dict(l=20, r=20, t=20, b=20),  
        plot_bgcolor='rgba(255, 255, 255, 0.8)',  
        paper_bgcolor='rgba(255, 255, 255, 0.3)',
        xaxis=dict(
            title_font=dict(size=12, color='white'), 
            tickfont=dict(size=10, color='white')
        ),
        yaxis=dict(
            title_font=dict(size=12, color='white'),
            tickfont=dict(size=10, color='white')
        ),
        shapes=[  
            dict(
                type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1,
                line=dict(
                    color="black",
                    width=2,
                ),
            )
        ]
    )
    return fig

def main_layout():
    return html.Div(
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
                    dbc.ButtonGroup([
                        dbc.Button("Nations", id="btn-line-plot", color="primary", className="mt-3", size='sm'),
                        dbc.Button("Individual", id="btn-back-main", color="primary", className="mt-3", size='sm')
                    ])
                ], className="d-flex justify-content-center"),
                dbc.Row([
                    dbc.Col(
                        html.H1("Men", style={'text-align':'center', 'font-size':'15px', 'color':'white'})
                    ),
                    dbc.Col(
                        html.H1("Women", style={'text-align':'center', 'font-size':'15px', 'color':'white'})                    
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
                            style={'width': '100%', 'height': '95%'}
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
                            style={'width': '100%', 'height': '95%'}
                        )
                    ], style={'width': '50%', 'display': 'inline-block'}) 
                ], className="d-flex justify-content-center")
            ],  fluid=True)]
)

def second_layout():
    return html.Div(
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
                    html.H1("Overall World Cup Winners and their nations", style={'text-align':'center','font-size':'30px', 'color':'white'})
                ]),
                dbc.Row([
                    dbc.ButtonGroup([
                        dbc.Button("Nations", id="btn-line-plot", color="primary", className="mt-3", size='sm'),
                        dbc.Button("Individual", id="btn-back-main", color="primary", className="mt-3", size='sm')
                    ], className='mr-2')
                ]),
                dbc.Row([
                    dbc.Col(
                        html.H1("Men", style={'text-align':'center', 'font-size':'15px', 'color':'white'})
                    ),
                    dbc.Col(
                        html.H1("Women", style={'text-align':'center', 'font-size':'15px', 'color':'white'})                    
                    )
                ], style={'color':'white'}),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(figure=sun1)
                    ]),
                    dbc.Col([
                        dcc.Graph(figure=sun2)
                    ])
                ], 
                className="d-flex justify-content-center"),
            ], fluid=True)]
)

app.layout = html.Div(id='page-content', children=main_layout())

#Callback to set the navigation between two sides
@app.callback(
    Output('page-content', 'children'),
    [Input('btn-line-plot', 'n_clicks'),
    Input('btn-back-main', 'n_clicks')],
    [State('page-content', 'children')]
)

def display_page(btn_line, btn_back, current_layout):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_layout
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'btn-line-plot':
            return second_layout()
        elif button_id == 'btn-back-main':
            return main_layout()
        else:
            return current_layout

app.run_server(debug=True)
