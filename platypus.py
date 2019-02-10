# input CSV
# 1.0 API(street) => CSV(data)
# 1.1 API(street) => KML(data)

# fields of interest:
# incidents_lat, incidents_long, incidents_shortDesc, and incidents_fullDesc
# that needs to be relabeled to: Lat, Long, Title, Description

# what data?
# pull construction and events

import sys
import csv
import json
import urllib3
import certifi
from colorama import init, Fore, Style

def dirtyFirstPoint(lat, lon):
    _lat = float(lat) - 0.1
    _lon = float(lon) - 0.1
    return str(_lat)+','+str(_lon)

def dirtySecondPoint(lat, lon):
    _lat = float(lat) + 0.1
    _lon = float(lon) + 0.1
    return str(_lat)+','+str(_lon)

def getGeoPoint(url):
    response = http.request('GET', url)
    if response.status != 200:
        print(Fore.RED + '[x] Error')
        print(response.status)
        sys.exit(1)
    jPoint = json.loads(response.data.decode('utf-8'))
    return jPoint

def getIncidentsPoints(url):
    jPoints = getGeoPoint(url)
    incidents = jPoints['incidents']
    #print('[# incidents] {}'.format(len(incidents)))
    _incidentsList = []
    for incident in incidents:
        _incidentsList.append({
            'title': incident['shortDesc'],
            'desc': incident['fullDesc'],
            'lat': incident['lat'],
            'long': incident['lng']
        })
        #print('<-->')
        #print('---- Title: {}'.format(incident['shortDesc']))
        #print('---- Description: {}'.format(incident['fullDesc']))
        #print('---- Geo: {},{}'.format(incident['lat'], incident['lng']))
    return _incidentsList

def getAddressPoint(url):
    _jPoint = getGeoPoint(url)
    _jAddress = _jPoint['results'][0]['locations'][0]['latLng']
    return _jAddress

def initCSV(filename):
    fieldnames = ['Title', 'Description', 'Lat', 'Long']
    writer = csv.DictWriter(filename, fieldnames=fieldnames)
    writer.writeheader()
    return writer

def writeRow(writer, incident):
    writer.writerow({
        'Title': incident['title'],
        'Description': incident['desc'],
        'Lat': incident['lat'],
        'Long': incident['long']
    })

def readRows(file):
    _entries = []
    with open(file) as inputFile:
        reader = csv.reader(inputFile)
        for row in reader:
            row[0] = row[0].replace(' ', '+')
            _entries.append(row[0]+'%2C'+row[1])
    return _entries

init(autoreset=True)
baseUrl = "https://www.mapquestapi.com"
key = ""
incidentsUrl = baseUrl + "/traffic/v2/incidents?&outFormat=json&key={}".format(key)
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

readCSV = input(Fore.YELLOW + "[<] read from: " + Style.RESET_ALL)
writeCSV = input(Fore.YELLOW + "[<] write to: " + Style.RESET_ALL)

cities = readRows(readCSV)
with open(writeCSV, 'w') as outputFile:
    writer = initCSV(outputFile)
    for city in cities:
        addressUrl = baseUrl + "/geocoding/v1/address?key={}&location={}".format(key, city)
        print(addressUrl)
        addressPoint = getAddressPoint(addressUrl)
        firstPoint = dirtyFirstPoint(addressPoint['lat'], addressPoint['lng'])
        secondPoint = dirtySecondPoint(addressPoint['lat'], addressPoint['lng'])

        incidentsUrl = incidentsUrl + "&boundingBox={}&filters=incidents".format(firstPoint+','+secondPoint)
        incidentsList = getIncidentsPoints(incidentsUrl)

        for incident in incidentsList:
            writeRow(writer, incident)