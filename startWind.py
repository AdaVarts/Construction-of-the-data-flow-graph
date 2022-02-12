import sys
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from constructor import Ui_ConstructorWindow
from llvm_parser import parse_llvm
from main import Ui_MainWindow
from first import convert_C_into_llvm
from worker import *

class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.open_main()
        self.threadpool = QThreadPool()
    
    def open_main(self):    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnChooseC.clicked.connect(self.clicked_choose_c_file)
        self.ui.btnChooseLlvm.clicked.connect(self.clicked_choose_llvm_file)
        self.ui.btnConvInLlvm.clicked.connect(self.clicked_convert_into_llvm)
        self.ui.btnBuildDFG.clicked.connect(self.clicked_build_module)

    def clicked_choose_c_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","C Files (*.c)")
        if fileName:
            self.ui.btnConvInLlvm.setEnabled(True)
            self.ui.linePathForC.setText(fileName)
    
    def clicked_choose_llvm_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","LLVM Files (*.ll)")
        if fileName:
            self.ui.btnBuildDFG.setEnabled(True)
            self.ui.linePathForLlvm.setText(fileName)

    def clicked_convert_into_llvm(self):
        worker = Worker(convert_C_into_llvm, self.ui.linePathForC.text())
        worker.signals.result.connect(self.save)
        worker.signals.progress.connect(self.reportProgress)
        self.threadpool.start(worker)

    def save(self, result):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', "","LLVM Files (*.ll)")
        if result is not None:
            with open(fileName, "w") as f1:
                f1.write(result)
        self.ui.linePathForC.setText('')
        self.ui.btnConvInLlvm.setEnabled(False)

    def reportProgress(self, s):
        self.ui.textPrint.append(s)

    
    def clicked_build_module(self):
        # self.ui.btnBuildDFG.setEnabled = False
        worker = Worker(parse_llvm, self.ui.linePathForLlvm.text())
        worker.signals.result.connect(self.open_constructW)
        worker.signals.progress.connect(self.reportProgress)
        self.threadpool.start(worker)
    
    def open_constructW(self, fs):
        self.ui = Ui_ConstructorWindow()
        self.ui.setupUi(self, fs)
        # self.ui.butAdd.clicked.connect(self.clicked_add_product)
        # self.ui.tableWidget.itemDoubleClicked.connect(self.clicked_open_product)
        # self.ui.butHome.clicked.connect(self.open_main)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())
