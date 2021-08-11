from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("16-3.ui", self)

        self.BTC.clicked.connect(self.check_BTC)
        self.LTC.clicked.connect(self.check_LTC)
        self.XRP.clicked.connect(self.check_XRP)

    def check_BTC(self):
        price = pyupbit.get_current_price("KRW-BTC")
        self.BTC_price.setText(str(price))

    def check_LTC(self):
        price = pyupbit.get_current_price("KRW-LTC")
        self.LTC_price.setText(str(price))

    def check_XRP(self):
        price = pyupbit.get_current_price("KRW-XRP")
        self.XRP_price.setText(str(price))
            


app = QApplication( [] )
label = MyWindow()
label.show()
app.exec_()