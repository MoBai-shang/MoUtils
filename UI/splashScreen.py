# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import sys
#重写QSplashScreen类
class MySplashScreen(QSplashScreen):
    # 鼠标点击事件
    def mousePressEvent(self, event):
        pass

# 主界面
class MyWindow(QMainWindow):
    # 初始化MenuDemo子类
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowTitle("Demo")
        # 宽×高
        self.resize(600, 600)
        # 最小窗口尺寸
        self.setMinimumSize(600,500)
        self.btn = QPushButton('关闭窗口')
        self.btn.clicked.connect(self.fun_Exit)
        self.setCentralWidget(self.btn)

    def load_data(self, sp):
        for i in range(1, 11):  # 模拟主程序加载过程
            time.sleep(0.5)  # 加载数据
            sp.showMessage("Main加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
            QtWidgets.qApp.processEvents()  # 允许主进程处理事件

    # 退出菜单响应
    def fun_Exit(self):
        response_quit = QApplication.instance()
        response_quit.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #设置启动界面
    splash = MySplashScreen()#QMovie类用来加载gif格式的图片，QSplashScreen类用来加载静态图片，他们都需要使用QLable容器接收，然后进行显示
    #初始图片
    splash.setPixmap(QPixmap('H:/image/JPG/124.jpg'))  # 设置背景图片
    #初始文本
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    # 设置字体
    splash.setFont(QFont('微软雅黑', 10))
    # 显示启动界面
    splash.show()
    app.processEvents()  # 处理主进程事件
    #主窗口
    window = MyWindow()
    window.load_data(splash)  # 加载数据
    window.show()
    splash.finish(window)  # 隐藏启动界面
    splash.deleteLater()
    app.exec_()