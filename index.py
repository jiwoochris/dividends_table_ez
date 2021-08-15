from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("index.ui", self)

        self.setWindowTitle("Dividends table by Jiwoo")
        self.setWindowIcon(QIcon('dividends_icon.png'))

        self.update_button.clicked.connect(self.update)

        self.upload()

        self.show()

    def update(self):
        dlg = MyApp()
        dlg.exec_()

        self.upload()

    def upload(self):
        balance = 0
        div = 0
        cal = ["", "", "", "", "", "", "", "", "", "", "", ""]
        div_cal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # table 정리

        for i in range(7):
            for j in range(9):
                self.table.setItem(i+1, j+1, None)

        # 목표가

        with open("goals.txt") as f:
            goal = f.readline()
            self.goal.setText("$" + goal)

        # table

        with open("show_table.txt") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                self.table.setItem(int(i/7)+1, (i % 7), QTableWidgetItem(lines[i].strip()))

                # value, 총자산 계산
                if i % 7 == 3:
                    balance += float(lines[i].strip())

                # diviends, 1년 배당금 계산
                if i % 7 == 5:
                    div = div + float(lines[i].strip())

                # 배당 주기, 언제 주는지, 월별 배당금 계산
                if i % 7 == 6:
                    if lines[i].strip() == "monthly": # 월배당
                        for j in range(12):
                            if cal[j] == "":
                                cal[j] = lines[i-5].strip()
                            else:
                                cal[j] = cal[j] + ", " + lines[i-5].strip()
                            div_cal[j] += float(lines[i-2].strip())

                    for j in range(12): # non 월배당
                        if str(j+1) in lines[i].strip()[1:-1].split(", "):
                            if cal[j] == "":
                                cal[j] = lines[i-5].strip()
                                div_cal[j] += float(lines[i-2].strip())
                            else:
                                cal[j] = cal[j] + ", " + lines[i-5].strip()
                                div_cal[j] += float(lines[i-2].strip())

            # 배당 캘린더

            for i in range(12):
                self.calendar.setItem(1, i, QTableWidgetItem(cal[i]))
                self.calendar.setItem(2, i, QTableWidgetItem(f"{div_cal[i] : .3f}"))
            
            self.balance.setText(f"$ {balance : .3f}") # 총 자산
            self.div.setText(f"$ {div : .3f} / $ {div/12 : .3f}") # 1년 / 1달 배당금
            
            if goal != "":
                self.progressBar.setValue(int(div/12 / float(goal.strip()) * 100)) # 1달 목표가 대비 얼마나

            self.calendar.setRowHeight(1, 80)



class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("update.ui", self)

        self.setWindowTitle("Update your account")
        self.setWindowIcon(QIcon('dividends_icon.png'))

        self.update_button.clicked.connect(self.pushButtonClicked)

        # 목표가 수정
        with open("goals.txt") as f:
            line = f.readline()
            if line == "":
                line = "Enter your goals"

        self.goals.setPlaceholderText(line)

        # 포트폴리오 수정
        with open("table.txt") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                self.table.setItem(int(i/2), i % 2, QTableWidgetItem(lines[i].strip()))


    def pushButtonClicked(self):
        import yfinance as yf
        import pandas as pd

        # 목표가 파일 입력
        if self.goals.text() != "":
            with open("goals.txt", "w") as f:
                f.write(self.goals.text())

        # 사용자 table 파일 입력
        with open("table.txt", "w") as f:
            for i in range(20):
                if self.table.item(int(i/2), i % 2) != None:
                    f.write(f"{self.table.item(int(i/2), i % 2).text()}\n")

        # show table 파일 입력
        with open("show_table.txt", "w") as f:
            for i in range(20):
                if self.table.item(int(i/2), i % 2) != None:
                    if self.table.item(int(i/2), i % 2).text() != "":
                        if i % 2 == 0:
                            ticker = yf.Ticker(self.table.item(int(i/2), 0).text())
                            f.write(f"{ticker.info['longName']}\n") # 긴 이름
                            f.write(f"{ticker.info['symbol']}\n") # ticker
                            # print(self.table.item(int(i/2), 0).text())

                        if i % 2 == 1:
                            amount = int(self.table.item(int(i/2), i % 2).text())
                            f.write(f"{amount}\n") # 개수
                            f.write(f"{ticker.info['currentPrice'] * amount : .3f}\n") # values, 자산
                            f.write(f"{amount * ticker.dividends[-1] * 0.85 : .3f}\n") # 월별 배당금 (수수료 포함)

                            # 월 배당
                            if pd.Series(ticker.dividends[-12:].index).dt.month.nunique() == 12:
                                f.write(f"{12* amount * ticker.dividends[-1] * 0.85 : .3f}\n") # 1년 배당금 (수수료 포함)
                                f.write(f"monthly\n") # 배당 주기
                            # non 월 배당
                            else:
                                f.write(f"{pd.Series(ticker.dividends[-4:].index).dt.month.nunique() * amount * ticker.dividends[-1] * 0.85 : .3f}\n") # 1년 배당금 (수수료 포함)
                                f.write(f"{set(pd.Series(ticker.dividends[-4:].index).dt.month)}\n") # 배당 주기
                    
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = MyWindow()
    label.show()
    
    try:
        app.exec_()
    except:
        print("Exiting")