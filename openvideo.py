
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal#多线程
import filetype
from myui import Ui_MainWindow
import threading
import cv2
import numpy as np
# 多线程类
class MyThread(QThread):  # 建立一个任务线程类
    signal = pyqtSignal(object)  # 设置触发信号传递的参数数据类型,传递信号必须事先定义好数据类型
    def __init__(self,fileName):
        super(MyThread, self).__init__()
        self.file=fileName
    def __del__(self):
        self.terminate()
        '''
        线程的主程序 函数功能：读取视频帧，在获得视频帧时，
        通过线程的emit函数触发传递视频帧，
        界面窗体获得该帧后展示在窗体的标签上'''
    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        self.cap = cv2.VideoCapture(self.file)
        while True:
            self.ret, self.srcImage = self.cap.read()
            try:
                self.signal.emit(self.srcImage)
            except:
                print("error:10086")
                break
            if (self.ret == False):
                print("the viedo is over.")
                break
        self.cap.release()

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    #初始化
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        '''下面连接动作对应的函数'''
        self.pushButton.clicked.connect(self.openFile)#按钮一连接openFile函数

        '''对文件类型判断选择不同的函数实现展示功能'''
    def openFile(self):
        #选择且获取文件的地址
        fileName,filetype11= QFileDialog.getOpenFileName(
            self,
            "选取文件",
            "C:/",
            "all file(*)")
        try:
            type = filetype.guess(fileName)
            print(type.mime)
            if str(type.mime) == 'video/mp4' or str(type.mime) =='video/x-flv':
                print("video!")
                self.open_video(fileName)
            elif str(type.mime) == 'image/jpeg' or str(type.mime) =='image/png':
                self.showFile(fileName)
                print("image")
            else:
                print("文件格式不符合要求！")
        except:
            pass

    def open_video(self,fileName):#通过启动线程类实现视频的展示
        self.mythread = MyThread(fileName)  # 实例化自己建立的任务线程类
        self.mythread.moveToThread(self.mythread)
        # self.mythread.endsignal.connect(self.wait_function)
        # 启动线程
        self.mythread.start()
        self.mythread.signal.connect(self.image_callback)  # 设置任务线程发射信号触发的函数

    def image_callback(self,image):
        try:
            self.display(image)
        except:
            pass

    # 将指定的图片文件显示在label
    def showFile(self,fileName):
        srcImage = cv2.imdecode(np.fromfile(fileName, dtype=np.uint8), -1)
        self.display(srcImage)

    #展示视频帧到label
    def display(self, srcImage):
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
        QtWidgets.QApplication.processEvents()


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())