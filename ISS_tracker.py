#%%
import requests
import folium
import datetime
reponse = requests.get(url="http://api.open-notify.org/iss-now.json")

# Connection error status
reponse.raise_for_status()

data = reponse.json()
#print(data)

timestamp = data["timestamp"]
longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]
date_time = datetime.datetime.utcfromtimestamp(timestamp)
iss_position = (longitude, latitude)

print(iss_position)
#print(date_time)


mapObj = folium.Map(location=[latitude,longitude], zoom_start=2)
folium.Marker(location=[latitude,longitude]).add_to(mapObj)
mapObj.save("ISS.html")







# %%
