import io
import sys
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QLabel


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.tr("Punggol Transport"))
        self.setFixedSize(1500, 800)
        self.mainpage()

    def mainpage(self):
        # starting location dropbox
        l1 = QLabel()
        l1.setText("Start Location:")
        start = QtWidgets.QComboBox(self)
        start.addItem("Punggol MRT")
        start.addItem("Punggol LRT")

        # final location dropbox
        l2 = QLabel()
        l2.setText("Final Location:")
        final = QtWidgets.QComboBox(self)
        final.addItem("test")

        # search button
        search = QtWidgets.QPushButton(self.tr("Find shortest path"))
        search.setFixedSize(120, 30)

        # add map widget
        self.viewmap = QtWebEngineWidgets.QWebEngineView()
        self.viewmap.setContentsMargins(50, 50, 50, 50)

        # create a central widget in horizontal layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)

        # button container for vertical layout
        button_container = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(button_container)
        vlay.setSpacing(20)
        vlay.addWidget(l1)
        vlay.addWidget(start)
        vlay.addWidget(l2)
        vlay.addWidget(final)
        vlay.addWidget(search)
        vlay.addStretch()

        # add button container and map into central widget
        lay.addWidget(button_container)
        lay.addWidget(self.viewmap, stretch=0)

        # create the map
        m = folium.Map(
            location=[1.3984, 103.9072], zoom_start=18
        )
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.viewmap.setHtml(data.getvalue().decode())


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
