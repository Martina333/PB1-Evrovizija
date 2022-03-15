#pridobivanje podatkov s spleta

import requests
import re
import pandas as pd

url = 'https://github.com/Spijkervet/eurovision_dataset/releases/download/2020.0/contestants.csv'
url2 = 'https://github.com/Spijkervet/eurovision_dataset/releases/download/2020.0/votes.csv'
req = requests.get(url)
req2 = requests.get(url2)
url_content = req.content
url_content2 = req2.content
csv_file = open('tekmovalci.csv', 'wb')
csv_file2 = open('glasovi.csv', 'wb')
csv_file.write(url_content)
csv_file2.write(url_content2)
csv_file.close()
csv_file2.close()

df = pd.read_csv('tekmovalci.csv')
odrezi = df.drop("composers",axis=1,inplace=True)
odrezi2 = df.drop("lyricists", axis=1,inplace=True)
odrezi3 = df.drop("lyrics", axis=1,inplace=True)

# df.rename(columns={"year": "leto"}, inplace=True)
# df.rename(columns={"to_country_id": "kratica_drzav"}, inplace=True)
# df.rename(columns={"to_country": "drzava"}, inplace=True)
# df.rename(columns={"performer": "izvajalec"}, inplace=True)
# df.rename(columns={"song": "naziv_pesmi"}, inplace=True)
# df.rename(columns={"place_contest": "koncna_uvrstitev"}, inplace=True)
# df.rename(columns={"sf_num": "prvo/drugo_polfinale"}, inplace=True)
# df.rename(columns={"running_final": "zaporedna_stevilka_v_finalu"}, inplace=True)
# df.rename(columns={"running_sf": "zaporedna_stevilka_v_polfinalu"}, inplace=True)
# df.rename(columns={"place_final": "koncna_uvrstitev_v_finalu"}, inplace=True)
# df.rename(columns={"points_final": "tocke_v_finalu"}, inplace=True)
# df.rename(columns={"place_sf": "koncna_uvrstitev_v_polfinalu"}, inplace=True)
# df.rename(columns={"points_sf": "tocke_v_polfinalu"}, inplace=True)
# df.rename(columns={"points_tele_final": "skupne_tocke_obcinstva_v_finalu"}, inplace=True)
# df.rename(columns={"points_jury_final": "skupne_tocke_zirije_v_finalu"}, inplace=True)
# df.rename(columns={"points_tele_sf": "skupne_tocke_obcinstva_v_polfinalu"}, inplace=True)
# df.rename(columns={"points_jury_sf": "skupne_tocke_zirije_v_finalu"}, inplace=True)
# 
# 
# tocke = pd.read_csv('glasovi.csv')
# tocke.rename(columns={"year": "leto"}, inplace=True)
# tocke.rename(columns={"round": "krog"}, inplace=True)
# tocke.rename(columns={"from_country_id": "kdo_id"}, inplace=True)
# tocke.rename(columns={"to_country_id": "komu_id"}, inplace=True)
# tocke.rename(columns={"from_country": "kdo"}, inplace=True)
# tocke.rename(columns={"to_country": "komu"}, inplace=True)
# tocke.rename(columns={"total_points": "skupne_tocke"}, inplace=True) #tocke_obcinstva+tocke_zirije
# tocke.rename(columns={"tele_points": "tocke_obcinstva"}, inplace=True)
# tocke.rename(columns={"jury_points": "tocke_zirije"}, inplace=True)