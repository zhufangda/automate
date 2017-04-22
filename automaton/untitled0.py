# -*- coding: utf-8 -*-
"""第一个程序"""
#from PyQt5 import QtWidgets
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,QLabel,
    QAction, QFileDialog, QApplication,QDialog,QGridLayout,
    QLineEdit,QSpinBox,QDialogButtonBox,QSizePolicy,QVBoxLayout,QSpacerItem,QListWidget,QListWidgetItem,QMessageBox)
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
class myDialog(QDialog):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(myDialog, self).__init__(arg)
        self.setWindowTitle("first window")
        self.resize(400,300);
        conLayout = QVBoxLayout()
        self.lv = QListWidget()
        #排序
        self.lv.setSortingEnabled(1)
        item = ['OaK','Banana','Apple','Orange','Grapes','Jayesh']
        #创建列表项
        listItem = []
        for lst in item:
            listItem.append(QListWidgetItem(self.tr(lst)))
        #把列表项添加到listwidget中
        for i in range(len(listItem)):
            self.lv.insertItem(i+1,listItem[i])
        conLayout.addWidget(self.lv)
        self.setLayout(conLayout)
        self.lv.itemClicked.connect(self.clickitem)
    def clickitem(self,obj):
        print(obj.text())
        QMessageBox.warning(self,"警告",obj.text(),QMessageBox.Yes)
app = QApplication(sys.argv)
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()