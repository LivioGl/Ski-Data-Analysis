import pandas as pd #type: ignore
import re
import os
from bs4 import BeautifulSoup #type:ignore
from io import StringIO

def define_position(argument):
  switcher ={
    ".31":31,
    ".32":32,
    ".33":33,
    ".34":34,
    ".35":35,
    ".36":36,
    ".37":37,
    ".38":38,
    ".39":39,
    ".40":40,
    ".41":41,
    ".42":42,
    ".43":43,
    ".44":44,
    ".45":45,
    ".46":46,
    ".47":47,
    ".48":48,
    ".49":49,
    ".50":50,
    ".51":51,
    ".52":52,
    ".53":53,
    ".54":54,
    ".55":55,
    ".56":56,
    ".57":57,
    ".58":58,
    ".59":59,
    ".60":60
  }
  return switcher.get(argument)


races_number_m={
  2023: 26,
  2022: 25,
  2021: 26,
  2020: 27,
  2019: 22,
  2018: 20,
  2017: 25,
  2016: 28,
  2015: 23,
  2014: 21,
  2013: 20,
  2012: 23,
  2011: 34,
  2010: 27,
  2009: 35,
  2008: 38,
  2007: 36,
  2006: 34,
  2005: 36,
  2004: 30,
  2003: 24,
  2002: 24,
  2001: 22,
  2000: 30,
  1999: 30,
  1998: 23,
  1997: 17,
  1996: 26,
  1995: 16,
  1994: 32,
  1993: 31
}

podium_number_m={
  2024: 20,
  2023: 22,
  2022: 16,
  2021: 9,
  2020: 7,
  2019: 15,
  2018: 16,
  2017: 16,
  2016: 19,
  2015: 14,
  2014: 13,
  2013: 18,
  2012: 14,
  2011: 10,
  2010: 10,
  2009: 7,
  2008: 11,
  2007: 8,
  2006: 12,
  2005: 14,
  2004: 9,
  2003: 13,
  2002: 17,
  2001: 15,
  2000: 22,
  1999: 11,
  1998: 19,
  1997: 9,
  1996: 10,
  1995: 11,
  1994: 8,
  1993: 7
}

top10_number_m={
  2024: 24,
  2023: 24,
  2022: 20,
  2021: 19,
  2020: 22,
  2019: 20,
  2018: 19,
  2017: 19,
  2016: 23,
  2015: 18,
  2014: 16,
  2013: 18,
  2012: 17,
  2011: 16,
  2010: 16,
  2009: 16,
  2008: 19,
  2007: 16,
  2006: 19,
  2005: 23,
  2004: 19,
  2003: 16,
  2002: 24,
  2001: 19,
  2000: 25,
  1999: 22,
  1998: 22,
  1997: 17,
  1996: 17,
  1995: 12,
  1994: 24,
  1993: 21
}

races_number_f={
  2023: 31, 2022: 26, 2021: 31, 2020: 25, 2019: 26, 2018: 26, 2017: 25, 2016: 32, 2015: 24, 2014: 24, 2013: 35, 2012: 36, 2011: 33, 2010: 31, 2009: 34, 2008: 33, 2007: 33, 2006: 35, 2005: 32, 2004: 29, 2003: 32, 2002: 27, 2001: 26, 2000: 40, 1999: 30, 1998: 33, 1997: 32, 1996: 33, 1995: 27, 1994: 27, 1993: 31 
}

podium_number_f={
  2023: 18, 2022: 14, 2021: 10, 2020: 11, 2019: 21, 2018: 18, 2017: 14, 2016: 13, 2015: 15, 2014: 11, 2013: 24, 2012: 17, 2011: 16, 2010: 17, 2009: 16, 2008: 10, 2007: 12, 2006: 17, 2005: 11, 2004: 13, 2003: 12, 2002: 10, 2001: 9, 2000: 11, 1999: 13, 1998: 13, 1997: 18, 1996: 13, 1995: 12, 1994: 15, 1993: 9
}

top10_number_f={
  2023: 29, 2022: 22, 2021: 21, 2020: 20, 2019: 26, 2018: 22, 2017: 20, 2016: 20, 2015: 21, 2014: 22, 2013: 32, 2012: 25, 2011: 25, 2010: 20, 2009: 26, 2008: 18, 2007: 21, 2006: 25, 2005: 20, 2004: 18, 2003: 22, 2002: 22, 2001: 15, 2000: 26, 1999: 24, 1998: 22, 1997: 27, 1996: 20, 1995: 18, 1994: 23, 1993: 20
}


