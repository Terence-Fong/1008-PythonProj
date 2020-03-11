from onemapsg import OneMapClient
import json
import heapq

def get_jsonLRT():
    results = json.loads(open("LRT.json").read())
    return results

def get_jsonHDB():
    results = json.loads(open("Punggol_HDB.json").read())
    return results

def get_jsonRoutes():
    #LRT.json to be replaced with routes json
    results = json.loads(open("LRT.json").read())
    return results

def get_jsonStops():
    #LRT.json to be replaced by stops json
    results = json.load(open("LRT.json").read())
    return results

#Need json for every bus stop and lrt
#Need json for all the bus routes and lrt routes

lrt = get_jsonLRT()
hdb = get_jsonHDB()
routes = get_jsonRoutes()
stops = get_jsonStops()

#converting flat lists into dictionaries of Descriptions THE KEY IS DESCRIPTION
stop_map = {stop['Description']: stop for stop in stops}
#converting flat lists into dictionaries of Bus Stop Codes THE KEY IS BUS STOP CODE
code_map = {stop['BusStopCode']: stop for stop in stops}


route_map = {}

for route in routes:
    key = (route["ServiceNo"], route["Direction"])
    if key not in route_map:
        route_map[key] = []
    route_map[key] += [route]

path = shortest_route()

def shortest_route(start, end, route_map):
    pass