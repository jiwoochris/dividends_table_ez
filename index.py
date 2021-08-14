from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("index.ui", self)

        self.update_button.clicked.connect(self.update)

        self.update_goals()
        self.update_table()

        self.show()

    def update(self):
        dlg = MyApp()
        dlg.exec_()

        self.update_goals()
        self.update_table()

        # self.widget= MyApp()
        # self.widget.show()

    def update_goals(self):
        with open("goals.txt") as f:
            self.goal.setText("$" + f.readline())

    def update_table(self):
        with open("table.txt") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                self.table.setItem(int(i/2)+1, (i % 2) +1, QTableWidgetItem(lines[i].strip()))


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
        if self.goals.text() != "":
            with open("goals.txt", "w") as f:
                f.write(self.goals.text())

        with open("table.txt", "w") as f:
            for i in range(20):
                if self.table.item(int(i/2), i % 2) != None:
                    f.write(f"{self.table.item(int(i/2), i % 2).text()}\n")

        for i in range(20):
            if self.table.item(int(i/2), i % 2) != None:
                print(self.table.item(int(i/2), i % 2).text())

        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = MyWindow()
    label.show()
    
    try:
        app.exec_()
    except:
        print("Exiting")