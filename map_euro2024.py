import folium
import pandas as pd
import webbrowser

df_euro24 = pd.read_csv("stadiums.csv")

# lat y lng de Alemania, que es donde se realiza la euro
latitude = 51.312801
longitude = 9.481544

sf_map = folium.Map(location = [latitude, longitude], zoom_start = 6)

# Inicializamos un FeatureGroup() para la Euro del DataFrame
euro2024 = folium.map.FeatureGroup()

# Recorre los 100 crímenes y agrega a cada uno al FeatureGroup() de incidentes
# La columna Y y X son las coordenadas, latitud y longitud respectivamente
# La columna "Category" es el tipo de incidente.

for lat, lng, label, foto in zip(df_euro24["lat"], df_euro24["long"], df_euro24["label"], df_euro24["foto"]):

    html = f'''<div style="white-space: nowrap; text-align: center;">
                    {label}<br>
                  <img src="{foto}" alt="Image" style="max-width:100%; max-height:100%;">
                  
               </div>'''

    iframe = folium.IFrame(html,
                       width=len(label)*8,
                       height=200)

    popup = folium.Popup(iframe,
                     max_width=250)
    
    
    
    euro2024.add_child(folium.Marker(location = [lat, lng],
                                      popup    = popup))
    
# Agrega incidentes al map
sf_map.add_child(euro2024)

map_filename = 'map_euro2024.html'
euro2024.save(map_filename)

webbrowser.open(map_filename) 