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
    WomenWinners['Avg_Points_per_race'] = WomenWinners['Points'] / WomenWinners['Races']
    WomenWinners['Avg_Points_per_race'] = WomenWinners['Avg_Points_per_race'].round(3)
    WomenWinners['WinRate'] = WomenWinners['Wins'] / WomenWinners['Races']
    WomenWinners['PodiumRate'] = WomenWinners['Top3'] / WomenWinners['Races']
WomenWinners.drop(columns=['Rank'], inplace=True)

# print(MenWinners)
# print(WomenWinners)
custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5', '#ff7f0e', 
    '#ffbb78', '#ff9896', '#c49c94', '#98df8a', '#aec7e8', '#ff7f0e', '#d62728', '#2ca02c', '#9467bd', '#8c564b', '#e377c2'
]
fig = px.scatter(MenWinners, x='season', y='Points', color='Athlete', color_discrete_sequence=px.colors.qualitative.D3, size='Wins', hover_data={'Wins':True, 'Top3':True, 'Athlete':True}, width=800, height=500)
# fig2 = px.bar(MenWinners, x='season', y='Points', color='Nat', width=800, height=500)
# fig3 = px.bar(MenWinners, x='season', y='WinRate', color='Athlete', width=800, height=500)
fig.show()
