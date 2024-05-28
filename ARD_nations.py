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
filepath_list = ["./ARD_links/WomenGS/areGS.txt", "./ARD_links/WomenGS/kranjskagoraGS.txt", "./ARD_links/WomenGS/mariborGS.txt", "./ARD_links/WomenGS/soldenGS.txt"]

AreDict = fun.Dict(filepath_list[0])
KranjskaGoraDict = fun.Dict(filepath_list[1])
MariborDict = fun.Dict(filepath_list[2])
SoldenDict = fun.Dict(filepath_list[3])

rename_athlete = {"Name + Surname" : "Athlete"}
list = [AreDict, KranjskaGoraDict, MariborDict, SoldenDict]
Are = pd.DataFrame()
KranjskaGora = pd.DataFrame()
Maribor = pd.DataFrame()
Solden = pd.DataFrame()
list_places = [Are, KranjskaGora, Maribor, Solden]

for element in list:
    for i, df in enumerate(element):
        single_df = f"df_{i}"
        globals()[single_df] = df
        df.rename(columns = rename_athlete, inplace = True)


for df in AreDict:
    Are = pd.concat([Are, df], ignore_index=True)
Are.sort_values(by='season')
print(Are)
fig = px.scatter(Are, x="season", y="Rank", color="Nat", hover_data="Athlete")
fig.show()

#print(AreRaces)


