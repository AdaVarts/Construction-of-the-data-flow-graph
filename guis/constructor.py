# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'constructor.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1128, 870)
        MainWindow.setMaximumSize(QtCore.QSize(1130, 870))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listFunctions = QtWidgets.QListView(self.centralwidget)
        self.listFunctions.setGeometry(QtCore.QRect(40, 40, 161, 221))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctions.setFont(font)
        self.listFunctions.setObjectName("listFunctions")
        self.listFunctAdd = QtWidgets.QListView(self.centralwidget)
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
        self.listFunctDel = QtWidgets.QListView(self.centralwidget)
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
        self.listArgs = QtWidgets.QListView(self.centralwidget)
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
        self.listFoundNodes = QtWidgets.QListView(self.centralwidget)
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
        self.btnClearlAdd = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearlAdd.setGeometry(QtCore.QRect(250, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClearlAdd.setFont(font)
        self.btnClearlAdd.setObjectName("btnClearlAdd")
        self.btnClearlDel = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearlDel.setGeometry(QtCore.QRect(460, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClearlDel.setFont(font)
        self.btnClearlDel.setObjectName("btnClearlDel")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(370, 290, 711, 551))
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 21))
        self.menubar.setObjectName("menubar")
        self.menuBack = QtWidgets.QMenu(self.menubar)
        self.menuBack.setObjectName("menuBack")
        MainWindow.setMenuBar(self.menubar)
        self.actionfff = QtWidgets.QAction(MainWindow)
        self.actionfff.setObjectName("actionfff")
        self.actionBack = QtWidgets.QAction(MainWindow)
        self.actionBack.setObjectName("actionBack")
        self.menuBack.addAction(self.actionBack)
        self.menubar.addAction(self.menuBack.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
        self.btnClearlAdd.setText(_translate("MainWindow", "Clear"))
        self.btnClearlDel.setText(_translate("MainWindow", "Clear"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Distance"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "n"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "ec"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("MainWindow", "add"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.menuBack.setTitle(_translate("MainWindow", "Home"))
        self.actionfff.setText(_translate("MainWindow", "fff"))
        self.actionBack.setText(_translate("MainWindow", "Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
