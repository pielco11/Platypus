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
    _lat = float(lat) - 1
    _lon = float(lon) - 1
    return str(_lat)+','+str(_lon)

def dirtySecondPoint(lat, lon):
    _lat = float(lat) + 0.1
    _lon = float(lon) + 0.1
    return str(_lat)+','+str(_lon)

def getGeoPoint(url):
    response = http.request('GET', url)
    if response.status != 200:
        print(Fore.RED + '[x] Error: {}'.format(response.status))
        sys.exit(1)
    jPoint = json.loads(response.data.decode('utf-8'))
    return jPoint

def getConstructionPoints(url):
    jPoints = getGeoPoint(url)
    construction = jPoints['incidents']
    #print('[# construction] {}'.format(len(construction)))
    _constructionList = []
    for constructionSite in construction:
        _constructionList.append({
            'title': constructionSite['shortDesc'],
            'desc': constructionSite['fullDesc'],
            'lat': constructionSite['lat'],
            'long': constructionSite['lng']
        })
    return _constructionList

def getAddressPoint(url):
    _jPoint = getGeoPoint(url)
    _jAddress = _jPoint['results'][0]['locations'][0]['latLng']
    return _jAddress

def initCSV(filename):
    fieldnames = ['Title', 'Description', 'Lat', 'Long']
    writer = csv.DictWriter(filename, fieldnames=fieldnames)
    writer.writeheader()
    return writer

def writeRow(writer, constructionSite):
    writer.writerow({
        'Title': constructionSite['title'],
        'Description': constructionSite['desc'],
        'Lat': constructionSite['lat'],
        'Long': constructionSite['long']
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
key = open('key.txt', 'r').read().strip('\n')
constructionUrl = baseUrl + "/traffic/v2/incidents?&outFormat=json&key={}".format(key)
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

city = input(Fore.YELLOW + "[<] City: " + Style.RESET_ALL)
city = city.replace(' ', '+').replace(',', '%2C')
writeCSV = input(Fore.YELLOW + "[<] write to: " + Style.RESET_ALL)

with open(writeCSV, 'w') as outputFile:
    writer = initCSV(outputFile)

    addressUrl = baseUrl + "/geocoding/v1/address?key={}&location={}".format(key, city)
    addressPoint = getAddressPoint(addressUrl)

    firstPoint = dirtyFirstPoint(addressPoint['lat'], addressPoint['lng'])
    secondPoint = dirtySecondPoint(addressPoint['lat'], addressPoint['lng'])

    constructionUrl = constructionUrl + "&boundingBox={}&filters=construction".format(firstPoint+','+secondPoint)
    constructionList = getConstructionPoints(constructionUrl)
    for constructionSite in constructionList:
        writeRow(writer, constructionSite)
