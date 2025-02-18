class Graph:
    def __init__(self):
        # Creates a new graph object
        self.data = {}

    def __iter__(self):
        return iter(self.data.values())

    def getVertices(self):
        return list(self.data.keys())

    def getEdges(self, nid):
        return self.data[nid]

    def getVertex(self, nid):
        for key in self.data.keys():
            if key == nid:
                return key
        return None

    def addVertex(self, nid):
        # if key not in dict
        if nid not in self.data:
            self.data[nid] = {}

    def addHDBEdge(self, fromNID, toNID, weight=0):
        if fromNID not in self.data:
            self.addVertex(fromNID)
        if toNID not in self.data:
            self.addVertex(toNID)

        # Both ways
        self.data[fromNID][toNID] = weight
        self.data[toNID][fromNID] = weight

    def addBusEdge(self, fromNID, toNID, BusSvc, direction, weight=0):
        if fromNID not in self.data:
            self.addVertex(fromNID)
        if toNID not in self.data:
            self.addVertex(toNID)

        # Both ways
        self.data[fromNID][(toNID, (BusSvc, direction))] = weight

    def addLRTEdge(self, fromNID, toNID, weight=0):
        if fromNID not in self.data:
            self.addVertex(fromNID)
        if toNID not in self.data:
            self.addVertex(toNID)

        # Both ways
        self.data[fromNID][toNID] = weight

    def printGraph(self):
        for x in self.data:
            print(str(x) + ": ", end="")
            print(str(self.data.get(x)))

    def getHDBBusStop(self, postalCode):
        for code in self.data[str(postalCode)]:
            return code

    def getLRTBusStop(self, LRT):
        twostops = []
        num = 0
        for code in self.data[str(LRT)]:
            if num < 2:
                twostops.append(code)
                num += 0
        return twostops