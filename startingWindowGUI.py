from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 870)
        MainWindow.setMaximumSize(QtCore.QSize(1500, 870))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.btnChooseC = QtWidgets.QPushButton(self.centralwidget)
        self.btnChooseC.setGeometry(QtCore.QRect(650, 40, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnChooseC.setFont(font)
        self.btnChooseC.setObjectName("btnChooseC")

        self.linePathForC = QtWidgets.QLineEdit(self.centralwidget)
        self.linePathForC.setGeometry(QtCore.QRect(20, 40, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.linePathForC.setFont(font)
        self.linePathForC.setReadOnly(True)
        self.linePathForC.setObjectName("linePathForC")

        self.btnBuildDFG = QtWidgets.QPushButton(self.centralwidget)
        self.btnBuildDFG.setEnabled(False)
        self.btnBuildDFG.setGeometry(QtCore.QRect(270, 250, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnBuildDFG.setFont(font)
        self.btnBuildDFG.setObjectName("btnBuildDFG")

        self.btnConvInLlvm = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvInLlvm.setEnabled(False)
        self.btnConvInLlvm.setGeometry(QtCore.QRect(270, 90, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnConvInLlvm.setFont(font)
        self.btnConvInLlvm.setObjectName("btnConvInLlvm")

        self.linePathForLlvm = QtWidgets.QLineEdit(self.centralwidget)
        self.linePathForLlvm.setGeometry(QtCore.QRect(20, 200, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.linePathForLlvm.setFont(font)
        self.linePathForLlvm.setReadOnly(True)
        self.linePathForLlvm.setObjectName("linePathForLlvm")
        
        self.btnChooseLlvm = QtWidgets.QPushButton(self.centralwidget)
        self.btnChooseLlvm.setGeometry(QtCore.QRect(650, 200, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnChooseLlvm.setFont(font)
        self.btnChooseLlvm.setObjectName("btnChooseLlvm")

        self.textPrint = QtWidgets.QTextEdit(self.centralwidget)
        self.textPrint.setEnabled(True)
        self.textPrint.setGeometry(QtCore.QRect(760, 40, 350, 211))
        self.textPrint.setMaximumSize(QtCore.QSize(441, 211))
        self.textPrint.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textPrint.setFont(font)
        self.textPrint.setObjectName("textPrint")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 170, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DFGConstructor"))
        self.btnChooseC.setText(_translate("MainWindow", "Choose file"))
        self.btnBuildDFG.setText(_translate("MainWindow", "Load LLVM module"))
        self.btnConvInLlvm.setText(_translate("MainWindow", "Convert into LLVM IR"))
        self.btnChooseLlvm.setText(_translate("MainWindow", "Choose file"))
        self.label.setText(_translate("MainWindow", "Load file in C"))
        self.label_2.setText(_translate("MainWindow", "Load file in LLVM format"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())