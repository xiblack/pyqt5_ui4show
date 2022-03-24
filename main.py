# 安装python中qt的对应库 ，终端执行：pip install pyqt5 pyqt5-tools
from PyQt5 import QtWidgets
from a import Ui_MainWindow


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    #初始化,
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)

        '''下面连接动作对应的函数'''
        self.pushButton.clicked.connect(self.writeline)#按钮一连接openFile函数

    def writeline(self):
        #选择且获取图片文件的地址
       print("按下按钮")


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())