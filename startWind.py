import sys
import threading
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import Ui_MainWindow
from first import convert_C_into_llvm


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

class MainWin(QtWidgets.QMainWindow):
    

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.open_main()
    
    def open_main(self):    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnChooseC.clicked.connect(self.clicked_choose_c_file)
        self.ui.btnChooseLlvm.clicked.connect(self.clicked_choose_llvm_file)
        self.ui.btnConvInLlvm.clicked.connect(self.clicked_convert_into_llvm)

    def clicked_choose_c_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","C Files (*.c)", options=options)
        if fileName:
            # self.ui.btnBuildDFG.setEnabled(True)
            self.ui.btnConvInLlvm.setEnabled(True)
            self.ui.linePathForC.setText(fileName)
    
    def clicked_choose_llvm_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","LLVM Files (*.ll)", options=options)
        if fileName:
            self.ui.btnBuildDFG.setEnabled(True)
            self.ui.linePathForLlvm.setText(fileName)

    def call_convert_into_llvm(self, filename):
        return convert_C_into_llvm(filename)

    def clicked_convert_into_llvm(self):
        x = ThreadWithReturnValue(target=self.call_convert_into_llvm, args=(self.ui.linePathForC.text(),))
        x.start()
        m = x.join()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', "","LLVM Files (*.ll)", options=options)
        if m is not None:
            with open(fileName, "w") as f1:
                f1.write(m)
        self.ui.linePathForC.setText('')


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())
