from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("index.ui", self)

        self.update_button.clicked.connect(self.update)

        self.show()

    def update(self):
        self.widget= MyApp()
        self.widget.show()




class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("change.ui", self)

        self.update_button.clicked.connect(self.update)
    
    def update(self):
        print(self.goals.text())
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = MyWindow()
    label.show()
    
    try:
        app.exec_()
    except:
        print("Exiting")