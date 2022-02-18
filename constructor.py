# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'constructor.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QListWidgetItem

from classes import Function
from first import create_dfg, get_path, start_DFG
from function_manag import merge_in_one
from worker import *

class Ui_ConstructorWindow(object):
    def setupUi(self, MainWindow, fs=[]):
        self.fs = fs
        self.function = None
        self.dfg = None

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 870)
        MainWindow.setMaximumSize(QtCore.QSize(1130, 870))
        MainWindow.setMinimumSize(QtCore.QSize(1130, 870))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.listFunctions = QtWidgets.QListWidget(self.centralwidget)
        self.listFunctions.setGeometry(QtCore.QRect(40, 40, 161, 221))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctions.setFont(font)
        self.listFunctions.setObjectName("listFunctions")

        self.listFunctAdd = QtWidgets.QListWidget(self.centralwidget)
        self.listFunctAdd.setGeometry(QtCore.QRect(250, 40, 161, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctAdd.setFont(font)
        self.listFunctAdd.setObjectName("listFunctAdd")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(470, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.listFunctDel = QtWidgets.QListWidget(self.centralwidget)
        self.listFunctDel.setGeometry(QtCore.QRect(460, 40, 161, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctDel.setFont(font)
        self.listFunctDel.setObjectName("listFunctDel")

        self.btnGenerate = QtWidgets.QPushButton(self.centralwidget)
        self.btnGenerate.setGeometry(QtCore.QRect(820, 230, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnGenerate.setFont(font)
        self.btnGenerate.setObjectName("btnGenerate")

        self.textPrint = QtWidgets.QTextEdit(self.centralwidget)
        self.textPrint.setGeometry(QtCore.QRect(690, 40, 391, 171))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textPrint.setFont(font)
        self.textPrint.setObjectName("textPrint")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 290, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.lineFuncName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineFuncName.setGeometry(QtCore.QRect(180, 290, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineFuncName.setFont(font)
        self.lineFuncName.setReadOnly(True)
        self.lineFuncName.setObjectName("lineFuncName")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 320, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.lineInstrsNum = QtWidgets.QLineEdit(self.centralwidget)
        self.lineInstrsNum.setGeometry(QtCore.QRect(180, 320, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineInstrsNum.setFont(font)
        self.lineInstrsNum.setReadOnly(True)
        self.lineInstrsNum.setObjectName("lineInstrsNum")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(50, 350, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.listArgs = QtWidgets.QListWidget(self.centralwidget)
        self.listArgs.setGeometry(QtCore.QRect(180, 350, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listArgs.setFont(font)
        self.listArgs.setObjectName("listArgs")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(50, 440, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.lineRetValue = QtWidgets.QLineEdit(self.centralwidget)
        self.lineRetValue.setGeometry(QtCore.QRect(180, 440, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineRetValue.setFont(font)
        self.lineRetValue.setReadOnly(True)
        self.lineRetValue.setObjectName("lineRetValue")

        self.lineDistance = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDistance.setGeometry(QtCore.QRect(180, 470, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineDistance.setFont(font)
        self.lineDistance.setObjectName("lineDistance")
        self.onlyInt = QIntValidator()
        self.lineDistance.setValidator(self.onlyInt)

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(50, 470, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")

        self.btnFindNodes = QtWidgets.QPushButton(self.centralwidget)
        self.btnFindNodes.setGeometry(QtCore.QRect(130, 510, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnFindNodes.setFont(font)
        self.btnFindNodes.setObjectName("btnFindNodes")

        self.lineNodesNum = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNodesNum.setGeometry(QtCore.QRect(220, 570, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineNodesNum.setFont(font)
        self.lineNodesNum.setReadOnly(True)
        self.lineNodesNum.setObjectName("lineNodesNum")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(50, 560, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.listFoundNodes = QtWidgets.QListWidget(self.centralwidget)
        self.listFoundNodes.setGeometry(QtCore.QRect(50, 610, 281, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFoundNodes.setFont(font)
        self.listFoundNodes.setObjectName("listFoundNodes")

        self.btnDisplayDFG = QtWidgets.QPushButton(self.centralwidget)
        self.btnDisplayDFG.setGeometry(QtCore.QRect(120, 810, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnDisplayDFG.setFont(font)
        self.btnDisplayDFG.setObjectName("btnDisplayDFG")
        self.btnDisplayDFG.setEnabled = False
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 21))
        self.menubar.setObjectName("menubar")
        self.menuBack = QtWidgets.QMenu(self.menubar)
        self.menuBack.setObjectName("menuBack")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuBack.menuAction())

        self.btnClearlAdd = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearlAdd.setGeometry(QtCore.QRect(250, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClearlAdd.setFont(font)
        self.btnClearlAdd.setObjectName("btnClearlAdd")
        self.btnClearlAdd.clicked.connect(self.unselectAdd)

        self.btnClearlDel = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearlDel.setGeometry(QtCore.QRect(460, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClearlDel.setFont(font)
        self.btnClearlDel.setObjectName("btnClearlDel")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(370, 290, 711, 551))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for f in self.fs:
            self.listFunctions.addItem(f.name)
            self.listFunctAdd.addItem(f.name)
            self.listFunctDel.addItem(f.name)
        self.listFunctAdd.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.listFunctDel.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        
        self.btnClearlDel.clicked.connect(self.unselectDel)
        self.btnGenerate.clicked.connect(self.generate)
        self.btnFindNodes.clicked.connect(self.find_nodes)
        self.btnDisplayDFG.clicked.connect(self.show_dfg_path)

        self.threadpool = QThreadPool()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DFGConstructor"))
        self.label.setText(_translate("MainWindow", "Main function for DFG:"))
        self.label_2.setText(_translate("MainWindow", "Functions to add:"))
        self.label_3.setText(_translate("MainWindow", "Functions to exclude:"))
        self.btnGenerate.setText(_translate("MainWindow", "Generate model"))
        self.label_4.setText(_translate("MainWindow", "Function"))
        self.label_5.setText(_translate("MainWindow", "Instructions"))
        self.label_6.setText(_translate("MainWindow", "Arguments"))
        self.label_7.setText(_translate("MainWindow", "Return value"))
        self.label_8.setText(_translate("MainWindow", "Distance"))
        self.btnFindNodes.setText(_translate("MainWindow", "Find nodes"))
        self.label_9.setText(_translate("MainWindow", "Nodes on entered distance\n"
"from return value"))
        self.btnDisplayDFG.setText(_translate("MainWindow", "Display DFG"))
        self.btnClearlDel.setText(_translate("MainWindow", "Clear"))
        self.btnClearlAdd.setText(_translate("MainWindow", "Clear"))
        self.menuBack.setTitle(_translate("MainWindow", "Back"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Distance"))
    
    def unselectAdd(self):
        self.listFunctAdd.clearSelection()
        self.listFunctAdd.clearFocus()

    def unselectDel(self):
        self.listFunctDel.clearSelection()
        self.listFunctDel.clearFocus()

    def generate(self):
        self.dfg = None
        self.lineFuncName.setText('')
        self.lineInstrsNum.setText('')
        self.lineDistance.setText('')
        self.listArgs.clear()
        self.lineRetValue.setText('')
        self.listFoundNodes.clear()

        if len(self.listFunctions.selectedItems()) == 1:
            addf = self.listFunctAdd.selectedItems()
            delf = self.listFunctDel.selectedItems()
            worker = Worker(merge_in_one, self.fs, self.listFunctions.selectedItems()[0].text(),
                            [a.text() for a in addf], [d.text() for d in delf])
            worker.signals.result.connect(self.set_all)
            worker.signals.progress.connect(self.reportProgress)
            self.threadpool.start(worker)

    def reportProgress(self, progress):
        self.textPrint.append(progress)
    
    def set_all(self, result: Function):
        self.function = result
        self.textPrint.append("")
        self.lineFuncName.setText(result.name)
        self.lineInstrsNum.setText(str(len(result.labels[0].operations)))
        self.listArgs.addItems(result.params)
        self.lineRetValue.setText(result.labels[0].operations[-1].args[0])

    def find_nodes(self):
        distance = self.lineDistance.text()
        if distance and self.function is not None:
            worker = Worker(create_dfg, self.function)
            worker.signals.result.connect(self.save_dfg)
            worker.signals.progress.connect(self.reportProgress)
            self.threadpool.start(worker)

    def save_dfg(self, dfg):
        self.dfg = dfg

        distance = self.lineDistance.text()
        worker = Worker(start_DFG, self.dfg, self.function, distance, self.lineRetValue.text())
        worker.signals.result.connect(self.display_nodes)
        worker.signals.progress.connect(self.reportProgress)
        self.threadpool.start(worker)
    
    def display_nodes(self, nodes):
        self.listFoundNodes.clear()
        self.lineNodesNum.setText(str(len(nodes)))
        for node in nodes:
            self.listFoundNodes.addItem(str(node))
    
    def show_dfg_path(self):
        if len(self.listFoundNodes.selectedItems()) == 1 and self.dfg is not None:
            distance = self.lineDistance.text()
            value = self.listFoundNodes.selectedItems()[0].text()

            index = self.listFoundNodes.selectedIndexes()[0].row()
            number = 1
            for i in range(0, index):
                if self.listFoundNodes.item(i).text() == value:
                    number += 1

            worker = Worker(get_path, self.dfg, distance, value, self.lineRetValue.text(), number)
            worker.signals.result.connect(self.display_path)
            worker.signals.progress.connect(self.reportProgress)
            self.threadpool.start(worker)
    
    def display_path(self, nodes):
        x = 0
        for key, node in nodes.items():
            print(str(key)+"  "+node.__str__())
            self.tableWidget.setRowCount(x+2)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(x, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(x+1, item)

            item3 = QtWidgets.QTableWidgetItem()
            item3.setTextAlignment(Qt.AlignCenter)
            item3.setText("n")
            self.tableWidget.setItem(x, 0, item3)

            item4 = QtWidgets.QTableWidgetItem()
            item4.setText(node[0].name)
            self.tableWidget.setItem(x, 1, item4)
            item5 = QtWidgets.QTableWidgetItem()
            item5.setText(str(key))
            item5.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(x, 2, item5)

            item6 = QtWidgets.QTableWidgetItem()
            item6.setText("e")
            item6.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(x+1, 0, item6)
            item7 = QtWidgets.QTableWidgetItem()
            item7.setText(node[1].name)
            self.tableWidget.setItem(x+1, 1, item7)

            x += 2
        
            
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ConstructorWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
