from PyQt5.QtCore import *

class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    progress = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, fn, *args):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    def run(self):
        m = self.fn(*self.args, self.signals.progress)
        self.signals.result.emit(m)
        self.signals.finished.emit()
