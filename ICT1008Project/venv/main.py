import io
import sys
import json
import folium
from PyQt5.QtGui import QTextLayout, QTextLine

from mainTest import programMain
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QApplication, QMainWindow, QComboBox, QTextEdit


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Punggol Transport App"))
        self.setFixedSize(1500, 800)
        self.mainpage()

    def mainpage(self):
        # starting location dropbox
        l1 = QLabel()
        l1.setText("Start Location:")
        start = QComboBox(self)

        # add the starting location to drop down list
        with open('LRT.json') as file1:
            startdata = json.load(file1)
        file1.close()
        for key in startdata.keys():
            start.addItem(startdata[key][0]['NAME'])

        # final location dropbox
        l2 = QLabel()
        l2.setText("Final Location:")
        final = QComboBox(self)

        # add the final location to drop down list
        with open('Punggol_HDB.json') as file2:
            finaldata = json.load(file2)
        file2.close()
        for key in finaldata.keys():
            final.addItem(finaldata[key][0]['ADD'])

        # search button
        search = QPushButton(self.tr("Find shortest path"))
        search.setFixedSize(120, 30)
        search.clicked.connect(lambda: self.findShortestPath(str(start.currentText()), str(final.currentText())))

        # quit app button
        e = QPushButton("Quit", self)
        e.setFixedSize(120, 30)
        e.clicked.connect(self.quitApp)

        # create a central widget in horizontal layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)

        # button container for vertical layout
        button_container = QtWidgets.QWidget()
        button_container.setContentsMargins(50, 50, 50, 50)
        vlay = QtWidgets.QVBoxLayout(button_container)
        vlay.setSpacing(20)
        vlay.addWidget(l1)
        vlay.addWidget(start)
        vlay.addWidget(l2)
        vlay.addWidget(final)
        vlay.addWidget(search)
        vlay.addWidget(e)
        vlay.addStretch()

        # add map widget
        self.basemap = QtWebEngineWidgets.QWebEngineView()
        self.basemap.setContentsMargins(50, 50, 50, 50)

        # add button container and map into central widget
        lay.addWidget(button_container)
        lay.addWidget(self.basemap, stretch=0)

        # create the map
        m = folium.Map(
            location=[1.4045, 103.9072], zoom_start=15
        )

        # plot the nodes for starting location
        for key in startdata.keys():
            folium.Marker((startdata[key][0]['LATITUDE'], startdata[key][0]['LONGTITUDE']), popup=startdata[key][0]['NAME']).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.basemap.setHtml(data.getvalue().decode())

    def quitApp(self):
        self.close()

    def findShortestPath(self, start, dest):
        # algorithm function that returns busStop code, shortest path, bus services in a list
        busCode, pathFound, busSvc = programMain(start, dest)
        self.search = SearchResult(start, dest, busCode, pathFound, busSvc)
        self.search.show()


