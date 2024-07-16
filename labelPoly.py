from PyQt5 import QtWidgets, QtCore

from design import Ui_LabelPoly
import sys


class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_LabelPoly()
        self.ui.setupUi(self)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def closeEvent(self, event):
        self.ui.image_inspector.current = None
        event.accept()


app = QtWidgets.QApplication([])
application = Window()
application.show()

sys.exit(app.exec())
