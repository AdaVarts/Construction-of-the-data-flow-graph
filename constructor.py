#
# GUI of second window 
#

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import *

from classes import Function, Worker
from convert_and_dfgBuild import create_dfg, start_DFG
from function_manag import get_ret_values, merge_in_one

class Ui_ConstructorWindow(object):
    def setupUi(self, MainWindow, fs=[]):
        self.fs = fs
        self.function = None
        self.dfg = None

        # Created in: PyQt5 designer
        # Created by: PyQt5 UI code generator 5.15.4 
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 870)
        MainWindow.setMaximumSize(QtCore.QSize(1500, 870))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.listFunctions = QtWidgets.QListWidget(self.centralwidget)
        self.listFunctions.setGeometry(QtCore.QRect(40, 40, 161, 221))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctions.setFont(font)
        self.listFunctions.setObjectName("listFunctions")
        self.gridLayout.addWidget(self.listFunctions, 1, 0, 2, 2)

        self.listFunctAdd = QtWidgets.QListWidget(self.centralwidget)
        self.listFunctAdd.setGeometry(QtCore.QRect(250, 40, 161, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctAdd.setFont(font)
        self.listFunctAdd.setObjectName("listFunctAdd")
        self.gridLayout.addWidget(self.listFunctAdd, 1, 2, 1, 1)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(470, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)

        self.listFunctDel = QtWidgets.QListWidget(self.centralwidget)
        self.listFunctDel.setGeometry(QtCore.QRect(460, 40, 161, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFunctDel.setFont(font)
        self.listFunctDel.setObjectName("listFunctDel")
        self.gridLayout.addWidget(self.listFunctDel, 1, 3, 1, 1)

        self.btnGenerate = QtWidgets.QPushButton(self.centralwidget)
        self.btnGenerate.setGeometry(QtCore.QRect(820, 230, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnGenerate.setFont(font)
        self.btnGenerate.setObjectName("btnGenerate")
        self.gridLayout.addWidget(self.btnGenerate, 2, 4, 1, 1)

        self.textPrint = QtWidgets.QTextEdit(self.centralwidget)
        self.textPrint.setGeometry(QtCore.QRect(690, 40, 391, 171))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textPrint.setFont(font)
        self.textPrint.setReadOnly(True)
        self.textPrint.setObjectName("textPrint")
        self.gridLayout.addWidget(self.textPrint, 1, 4, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 290, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.lineFuncName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineFuncName.setGeometry(QtCore.QRect(180, 290, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineFuncName.setFont(font)
        self.lineFuncName.setReadOnly(True)
        self.lineFuncName.setObjectName("lineFuncName")
        self.gridLayout.addWidget(self.lineFuncName, 3, 1, 1, 2)

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 320, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.lineInstrsNum = QtWidgets.QLineEdit(self.centralwidget)
        self.lineInstrsNum.setGeometry(QtCore.QRect(180, 320, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineInstrsNum.setFont(font)
        self.lineInstrsNum.setReadOnly(True)
        self.lineInstrsNum.setObjectName("lineInstrsNum")
        self.gridLayout.addWidget(self.lineInstrsNum, 4, 1, 1, 2)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(50, 350, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.listArgs = QtWidgets.QListWidget(self.centralwidget)
        self.listArgs.setGeometry(QtCore.QRect(180, 350, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listArgs.setFont(font)
        self.listArgs.setObjectName("listArgs")
        self.gridLayout.addWidget(self.listArgs, 5, 1, 2, 2)

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 6, 0, 1, 1)

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(50, 440, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 8, 0, 1, 1)

        self.listReturnValues = QtWidgets.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listReturnValues.setFont(font)
        self.listReturnValues.setObjectName("listReturnValues")
        self.gridLayout.addWidget(self.listReturnValues, 7, 1, 2, 2)

        self.lineDistance = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDistance.setGeometry(QtCore.QRect(180, 470, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineDistance.setFont(font)
        self.lineDistance.setObjectName("lineDistance")
        self.onlyInt = QIntValidator()
        self.lineDistance.setValidator(self.onlyInt)
        self.gridLayout.addWidget(self.lineDistance, 9, 1, 1, 2)

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(50, 470, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)

        self.btnFindNodes = QtWidgets.QPushButton(self.centralwidget)
        self.btnFindNodes.setGeometry(QtCore.QRect(130, 510, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnFindNodes.setFont(font)
        self.btnFindNodes.setObjectName("btnFindNodes")
        self.gridLayout.addWidget(self.btnFindNodes, 10, 1, 1, 2)

        self.labelNodes = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelNodes.setFont(font)
        self.labelNodes.setObjectName("labelNodes")
        self.gridLayout.addWidget(self.labelNodes, 11, 0, 1, 1)
        self.lineNodes = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineNodes.setFont(font)
        self.lineNodes.setReadOnly(True)
        self.lineNodes.setObjectName("lineNodes")
        self.gridLayout.addWidget(self.lineNodes, 11, 1, 1, 2)
        self.labelEdges = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelEdges.setFont(font)
        self.labelEdges.setObjectName("labelEdges")
        self.gridLayout.addWidget(self.labelEdges, 12, 0, 1, 1)
        self.lineEdges = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdges.setFont(font)
        self.lineEdges.setReadOnly(True)
        self.lineEdges.setObjectName("lineEdges")
        self.gridLayout.addWidget(self.lineEdges, 12, 1, 1, 2)

        self.lineNodesNum = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNodesNum.setGeometry(QtCore.QRect(220, 570, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineNodesNum.setFont(font)
        self.lineNodesNum.setReadOnly(True)
        self.lineNodesNum.setObjectName("lineNodesNum")
        self.gridLayout.addWidget(self.lineNodesNum, 13, 2, 1, 1)

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(50, 560, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 13, 0, 1, 2)

        self.listFoundNodes = QtWidgets.QListWidget(self.centralwidget)
        self.listFoundNodes.setGeometry(QtCore.QRect(50, 610, 281, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listFoundNodes.setFont(font)
        self.listFoundNodes.setObjectName("listFoundNodes")
        self.gridLayout.addWidget(self.listFoundNodes, 14, 0, 1, 3)

        self.btnDisplayDFG = QtWidgets.QPushButton(self.centralwidget)
        self.btnDisplayDFG.setGeometry(QtCore.QRect(120, 810, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnDisplayDFG.setFont(font)
        self.btnDisplayDFG.setObjectName("btnDisplayDFG")
        self.btnDisplayDFG.setEnabled(False)
        self.gridLayout.addWidget(self.btnDisplayDFG, 15, 0, 1, 3)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.actionBack = QtWidgets.QAction(MainWindow)
        self.actionBack.setObjectName("actionBack")

        self.menubar.addAction(self.actionBack)

        self.btnClearlAdd = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearlAdd.setGeometry(QtCore.QRect(250, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClearlAdd.setFont(font)
        self.btnClearlAdd.setObjectName("btnClearlAdd")
        self.gridLayout.addWidget(self.btnClearlAdd, 2, 2, 1, 1)
        self.btnClearlAdd.clicked.connect(self.unselectAdd)

        self.btnClearlDel = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearlDel.setGeometry(QtCore.QRect(460, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClearlDel.setFont(font)
        self.btnClearlDel.setObjectName("btnClearlDel")
        self.gridLayout.addWidget(self.btnClearlDel, 2, 3, 1, 1)

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
        self.gridLayout.addWidget(self.tableWidget, 3, 3, 13, 2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Set all functions from uploaded LLVM module
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
        self.label_21.setText(_translate("MainWindow", "            \n\n"))
        self.btnDisplayDFG.setText(_translate("MainWindow", "Display path"))
        self.btnClearlDel.setText(_translate("MainWindow", "Clear"))
        self.btnClearlAdd.setText(_translate("MainWindow", "Clear"))
        self.labelNodes.setText(_translate("MainWindow", "Nodes"))
        # self.labelEdges_2.setText(_translate("MainWindow", "   "))
        self.labelEdges.setText(_translate("MainWindow", "Edges"))
        # self.menuBack.setTitle(_translate("MainWindow", "Home"))
        self.actionBack.setText(_translate("MainWindow", "Back"))
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

    # Merging other functions into main one and deleting the marked ones
    def generate(self):
        self.dfg = None
        self.lineFuncName.setText('')
        self.lineInstrsNum.setText('')
        self.lineDistance.setText('')
        self.listArgs.clear()
        self.listReturnValues.clear()
        # self.lineRetValue.setText('')
        self.listFoundNodes.clear()
        self.lineNodesNum.setText('')
        self.lineNodes.setText('')
        self.lineEdges.setText('')

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
    
    # Set information about final function
    def set_all(self, result: Function):
        if len(result.labels) > 1:
            self.textPrint.append(f"Error: chosen function {result.name} has more than 1 label")
            self.textPrint.append(f"Choose another function")
            return
        self.function = result
        self.textPrint.append("")
        self.lineFuncName.setText(result.name)
        self.lineInstrsNum.setText(str(len(result.labels[0].operations)))
        self.listArgs.addItems(result.params)
        if result.labels[0].operations[-1].args[0] == '':
            self.btnDisplayDFG.setEnabled(False)
            self.btnFindNodes.setEnabled(False)
            self.btnGenerate.setEnabled(False)
            worker = Worker(get_ret_values, result)
            worker.signals.result.connect(self.set_return_val)
            worker.signals.progress.connect(self.reportProgress)
            self.threadpool.start(worker)
        else:
            self.listReturnValues.addItem(result.labels[0].operations[-1].args[0])

    # Set returning values of final function
    def set_return_val(self, ret_values):
        self.listReturnValues.addItems(ret_values)
        self.btnGenerate.setEnabled(True)
        self.btnDisplayDFG.setEnabled(True)
        self.btnFindNodes.setEnabled(True)

    # Search for nodes at entered distance, if dfg is not created yet -> construct a dfg
    def find_nodes(self):
        distance = self.lineDistance.text()
        self.listFoundNodes.clear()
        self.lineNodesNum.setText('')
        if distance and self.function is not None:
            self.btnDisplayDFG.setEnabled(False)
            self.btnFindNodes.setEnabled(False)
            self.btnGenerate.setEnabled(False)
            worker = Worker(create_dfg, self.function)
            worker.signals.result.connect(self.save_dfg)
            worker.signals.progress.connect(self.reportProgress)
            self.threadpool.start(worker)

    # Save constructed dfg and set information about it
    def save_dfg(self, dfg):
        self.dfg = dfg
        self.lineNodes.setText(str(len(dfg.nodes)))
        self.lineEdges.setText(str(len(dfg.edges)))
        distance = self.lineDistance.text()
        if self.listReturnValues.count() == 0:
            self.btnDisplayDFG.setEnabled(True)
            self.btnFindNodes.setEnabled(True)
            self.btnGenerate.setEnabled(True)
            return
        ret_val = self.listReturnValues.selectedItems()[0].text() if len(self.listReturnValues.selectedItems()) == 1 \
            else self.listReturnValues.item(0).text()
        worker = Worker(start_DFG, self.dfg, self.function, distance, ret_val)
        worker.signals.result.connect(self.display_nodes)
        worker.signals.progress.connect(self.reportProgress)
        self.threadpool.start(worker)
    
    # Display the found nodes at entered distance
    def display_nodes(self, dfg):
        if dfg != []:
            self.dfg = dfg
            self.listFoundNodes.clear()
            self.lineNodesNum.setText(str(len(self.dfg.map_path.keys())))
            for node, value in self.dfg.map_path.items():
                for val in value:
                    self.listFoundNodes.addItem(str(node))
        else:
            self.textPrint.append(f"Error: path was not found")
        self.btnDisplayDFG.setEnabled(True)
        self.btnFindNodes.setEnabled(True)
        self.btnGenerate.setEnabled(True)
    
    # Display the path from chosen node to a returning variable in the table
    def show_dfg_path(self):
        if len(self.listFoundNodes.selectedItems()) == 1 and self.dfg is not None:
            distance = self.lineDistance.text()
            value = self.listFoundNodes.selectedItems()[0].text()

            index = self.listFoundNodes.selectedIndexes()[0].row()
            number = 0
            for i in range(0, index):
                if self.listFoundNodes.item(i).text() == value:
                    number += 1

            nodes = self.dfg.map_path[value][number]
            self.display_path(nodes)
    
    # Displaying path in the table
    def display_path(self, nodes):
        x = 0
        for node in nodes[::-1]:
            key = node[0]
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
            item4.setText(node[1].name)
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
            item7.setText(node[2].name)
            item7.setTextAlignment(Qt.AlignCenter)
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
