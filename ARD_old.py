import pandas as pd #type: ignore
import plotly.express as px #type: ignore
import ARD_functions as fun #type: ignore
file_path = 'data.txt'
f = open(file_path, 'r')
attr = {'id': 'stripedTable1'}
# Saving all links in a list
lines = f.readlines()
links = []
for line in lines:
  links.append(line.strip())

#SL FILTER
SL_links = [link for link in links if '520' in link]
#GS FILTER
GS_links = [link for link in links if '320' in link]
#SG FILTER
SG_links = [link for link in links if '720' in link]
#DH FILTER
DH_links = [link for link in links if '120' in link]


# Men's Slalom 2024 Season
GurglSL = pd.read_html(SL_links[0], attrs = attr)
Gurgl_SL_M_2023 = GurglSL[0]

ValIsereSL = pd.read_html(SL_links[1], attrs = attr)
Val_d_Isere_SL_M_2023 = ValIsereSL[0]

CampiglioSL = pd.read_html(SL_links[2], attrs = attr)
Campiglio_SL_M_2023 = CampiglioSL[0]

AdelbodenSL = pd.read_html(SL_links[3], attrs = attr)
Adelboden_SL_M_2024 = AdelbodenSL[0]

WengenSL = pd.read_html(SL_links[4], attrs = attr)
Wengen_SL_M_2024 = WengenSL[0]

KitzbuhelSL = pd.read_html(SL_links[5], attrs = attr)
Kitzbuhel_SL_M_2024 = KitzbuhelSL[0]

SchladmingSL = pd.read_html(SL_links[6], attrs = attr)
Schladming_SL_M_2024 = SchladmingSL[0]

ChamonixSL = pd.read_html(SL_links[7], attrs = attr)
Chamonix_SL_M_2024 = ChamonixSL[0]

BanskoSL = pd.read_html(SL_links[8], attrs = attr)
Bansko_SL_M_2024 = BanskoSL[0]

PTahoeSL = pd.read_html(SL_links[9], attrs = attr)
PTahoe_SL_M_2024 = PTahoeSL[0]

AspenSL = pd.read_html(SL_links[10], attrs = attr)
Aspen_SL_M_2024 = AspenSL[0]

KranjskaGoraSL = pd.read_html(SL_links[11], attrs = attr)
KranjskaGora_SL_M_2024 = KranjskaGoraSL[0]

SaalbachSL = pd.read_html(SL_links[12], attrs = attr)
Saalbach_SL_M_2024 = SaalbachSL[0]

All_SL_races_2024 = [Gurgl_SL_M_2023, Val_d_Isere_SL_M_2023, Campiglio_SL_M_2023, Adelboden_SL_M_2024, Wengen_SL_M_2024, Kitzbuhel_SL_M_2024, Schladming_SL_M_2024, Chamonix_SL_M_2024, Bansko_SL_M_2024, PTahoe_SL_M_2024, Aspen_SL_M_2024, KranjskaGora_SL_M_2024, Saalbach_SL_M_2024]
#print(Aspen_SL_M_2024)
rename_athlete = {"Name + Surname" : "Athlete"}
for race in All_SL_races_2024:
   race.rename(columns = rename_athlete, inplace = True)


# All Feller's races
SL_races = list(filter(lambda race: not race.empty, All_SL_races_2024))
Feller_SL_Races = pd.DataFrame()
for race in SL_races:
   Feller_mask = race['Athlete'] == "Manuel Feller"
   FM = pd.DataFrame()
   FM = (race[Feller_mask])
   Feller_SL_Races= pd.concat([Feller_SL_Races, FM], ignore_index=True)
Feller_SL_Races['Rank'] = Feller_SL_Races['Rank'].astype(str).astype(int)
Feller_SL_Wins = fun.WinCount(Feller_SL_Races)
Feller_Win_Rate = fun.WinRate(Feller_SL_Wins, len(Feller_SL_Races))
#print("Nella stagione 2023/24, Manuel Feller ha registrato una Win Rate pari a "+str(Feller_Win_Rate)+", vincendo "+str(Feller_SL_Wins)+" gare su "+str(len(Feller_SL_Races))+" disputate")
fig = px.bar(Feller_SL_Races, y='Rank', width=1000, height=500)
#fig.show()

#Material Stats: SL races Season 23/24
for df in All_SL_races_2024:
   df.dropna(inplace=True)
   df.Rank = df.Rank.astype(str).astype(int)

SL_Winners = pd.DataFrame()
for df in All_SL_races_2024:
   win_mask = df['Rank'] == 1
   SM = pd.DataFrame()
   SM = df[win_mask]
   SL_Winners = pd.concat([SL_Winners, SM], ignore_index = True)
print(SL_Winners)
figs = []
fig1 = px.pie(SL_Winners, title='Constructor wins', width=800, height=500, names='Nat')
fig2 = px.pie(SL_Winners, title='Constructor wins', width=800, height=500, names='Skis')
figs = [fig1, fig2]
#for fig in figs:
   #fig.show()

# Calcolare Podium Rate e Win Rate per tutti gli atleti che hanno concluso almeno una volta sul podio

# CALCOLO DEI PODI STAGIONALE
All_SL_Podiums = pd.DataFrame()
for race in All_SL_races_2024:
   race.Athlete = race.Athlete.astype(str)
   race.Skis = race.Skis.astype(str)
   podium_mask = (race['Rank'] <= 3)
   TempDataFrame = race[podium_mask]
   All_SL_Podiums = pd.concat([All_SL_Podiums, TempDataFrame], ignore_index=True)
Podium_Athletes = All_SL_Podiums["Athlete"]#.value_counts()
print(Podium_Athletes)

# Podi totali per materiali
Podium_Num = All_SL_Podiums["Skis"]#.value_counts()
print("Numero di podi in base alla marca di sci: ")
print(Podium_Num)
#fig_materials = px.pie(Podium_Num, title='Constructor Podiums', width=800, height=500, names='Skis')
#fig_materials.show()

sunburst = px.sunburst(All_SL_Podiums, path=["Skis", "Nat", "Athlete"], width=800, height=600, title="Podium in SL, season 2023-24")
sunburst.show()

# Podi totali per nazioni
Podium_Nat_Num = All_SL_Podiums["Nat"].value_counts()
print("Numero di podi in base alla nazione: ")
print(Podium_Nat_Num)

tmp = Podium_Athletes.tolist()
list_pdms = []
for element in tmp:
   if element not in list_pdms:
      list_pdms.append(element)
#print(list_pdms)