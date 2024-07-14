from time import sleep
import numpy as np
import pandas as pd

import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import folium

# abro el browser en la página de eurocopa 
browser = webdriver.Chrome()

browser.get("https://es.wikipedia.org/wiki/Eurocopa_2024")

browser.maximize_window()

# defino las filas de la tabla que quiero y sus columnas respectivas
filas = [3, 8, 13]
col_4 = [1, 2]
cols = [x for x in range(1,5)]
data = []

# inicio un bucle para las filas
for fila in filas:
    # la fila 8 solo contiene 2 y se comporta diferente, por lo que hacemos una excepción
    if fila == 8:
        for col in col_4: 
            browser.find_element(by = By.XPATH, value = f'//*[@id="mw-content-text"]/div[1]/center[1]/table/tbody/tr[{fila}]/td[{col}]/a').click()
            sleep(2)
            
            # definir bs4
            soup = BeautifulSoup(browser.page_source, "html.parser")

            # city
            ciudad = soup.find_all("tr")[4].find("td").find_all("a", recursive = False)[0]
            ciudad = ciudad.text if ciudad else np.nan

            # estadio
            estadio = soup.find("h1")
            estadio = estadio.text if estadio else np.nan
            
            # foto
            foto = soup.find_all("tr")[1].find("a")
            foto = str(foto).split('src="')[1].split('" src')[0] if foto else np.nan
            foto = f'https:{foto}'

            #lat, long
            lat_long = soup.find("span", class_ = "geo-dec")
            lat_long = lat_long.text.split(",") if lat_long else np.nan
            lat, long = lat_long
            long = long.strip()

            data.append([estadio, ciudad, lat, long, foto])
            browser.back()
        #continue para que no se vuelva a ejecutar
        continue
    #las otras dos filas que se comportan igual
    for col in cols:
        browser.find_element(by = By.XPATH, value = f'//*[@id="mw-content-text"]/div[1]/center[1]/table/tbody/tr[{fila}]/td[{col}]/a').click()
        sleep(2)
            
        # definir bs4
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # city
        ciudad = soup.find_all("tr")[4].find("td").find_all("a", recursive = False)[0]
        ciudad = ciudad.text if ciudad else np.nan

        # estadio
        estadio = soup.find("h1")
        estadio = estadio.text if estadio else np.nan
        
        # foto
        foto = soup.find_all("tr")[1].find("a")
        foto = str(foto).split('src="')[1].split('" src')[0] if foto else np.nan
        foto = f'https:{foto}'


        #lat, long
        lat_long = soup.find("span", class_ = "geo-dec")
        lat_long = lat_long.text.split(",") if lat_long else np.nan
        lat, long = lat_long
        long = long.strip()

        data.append([estadio, ciudad, lat, long, foto])
        browser.back()

browser.quit()


# Genero el DataFrame y le agrego en una sola columna el estadio y la ciudad
df_euro24 = pd.DataFrame(data, columns = ['estadio', 'ciudad', 'lat', 'long', 'foto'])

df_euro24["label"] = df_euro24["estadio"] + ", " + df_euro24["ciudad"]

df_euro24["foto"] = df_euro24["foto"].apply(lambda x: x.split()[0])

df_euro24

df_euro24.to_csv("stadiums.csv")