def fill_value_f(row):
  if(pd.isna(row['Races'])):
    return races_number_f.get(row['season'], row['Races'])
  return row['Races']

def fill_value_m(row):
  if(pd.isna(row['Races'])):
    return races_number_m.get(row['season'], row['Races'])
  return row['Races']

def update_top3_f(row):
  row['Top3'] = podium_number_f.get(row['season'], row['Top3'])
  return row

def update_top3_m(row):
  row['Top3'] = podium_number_m.get(row['season'], row['Top3'])
  return row

def update_top10_f(row):
  row['Top10'] = top10_number_m.get(row['season'], row['Top10'])
  return row

def update_top10_m(row):
  row['Top10'] = top10_number_m.get(row['season'], row['Top10'])
  return row

def get_season(argument):
  switcher = {
    "2024_": 2024,
    "2023_": 2023,
    "2022_": 2022,
    "2021_": 2021,
    "2020_": 2020,
    "2019_": 2019,
    "2018_": 2018,
    "2017_": 2017,
    "2016_": 2016,
    "2015_": 2015,
    "2014_": 2014,
    "2013_": 2013,
    "2012_": 2012,
    "2011_": 2011,
    "2010_": 2010,
    "2009_": 2009,
    "2008_": 2008,
    "2007_": 2007,
    "2006_": 2006,
    "2005_": 2005,
    "2004_": 2004,
    "2003_": 2003,
    "2002_": 2002,
    "2001_": 2001,
    "2000_": 2000,
    "1999_": 1999,
    "1998_": 1998,
    "1997_": 1997,
    "1996_": 1996,
    "1995_": 1995,
    "1994_": 1994,
    "1993_": 1993
  }
  return switcher.get(argument)
  
Place = {
    "Beaver Creek": 0.2,
    "Bormio": 0.4,
    "Wengen": 0.6,
    "Kitzbuhel": 0.8
  }

def Dict(filepath):
  var = open(filepath, 'r')
  attr = {'id': 'stripedTable1'}
  lines = var.readlines()
  links = []
  for line in lines:
    links.append(line.strip())
  dict = {}
  for i, link in enumerate(links):
    table = pd.read_html(link, attrs = attr)
    data_table = table[0]
    data_table.dropna(inplace=True)
    # Using regular expressions to get the season and add it to df
    pattern = r'/(?P<numeri>\d{2})/'
    match = re.findall(pattern, link)
    season_number = get_season(match[0])
    data_table['season'] = season_number
    dict[f"df_{i}"] = data_table
    keys_list = list(dict.keys())
    values_list = list(dict.values())
  return values_list



def new_dict(dir_path):
  table_class = 'skidb'
  dataframes = []

  for filename in os.listdir(dir_path):
      if filename.endswith('.html'):
          file_path = os.path.join(dir_path, filename)
          # Read HTML file
          with open(file_path, 'r', encoding='utf-8') as file:
                  content = file.read()
          # Analyse HTML content using Beautiful Soup
          soup = BeautifulSoup(content, 'lxml')
          table = soup.find('table', class_=table_class)
          if table:
            # Use StringIO to extract HTML string
            string = StringIO(str(table))
            # Use pandas to read HTML table
            df = pd.read_html(string)[0]
            #df.dropna(inplace=True)
            # Using regular expressions to get the season and add it to df
            pattern = r'\d{4}_'
            match = re.findall(pattern, filename)
            season_number = get_season(match[0])
            df['season'] = season_number
            dataframes.append(df)
  return dataframes


def Dict2(filepath):
  var = open(filepath, 'r')
  attr = {'class': 'skidb'}
  lines = var.readlines()
  links = []
  for line in lines:
    links.append(line.strip())
  dict = {}
  for i, link in enumerate(links):
    table = pd.read_html(link, attrs = attr)
    data_table = table[0]
    data_table["Wins"] = data_table["Wins"].fillna("0")
    data_table["Top3"] = data_table["Wins"].fillna("0")
    data_table["Top10"] = data_table["Wins"].fillna("0")
    data_table["Wins"] = data_table.Wins.astype(float).astype(int)
    # Using regular expressions to get the season and add it to df
    pattern = r'/(?P<numeri>\d{2})/'
    match = re.findall(pattern, link)
    season_number = get_season(match[0])
    data_table['season'] = season_number
    dict[f"df_{i}"] = data_table
    values_list = list(dict.values())
  return values_list

def DeleteData(df):
  count = df.groupby(['season', 'location']).size()
  correct_data = count[count == 2].index
  df = df[df.apply(lambda row: (row['season'], row['location']) in correct_data, axis = 1)]
  return df

    
    