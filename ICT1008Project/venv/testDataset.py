from Dataset import Graph
import Populate

mapGraph = Graph()
infoDict = {}
# Populate graph and infodict
mapGraph, infoDict = Populate.populateHDB(mapGraph, infoDict)
mapGraph, infoDict = Populate.populateBus(mapGraph, infoDict)
mapGraph, infoDict = Populate.populateLRT(mapGraph, infoDict)
# print(infoDict)
mapGraph = Populate.addBusRoute(mapGraph)
mapGraph = Populate.addHDBtoBusStop(mapGraph, infoDict)
mapGraph = Populate.addLRTtoBusStops(mapGraph, infoDict)
mapGraph.printGraph()
# print(infoDict)