import sys

class Vertex:
    def __init__(self, nid, name, address, postal, lon, lat):
        self.nid = nid
        self.name = name
        self.address = address
        self.postal = postal
        self.lon = lon
        self.lat = lat
        self.visited = False
        # Dictionary neighbour with node as key and weight as value
        self.neighbour = {}
        # # Set distance to all node to infinity
        # self.distance = sys.maxsize

    def getNID(self):
        return self.nid

    def getName(self):
        return self.name

    def getAddress(self):
        return self.address

    def getPostal(self):
        return self.postal

    def getLongitude(self):
        return self.lon

    def getLatitude(self):
        return self.lat

    def addNeighbour(self, neighbour, weight=0):
        self.neighbour[neighbour] = weight

    def getNeighbour(self):
        return self.neighbour.keys()

    def printNeighbour(self):
        for x in self.neighbour:
            print("key=" + str(x.getNID()) + " value=" + str(self.neighbour.get(x)))

class Graph:
    def __init__(self):
        # Creates a new graph object
        self.data = {}

    def __iter__(self):
        return iter(self.data.values())

    def getVertices(self):
        return list(self.data.keys())

    def getEdges(self, vertex):
        return self.data

    def addVertex(self, vertex):
        # if key not in dict
        if vertex not in self.data:
            self.data[vertex] = []

    def addEdge(self, fromVertex, toVertex, weight=0):
        if fromVertex not in self.data:
            self.addVertex(fromVertex)
        if toVertex not in self.data:
            self.addVertex(toVertex)

        # Both ways
        fromVertex.addNeighbour(toVertex, weight)
        toVertex.addNeighbour(fromVertex, weight)
        self.data[fromVertex] = (toVertex, weight)
        self.data[toVertex] = (fromVertex, weight)
        # self.data[fromVertex].addNeighbour(toVertex, weight)
        # self.data[toVertex].addNeighbour(fromVertex, weight)

    def printGraph(self):
        for x in self.data:
            print("key= " + str(x.getNID()) + " value= " + str(self.data.get(x)[0].getNID()))