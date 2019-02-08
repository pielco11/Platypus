# input CSV
# 1.0 API(street) => CSV(data)
# 1.1 API(street) => KML(data)

# fields of interest:
# incidents_lat, incidents_long, incidents_shortDesc, and incidents_fullDesc
# that needs to be relabeled to: Lat, Long, Title, Description

# what data?
# pull construction and events

import csv
import json
import urllib3
import certifi
from colorama import init, Fore

from geopy.geocoders import Nominatim

def dirtyNewPoint(lat, lon):
    _lat = float(lat) + 0.003
    _lon = float(lon) + 0.004

    return str(_lat)+','+str(_lon)

init(autoreset=True)

geolocator = Nominatim(user_agent="platypus-1.0")
key = ""
baseUrl = "http://www.mapquestapi.com/traffic/v2/incidents?key={}".format(key)
http = urllib3.PoolManager( 1,
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where(),
        headers={'user-agent': 'platypus-1.0', 'Cookie': ''})

print(Fore.CYAN + """
██████╗ ██╗      █████╗ ████████╗██╗   ██╗██████╗ ██╗   ██╗███████╗
██╔══██╗██║     ██╔══██╗╚══██╔══╝╚██╗ ██╔╝██╔══██╗██║   ██║██╔════╝
██████╔╝██║     ███████║   ██║    ╚████╔╝ ██████╔╝██║   ██║███████╗
██╔═══╝ ██║     ██╔══██║   ██║     ╚██╔╝  ██╔═══╝ ██║   ██║╚════██║
██║     ███████╗██║  ██║   ██║      ██║   ██║     ╚██████╔╝███████║
╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝      ╚═════╝ ╚══════╝
""")

print(Fore.YELLOW + "[<] City: ")
city = input()
geoCodedCity = geolocator.geocode(city, timeout=1000)
firstPoint = str(geoCodedCity.latitude) + ',' + str(geoCodedCity.longitude)
secondPoint = dirtyNewPoint(geoCodedCity.latitude, geoCodedCity.longitude)
print(firstPoint)
print(secondPoint)

url = baseUrl + "&boundingBox={}&filters=incidents".format(firstPoint+','+secondPoint)
response = http.request('GET', url)
print(response.status)
print(json.loads(response.data.decode('utf-8')))

