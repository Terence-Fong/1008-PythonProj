import json
import heapq
from datetime import datetime
import AlgoTest
from Dataset import Graph
import Populate
import math

mapGraph = Graph()
infoDict = {}

# Populate graph and infodict
mapGraph, infoDict = Populate.populateHDB(mapGraph, infoDict)
mapGraph, infoDict = Populate.populateBus(mapGraph, infoDict)
mapGraph, infoDict = Populate.populateLRT(mapGraph, infoDict)
mapGraph = Populate.addBusRoute(mapGraph)
mapGraph = Populate.addHDBtoBusStop(mapGraph, infoDict)
mapGraph = Populate.addLRTtoBusStops(mapGraph, infoDict)

HDB = 821160
LRT = 3 # Soo Teck

# Get bus stop closest to HDB
busStop = mapGraph.getHDBBusStop(HDB)
busStopHDB = infoDict[busStop]['Description']

# Get bus stop closes to LRT
LRTbusStops = mapGraph.getLRTBusStop(LRT)
busStopLRT1 = infoDict[LRTbusStops[0]]['Description']
busStopLRT2 = infoDict[LRTbusStops[1]]['Description']

# Bus shortest path
try:
    busSP1, numStops1 = AlgoTest.calculate_route(busStopLRT1, busStopHDB)
except:
    numStops1 = math.inf
try:
    busSP2, numStops2 = AlgoTest.calculate_route(busStopLRT2, busStopHDB)
except:
    numStops2 = math.inf

if numStops1 < numStops2:
    numStops = numStops1
    busSP = busSP1
else:
    numStops = numStops2
    busSP = busSP2

busStopSP = []
busSvc = []
for stops in busSP:
    busStopSP.append(stops[0])
    busSvc.append(stops[1])

# cleaning up the array
for x in range(len(busSvc)):
    if busSvc[x] is None:
        busSvc[x] = busSvc[x+1]

print(busStopSP)
print(busSvc)

fullSP = []
fullSP.append(str(LRT))
fullSP.extend(busStopSP)
fullSP.append(str(HDB))
print(fullSP)

fullSPtranslated = []
for code in fullSP:
    if len(code) < 3:
        fullSPtranslated.append(infoDict[str(code)]['Name'])
    elif len(code) == 5:
        fullSPtranslated.append(infoDict[str(code)]['Description'])
    else:
        fullSPtranslated.append(infoDict[str(code)]['Address'])

print(fullSPtranslated)

# fullSP is the full path, fullSPtranslated is translated the codes to names
# busSvc is the bus svc from fullSP[1] to last stop. The last name of the fullSP is the HDB address
