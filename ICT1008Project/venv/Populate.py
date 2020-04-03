import json
from math import cos, asin, sqrt

def populateHDB(mapGraph, infoDict):
    with open('Punggol_HDB.json') as f:
        data = json.load(f)
    f.close
    for key in data.keys():
        mapGraph.addVertex(data[key][0]['POSTAL'])
        infoDict[data[key][0]['POSTAL']] = {}
        infoDict[data[key][0]['POSTAL']]['Name'] = data[key][0]['NAME']
        infoDict[data[key][0]['POSTAL']]['Address'] = data[key][0]['ADD']
        infoDict[data[key][0]['POSTAL']]['Latitude'] = data[key][0]['LATITUDE']
        infoDict[data[key][0]['POSTAL']]['Longitude'] = data[key][0]['LONGTITUDE']

    return mapGraph, infoDict

def addHDBtoBusStop(mapGraph, infoDict):

    for key in infoDict:
        # if is postal code
        if len(key) == 6:
            distarr = []
            key2arr = []
            for key2 in infoDict:
                # check all bus stop
                if len(key2) == 5:
                    # find closest bus stops to the hdb
                    dist = distance(infoDict[key]['Latitude'], infoDict[key]['Longitude'], infoDict[key2]['Latitude'],
                                    infoDict[key2]['Longitude'])
                    distarr.append(dist)
                    key2arr.append(key2)
            mapGraph.addHDBEdge(key, key2arr[distarr.index(min(distarr))], min(distarr))

    return mapGraph

def populateBus(mapGraph, infoDict):

    with open('BusStop.json') as f:
        data = json.load(f)
    f.close
    # Add busstops
    for x in data:
        mapGraph.addVertex(data[x]['BusStopCode'])
        if 'Latitude' in data[x]:
            infoDict[data[x]['BusStopCode']] = {}
            infoDict[data[x]['BusStopCode']]['Description'] = data[x]['Description']
            infoDict[data[x]['BusStopCode']]['RoadName'] = data[x]['RoadName']
            infoDict[data[x]['BusStopCode']]['Latitude'] = data[x]['Latitude']
            infoDict[data[x]['BusStopCode']]['Longitude'] = data[x]['Longitude']

    return mapGraph, infoDict

def populateLRT(mapGraph, infoDict):
    with open('LRT.json') as f:
        data = json.load(f)
    f.close
    # Add LRT
    for x in data:
        mapGraph.addVertex(x)
        infoDict[x] = {}
        infoDict[x]['Name'] = data[x][0]['NAME']
        infoDict[x]['Latitude'] = data[x][0]['LATITUDE']
        infoDict[x]['Longitude'] = data[x][0]['LONGTITUDE']

    return mapGraph, infoDict

def addLRTtoBusStops(mapGraph, infoDict):
    for key in infoDict:
        # if is LRT
        if int(key) <= 15:
            distarr = []
            key2arr = []
            for key2 in infoDict:
                # check all bus stop
                if len(key2) == 5:
                    # find 2 closest bus stops to the hdb
                    dist = distance(infoDict[key]['Latitude'], infoDict[key]['Longitude'], infoDict[key2]['Latitude'],
                                    infoDict[key2]['Longitude'])
                    distarr.append(dist)
                    key2arr.append(key2)
            mapGraph.addHDBEdge(key, key2arr[distarr.index(min(distarr))], min(distarr))
            minIndex = distarr.index(min(distarr))
            del key2arr[minIndex]
            del distarr[minIndex]
            mapGraph.addHDBEdge(key, key2arr[distarr.index(min(distarr))], min(distarr))

    return mapGraph

def distance(lat1, lon1, lat2, lon2):
    # Haversine formula, to calculate the distance between given latitude and longitude
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))



