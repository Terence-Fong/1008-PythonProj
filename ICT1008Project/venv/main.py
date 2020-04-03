import io
import sys
import json
import folium
from mainLogic import programMain
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
        pathFound, busSvc, LatLon = programMain(start, dest)
        self.search = SearchResult(start, dest, pathFound, busSvc, LatLon)
        self.search.show()


class SearchResult(QMainWindow):
    srclat = 0.0
    srclon = 0.0
    dstlat = 0.0
    dstlon = 0.0
    numOfstops = 0

    def __init__(self, start, dest, path, services, LatLon, parent=None):
        super(SearchResult, self).__init__(parent)
        self.setWindowTitle(self.tr("Shortest Path found"))
        self.setFixedSize(1500, 800)
        self.getCoordinates(start, dest)
        self.searchpage(start, dest, path, services, LatLon)

    def calMidpoint(self):
        lat = [self.srcLat, self.dstLat]
        lon = [self.srcLon, self.dstLon]
        avg_lat = sum(lat)/len(lat)
        avg_lon = sum(lon)/len(lon)
        return [avg_lat, avg_lon]

    def getCoordinates(self, start, dest):
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

    def searchpage(self, s, d, path, services, LatLon):
        mid = self.calMidpoint()

        # button container for vertical layout
        button_container = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(button_container)
        logOutput = QTextEdit()

        self.numOfstops = len(services)-2
        if self.numOfstops != 0:
            logOutput.insertPlainText("The bus trip will take " + str(self.numOfstops) + " stops\n")
            logOutput.insertPlainText("\nShortest Path found: ")
            logOutput.insertPlainText("\nFrom " + path[0] + " walk to " + path[1] + "\n")
            count = 0
            bus = services[1]
            for i in range(1, len(services)-1):
                if bus == services[i] and self.numOfstops != 0:
                    count += 1
                    if i == len(services)-2:
                        buses = bus[0]
                        print(buses)
                        logOutput.insertPlainText("\nTake Bus service " + buses + " for " + str(count)
                                                  + " stops and alight at " + path[i+1] + "\n")

                else:
                    buses = bus[0]
                    print(buses)
                    logOutput.insertPlainText("\nTake Bus service " + buses + " for " + str(count)
                                              + " stops and alight at " + path[i] + "\n")
                    count = 1
                    bus = services[i]
            logOutput.insertPlainText("\nWalk from " + path[len(path)-2] + " to " + path[len(path)-1])
        else:
            logOutput.insertPlainText("\nWalk from " + path[0] + " to " + path[2] + "\n")

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
        if self.numOfstops == 0:
            del LatLon[1]
        for i in range(len(LatLon)):
            if i == 0:
                folium.Marker(location=LatLon[i], popup=s, icon=folium.Icon(color="red")).add_to(m2)
            elif i == len(LatLon) - 1:
                folium.Marker(location=LatLon[i], popup=d, icon=folium.Icon(color="red")).add_to(m2)
            else:
                folium.Marker(location=LatLon[i], popup=path[i]).add_to(m2)

        folium.PolyLine(locations=LatLon, color='green').add_to(m2)

        data2 = io.BytesIO()
        m2.save(data2, close_file=False)
        self.viewresult.setHtml(data2.getvalue().decode())


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
