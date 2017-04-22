#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,QLabel,
    QAction, QFileDialog, QApplication,QDialog,QGridLayout,
    QLineEdit,QSpinBox,QDialogButtonBox,QSizePolicy,QVBoxLayout,QSpacerItem)
from PyQt5.QtGui import QIcon,QListWidget


from automate import Automate


class WindowsFrame(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.automate = Automate()


    def initUI(self):
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.listWidget = QListWidget()
        
        reconnuAction = QAction(QIcon('reconnu.png'),'&Reconnaitre',self)
        reconnuAction.setShortcut('Ctrl+R')
        reconnuAction.setStatusTip('Reconnaire une texte')
        reconnuAction.triggered.connect(self.reconnu)
        
        epsilonAction = QAction(QIcon('epsilon.png'),'&Determiniser',self)
        epsilonAction.setShortcut('Ctrl+E')
        epsilonAction.setStatusTip('Enlever les transitions spontanées')
        epsilonAction.triggered.connect(self.epsilon)
        
        determiniserAction = QAction(QIcon('determiniser.png'),'&Determiniser',self)
        determiniserAction.setShortcut('Ctrl+D')
        determiniserAction.setStatusTip('Determiniser cette automate')
        determiniserAction.triggered.connect(self.determiniser)
        
        minimiserAction = QAction(QIcon('minimiser.png'),'&Minimiser',self)
        minimiserAction.setShortcut('Ctrl+M')
        minimiserAction.setStatusTip('minimiser cette automate')
        minimiserAction.triggered.connect(self.minimiser)
        
        openAction = QAction(QIcon('open.png'),'&Open',self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Opne File')
        openAction.triggered.connect(self.showOpenDialog)
        
        saveAction = QAction(QIcon('save.png'),'&Save',self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save File')
        saveAction.triggered.connect(self.showSaveDialog)
        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        self.statusBar().showMessage('Ready')
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        
        self.toolbar = self.addToolBar('open')
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(epsilonAction)
        self.toolbar.addAction(determiniserAction)
        self.toolbar.addAction(minimiserAction)
        self.toolbar.addAction(reconnuAction)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')    
        self.show()
    
    def showOpenDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '../res')

        
        if fname[0]:
            self.automateList = automate.
            self.textEdit.setText(self.automate.__str__())

    def showSaveDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Open file', '../res')

        self.automate.export_XML(fname[0])
    
    def epsilon(self):
        self.automate.getNFA()
        self.textEdit.setText(self.automate.__str__())
        
    def determiniser(self):
        self.automate.determiniser()
        self.textEdit.setText(self.automate.__str__())
        
    def minimiser(self):
        self.automate.minimiser()
        self.textEdit.setText(self.automate.__str__())
    
    def reconnu(self):
        dialog = Dialog(parent=self)
        if dialog.exec_():
            self.model.appendRow((
                    QtGui.QStandardItem(dialog.name()),
                    QtGui.QStandardItem(str(dialog.age())),
                    ))

            dialog.destroy()
 
        
class Dialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(240, 200)
        
        grid = QGridLayout()

        grid.addWidget(QLabel(u'Text', parent=self), 0, 0, 1, 1)
    
        self.leName = QLineEdit(parent=self)
        grid.addWidget(self.leName, 0, 1, 1, 1)
    
        grid.addWidget(QLabel(u'年龄', parent=self), 1, 0, 1, 1)
    
        self.sbAge = QSpinBox(parent=self)
        grid.addWidget(self.sbAge, 1, 1, 1, 1)
        buttonBox = QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal) # 设置为水平方向
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept) # 确定
        buttonBox.rejected.connect(self.reject) # 取消
        

        layout = QVBoxLayout()

        # 加入前面创建的表格布局
        layout.addLayout(grid)

        # 放一个间隔对象美化布局
        spacerItem = QSpacerItem(20, 48, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def name(self):
        return self.leName.text()

    def age(self):
        return self.sbAge.value()


    
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowsFrame()
    sys.exit(app.exec_())