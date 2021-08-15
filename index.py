from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("index.ui", self)

        self.update_button.clicked.connect(self.update)

        self.upload()

        self.show()

    def update(self):
        dlg = MyApp()
        dlg.exec_()

        self.upload()

        # self.widget= MyApp()
        # self.widget.show()

    def upload(self):
        balance = 0
        div = 0
        cal = ["", "", "", "", "", "", "", "", "", "", "", ""]
        div_cal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for i in range(7):
            for j in range(9):
                self.table.setItem(i+1, j+1, None)

        # self.table.clear()
        # self.table.setItem(0, 0, QTableWidgetItem("long name"))

        with open("goals.txt") as f:
            goal = f.readline()
            self.goal.setText("$" + goal)

        with open("show_table.txt") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                self.table.setItem(int(i/7)+1, (i % 7), QTableWidgetItem(lines[i].strip()))
                if i % 7 == 3:
                    balance += float(lines[i].strip())
                if i % 7 == 5:
                    div = div + float(lines[i].strip())
                if i % 7 == 6:
                    if lines[i].strip() == "monthly":
                        for j in range(12):
                            if cal[j] == "":
                                cal[j] = lines[i-5].strip()
                            else:
                                cal[j] = cal[j] + ", " + lines[i-5].strip()
                            div_cal[j] += float(lines[i-2].strip())


                    for j in range(12):
                        if str(j+1) in lines[i].strip()[1:-1].split(", "):
                            if cal[j] == "":
                                cal[j] = lines[i-5].strip()
                                div_cal[j] += float(lines[i-2].strip())
                            else:
                                cal[j] = cal[j] + ", " + lines[i-5].strip()
                                div_cal[j] += float(lines[i-2].strip())
                
            print(cal)

            for i in range(12):
                self.calendar.setItem(1, i, QTableWidgetItem(cal[i]))
                self.calendar.setItem(2, i, QTableWidgetItem(f"{div_cal[i] : .3f}"))
            
            self.balance.setText(f"$ {balance : .3f}")
            self.div.setText(f"$ {div : .3f} / $ {div/12 : .3f}")

            self.progressBar.setValue(int(div/12 / float(goal.strip()) * 100))

            self.calendar.setRowHeight(1, 80)
            



class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("update.ui", self)

        self.update_button.clicked.connect(self.pushButtonClicked)

        with open("goals.txt") as f:
            line = f.readline()
            if line == "":
                line = "Enter your goals"

        self.goals.setPlaceholderText(line)

        with open("table.txt") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                self.table.setItem(int(i/2), i % 2, QTableWidgetItem(lines[i].strip()))


    def pushButtonClicked(self):
        import yfinance as yf
        import pandas as pd

        if self.goals.text() != "":
            with open("goals.txt", "w") as f:
                f.write(self.goals.text())

        with open("table.txt", "w") as f:
            for i in range(20):
                if self.table.item(int(i/2), i % 2) != None:
                    f.write(f"{self.table.item(int(i/2), i % 2).text()}\n")

        with open("show_table.txt", "w") as f:
            for i in range(20):
                if self.table.item(int(i/2), i % 2) != None:
                    if self.table.item(int(i/2), i % 2).text() != "":
                        print(self.table.item(int(i/2), i % 2).text())
                        if i % 2 == 0:
                            msft = yf.Ticker(self.table.item(int(i/2), 0).text())
                            f.write(f"{msft.info['longName']}\n")
                            f.write(f"{msft.info['symbol']}\n")

                        if i % 2 == 1:
                            amount = int(self.table.item(int(i/2), i % 2).text())
                            f.write(f"{amount}\n")
                            f.write(f"{msft.info['currentPrice'] * amount : .3f}\n")
                            f.write(f"{amount * msft.dividends[-1] * 0.85 : .3f}\n")

                            if pd.Series(msft.dividends[-12:].index).dt.month.nunique() == 12:
                                f.write(f"{12* amount * msft.dividends[-1] : .3f}\n")
                                f.write(f"monthly\n")
                            else:
                                f.write(f"{pd.Series(msft.dividends[-4:].index).dt.month.nunique() * amount * msft.dividends[-1] * 0.85 : .3f}\n")
                                f.write(f"{set(pd.Series(msft.dividends[-4:].index).dt.month)}\n")
                            
                    

        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = MyWindow()
    label.show()
    
    try:
        app.exec_()
    except:
        print("Exiting")