class SearchResult(QMainWindow):
    srclat = 0.0
    srclon = 0.0
    dstlat = 0.0
    dstlon = 0.0
    numOfstops = 0
    coordinates = {}

    def __init__(self, start, dest, busCode, path, services, parent=None):
        super(SearchResult, self).__init__(parent)
        self.setWindowTitle(self.tr("Shortest Path found"))
        self.setFixedSize(1500, 800)
        self.getCoordinates(start, dest, busCode, path)
        self.searchpage(start, dest, path, services)

    def calMidpoint(self):
        lat = [self.srcLat, self.dstLat]
        lon = [self.srcLon, self.dstLon]
        avg_lat = sum(lat)/len(lat)
        avg_lon = sum(lon)/len(lon)
        return [avg_lat, avg_lon]

    def getCoordinates(self, start, dest, busCode, path):
        with open('BusStop.json') as file3:
            busData = json.load(file3)
        file3.close()

        with open('LRT.json') as file1:
            startdata = json.load(file1)
        file1.close()

        with open('Punggol_HDB.json') as file2:
            finaldata = json.load(file2)
        file2.close()

        # find the lat and lon for src
        for key in startdata.keys():
            if startdata[key][0]['NAME'] == start:
                self.srcLat = float(startdata[key][0]['LATITUDE'])
                self.srcLon = float(startdata[key][0]['LONGTITUDE'])

        # find the lat and lon for dst
        for key in finaldata.keys():
            if finaldata[key][0]['ADD'] == dest:
                self.dstLat = float(finaldata[key][0]['LATITUDE'])
                self.dstLon = float(finaldata[key][0]['LONGTITUDE'])

        self.coordinates[0] = (self.srcLat, self.srcLon)

        # get bus stops coordinates
        for i in range(1, len(path)-1):
            for nodes in busCode:
                for key in busData:
                    if nodes == busData[key]['BusStopCode']:
                        self.coordinates[i] = (float(busData[key]['Latitude']), float(busData[key]['Longitude']))

        self.coordinates[len(path)-1] = (self.dstLat, self.dstLon)
        print(self.coordinates)

    def searchpage(self, s, d, path, services):
        mid = self.calMidpoint()

        # button container for vertical layout
        button_container = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(button_container)
        logOutput = QTextEdit()

        self.numOfstops = len(services)
        if self.numOfstops != 0:
            logOutput.insertPlainText("The bus trip will take " + str(self.numOfstops) + " stops\n")
            logOutput.insertPlainText("\nShortest Path found: \n\n")
            logOutput.insertPlainText("\nFrom " + path[0] + " walk to " + path[1] + "\n")
            count = 0
            bus = services[0]
            for i in range(len(services)):
                if bus == services[i]:
                    count += 1
                    if i == len(services)-1:
                        buses = bus[0]
                        logOutput.insertPlainText("\nTake Bus service " + buses + " for " + str(count)
                                                  + " stops and alight at " + path[i+1] + "\n")
                else:
                    buses = bus[0]
                    logOutput.insertPlainText("\nTake Bus service " + buses + " for " + str(count)
                                              + " stops and alight at " + path[count + 1] + "\n")
                    count = 0
                    bus = services[i + 1]
            logOutput.insertPlainText("\nWalk from " + path[len(path)-2] + " to " + path[len(path)-1])
        else:
            # print(path)
            for nodes in range(0, len(path)-1):
                logOutput.insertPlainText("\nWalk from " + path[nodes] + " to " + path[nodes+1] + "\n")

        logOutput.setDisabled(True)

        # create a central widget in horizontal layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)
        vlay.addWidget(logOutput)

        # add map widget
        self.viewresult = QtWebEngineWidgets.QWebEngineView()
        self.viewresult.setContentsMargins(50, 50, 50, 50)

        # add button container and map into central widget
        lay.addWidget(button_container)
        lay.addWidget(self.viewresult, stretch=1)

        # create the map
        m2 = folium.Map(
            location=mid, zoom_start=15
        )
        list = []
        node = []

        print(len(self.coordinates), len(path))
        for i in range(len(self.coordinates)):
            if i == 0:
                folium.Marker(location=tuple(self.coordinates[i]), popup=s, icon=folium.Icon(color="red")).add_to(m2)
            elif i == len(self.coordinates)-1:
                folium.Marker(location=tuple(self.coordinates[i]), popup=d, icon=folium.Icon(color="red")).add_to(m2)
            else:
                folium.Marker(location=tuple(self.coordinates[i]), popup=path[i]).add_to(m2)

        for i in range(len(self.coordinates)):
            list.append(tuple(self.coordinates[i]))

        for i in list:
            print(i)
            # folium.Marker(location=i, popup=path[i]).add_to(m2)

        folium.PolyLine(locations=list, color='green').add_to(m2)

        data2 = io.BytesIO()
        m2.save(data2, close_file=False)
        self.viewresult.setHtml(data2.getvalue().decode())


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
