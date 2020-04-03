import AlgoLogic
from Dataset import Graph
import Populate
import math


def programMain(LRTname, HDBadd):

    mapGraph = Graph()
    infoDict = {}

    # Populate graph and infodict for LRT BUS and HDB
    # infodict is a dictionary of the data
    mapGraph, infoDict = Populate.populateHDB(mapGraph, infoDict)
    mapGraph, infoDict = Populate.populateBus(mapGraph, infoDict)
    mapGraph, infoDict = Populate.populateLRT(mapGraph, infoDict)
    mapGraph = Populate.addHDBtoBusStop(mapGraph, infoDict)
    mapGraph = Populate.addLRTtoBusStops(mapGraph, infoDict)

    # Change input to postal code and lrt code
    for key in infoDict:
        if len(key) == 6:
            if infoDict[key]["Address"] == HDBadd:
                HDB = key
        if len(key) < 3:
            if infoDict[key]["Name"] == LRTname:
                LRT = key
    # HDB = 822312
    # LRT = 4

    # if distance is less than 400m (estimate)
    if (Populate.distance(infoDict[HDB]['Longitude'], infoDict[HDB]['Latitude'], infoDict[LRT]['Longitude'], infoDict[LRT]['Latitude']) < 0.15):
        fullSPtranslated = [LRTname, "", HDBadd]
        busSvc = [None, None]
        latlon = []
        latlon.append((float(infoDict[LRT]['Latitude']), float(infoDict[LRT]['Longitude'])))
        latlon.append((0.00, 0.00))
        latlon.append((float(infoDict[HDB]['Latitude']), float(infoDict[HDB]['Longitude'])))
        return fullSPtranslated, busSvc, latlon
    else:
        # Get bus stop closest to HDB
        busStop = mapGraph.getHDBBusStop(HDB)
        busStopHDB = infoDict[busStop]['Description']

        # Get 2 bus stop closest to LRT
        LRTbusStops = mapGraph.getLRTBusStop(LRT)
        busStopLRT1 = infoDict[LRTbusStops[0]]['Description']
        busStopLRT2 = infoDict[LRTbusStops[1]]['Description']

        # Bus shortest path for 2 closest bus to LRT and use the shorter one
        try:
            busSP1, numStops1 = AlgoLogic.calculate_route(busStopLRT1, busStopHDB)
        except:
            numStops1 = math.inf
        try:
            busSP2, numStops2 = AlgoLogic.calculate_route(busStopLRT2, busStopHDB)
        except:
            numStops2 = math.inf

        # choose shorter path
        if numStops1 < numStops2:
            numStops = numStops1
            busSP = busSP1
        else:
            numStops = numStops2
            busSP = busSP2

        # SP bus stops code and bus svc
        busStopSP = []
        busSvc = []
        for stops in busSP:
            busStopSP.append(stops[0])
            busSvc.append(stops[1])

        # Change the first None value to the bus svc
        # convert busSvc to fullSP bussvc
        busSvc.append(None)

        # Shortest Path from LRT to HDB code
        fullSP = []
        fullSP.append(str(LRT))
        fullSP.extend(busStopSP)
        fullSP.append(str(HDB))

        # convert fullSP which is code into names
        fullSPtranslated = []
        for code in fullSP:
            if len(code) < 3:
                fullSPtranslated.append(infoDict[str(code)]['Name'])
            elif len(code) == 5:
                fullSPtranslated.append(infoDict[str(code)]['Description'])
            else:
                fullSPtranslated.append(infoDict[str(code)]['Address'])

        # put the SP lat and long tuple into an array
        latlon = []
        for code in fullSP:
                latlon.append((float(infoDict[str(code)]['Latitude']), float(infoDict[str(code)]['Longitude'])))

        return fullSPtranslated, busSvc, latlon

    # fullSP is the full path, fullSPtranslated is translated the codes to names
    # busSvc is the bus svc from fullSP[1] to last stop. The last name of the fullSP is the HDB address

# programMain("NIBONG LRT STATION (PW5)", "312 PUNGGOL PARCVISTA SUMANG LINK 820312")