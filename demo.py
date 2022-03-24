
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from myui import Ui_MainWindow
import cv2
import numpy


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    #初始化
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        '''下面连接动作对应的函数'''
        self.pushButton.clicked.connect(self.openFile)#按钮一连接openFile函数

    def openFile(self):
        #选择且获取图片文件的地址
        fileName, filetype = QFileDialog.getOpenFileName(
            self,
            "选取文件",
            "C:/",
            "Image Files (*.bmp *.jpg *.jpeg *.png)")
        self.showFile(fileName)

    # 将图片显示在label
    def showFile(self,fileName):
        srcImage = cv2.imdecode(numpy.fromfile(fileName, dtype=numpy.uint8), -1)
        image_height, image_width, image_depth = srcImage.shape  # 获取图像的高，宽以及深度。
        # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        QImg = cv2.cvtColor(srcImage, cv2.COLOR_BGR2RGB)
        QShowImage = QImage(QImg.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                            image_width * image_depth,
                            QImage.Format_RGB888)
        self.label.clear()
        QShowImage = QShowImage.scaled(
            self.label.width(),
            self.label.height())  # 图片适应label大小
        self.label.setPixmap(QPixmap.fromImage(QShowImage))


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())