# iz glavnih csv datotek tekmovalci.csv naredimo več manjših csv datotek
import csv
import pandas as pd

data_drzava = pd.read_csv('tekmovalci.csv', usecols=['to_country_id', 'to_country', 'year'])
data_drzava.rename(columns = {'to_country_id':'kratica_drzave', 'to_country':'ime_drzave', 'year':'leto'}, inplace=True)
data_drzava.to_csv('drzava.csv', index = False)

data_izvajalec = pd.read_csv('tekmovalci.csv', usecols=['to_country', 'performer'])
data_izvajalec.rename(columns = {'to_country':'ime_drzave', 'performer':'ime_izvajalca'}, inplace=True)
data_izvajalec.to_csv('izvajalec.csv', index = False)

data_tekmovanje = pd.read_csv('tekmovalci.csv', usecols=['to_country', 'year'])
data_tekmovanje.rename(columns = {'to_country':'ime_drzave', 'year':'leto'}, inplace=True)
data_tekmovanje.to_csv('tekmovanje.csv', index = False)
# 
data_pesem = pd.read_csv('tekmovalci.csv', usecols=['to_country', 'year', 'song', 'place_contest', 'youtube_url', 'performer', 'points_final'])
data_pesem.rename(columns = {'year':'leto','to_country':'ime_drzave','performer':'ime_izvajalca','song':'naslov_pesmi','place_contest':'mesto','points_final':'tocke_v_finalu','youtube_url':'youtube_link'}, inplace = True)
data_pesem.to_csv('pesem.csv', index = False)
# 
data_glasovi = pd.read_csv('glasovi.csv', usecols=['from_country_id', 'to_country_id','year', 'total_points'])
data_glasovi.rename(columns = {'year':'leto','from_country_id':'kdo','to_country_id':'komu','total_points':'tocke'}, inplace = True)
data_glasovi.to_csv('glasovanje.csv', index = False)

