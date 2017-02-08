import folium
import pandas

df=pandas.read_csv("countrycapitals.csv", error_bad_lines=False)


map=folium.Map(location=[df['CapitalLatitude'].mean(),df['CapitalLongitude'].mean()],zoom_start=4,tiles='Mapbox bright')

def color(latitude):
        minimum=min(df['CapitalLatitude'])
        step=(max(df['CapitalLatitude']))-(min(df['CapitalLatitude']))/3
        if latitude in range(int(minimum),int(minimum+step)):
                color='red'
        elif latitude in range(int(minimum+step),int(minimum+step*2)):
                color='green'
        else:
                color='blue'
        return color

fg=folium.FeatureGroup('Lat_long_countrycode')

for lat,lon,code in zip(df['CapitalLatitude'],df['CapitalLongitude'],df['CountryCode']):
        fg.add_child(folium.Marker(location=[lat,lon],popup=str(code),icon=folium.Icon(color=color(lat))))

map.add_child(fg)

map.add_child(folium.GeoJson(data=open('world_population.geojson'),
name='World_poplulation 2014',
style_function=lambda x:{'fillColor':'green' if x['properties']['population_2014']<=10000000 else 'orange' if 10000000<x['properties']['population_2014']<20000000 else 'red'}
))

map.add_child(folium.LayerControl())
map.save(outfile='test.html')
