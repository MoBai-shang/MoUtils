import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import Qt
import time
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout,QWidget,QDesktopWidget
class ImagePlayer(QWidget):
    def __init__(self, filename,size=(0,0), title=None,speed=None, parent=None):
        QWidget.__init__(self, parent)
        # Load the file into a QMovie
        self.movie =  QtGui.QMovie(filename, QByteArray(), self)
        #size = self.movie.scaledSize()
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry((screen.width() - size[0]) // 2,
        (screen.height() - size[1]) // 2, size[0],size[1])
        self.setWindowFlags(Qt.FramelessWindowHint)#no border
        self.setAttribute(Qt.WA_TranslucentBackground, True)#background parrent
        if title:
            self.setWindowTitle(title)
        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        # Add the QMovie object to the label
        self.movie.setCacheMode( QtGui.QMovie.CacheAll)
        if speed:
            self.movie.setSpeed(speed)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

def loading(filename,app=None,size=(0,0),delay=3,title=None,speed=None,parent=None):
    if 'gif' in filename:
        face=ImagePlayer(filename,size,title,speed,parent)
        face.show()
        t1=time.time()
        while time.time()-t1 < delay:
            QtWidgets.QApplication.processEvents()# 处理主进程事件
        if app:
            app.show()
        face.hide()

app = QtWidgets.QApplication(sys.argv)
item=QWidget()
loading("H:/image/GIF/BirdDiance2.gif",item,(800,499))

sys.exit(app.exec_())
