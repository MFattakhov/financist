from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton, QScrollArea, \
    QHBoxLayout, QLabel, QInputDialog
from PyQt5.QtGui import QIcon
from add_line import lining
from add_date import dating
from PyQt5 import QtCore
import sys


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.my_balance = 0
        self.database = ['zero']
        self.setGeometry(450, 200, 400, 400)
        self.setWindowIcon(QIcon('icon.png'))

        self.topLayout = QHBoxLayout()
        self.topLayout.setGeometry(QtCore.QRect(5, 5, 390, 50))
        self.mainLayout = QVBoxLayout()

        self.btn = QPushButton(self)
        self.btn.setText("Доход")
        self.btn.clicked.connect(self.btn_plus_money)

        self.btn_2 = QPushButton(self)
        self.btn_2.setText("Расход")
        self.btn_2.clicked.connect(self.btn_minus_money)

        self.itemsLayout = QVBoxLayout()

        self.itemsLayout.addWidget(lining())

        with open('database.txt', 'r') as file:
            file = open('database.txt', 'r')
            if file.read():
                file.close()
                with open('database.txt', 'r') as f:
                        self.database = f.readline().split('#')

                        for widget in self.database[1:]:
                            widget = widget.split()
                            corrective = QHBoxLayout()
                            corrective.addWidget(QLabel(widget[0]))
                            corrective.addWidget(QLabel(widget[-1]))
                            self.itemsLayout.addLayout(corrective)
                            self.itemsLayout.addWidget(lining())

                        self.my_balance = int(self.database[0])

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.itemsLayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.balance = QLabel(f'Ваш Баланс: {str(self.my_balance)}', self)

        self.topLayout.addWidget(self.btn)
        self.topLayout.addWidget(self.btn_2)
        self.topLayout.addWidget(self.balance)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def btn_plus_money(self):
        corrective = QHBoxLayout()
        self.show_dialog_for_plus()
        date = QLabel(dating(), self)
        corrective.addWidget(date)
        corrective.addWidget(self.profit)
        self.itemsLayout.addLayout(corrective)
        self.itemsLayout.addWidget(lining())

    def show_dialog_for_plus(self):
        cash, ok = QInputDialog.getText(self, 'Доход', 'Сколько получили?')

        if ok:
            print(self.database)
            self.profit = QLabel(f'+{str(cash)}', self)
            self.my_balance += int(cash)
            self.balance.setText(f'Ваш баланс: {str(self.my_balance)}')
            self.database[0] = str(self.my_balance)
            self.database.append(' '.join([dating(), f'+{cash}']))
            f = open('database.txt', 'w')
            f.write('#'.join(self.database))
            f.close()

    def btn_minus_money(self):
        corrective = QHBoxLayout()
        self.show_dialog_for_minus()
        date = QLabel(dating(), self)
        corrective.addWidget(date)
        corrective.addWidget(self.outgo)
        self.itemsLayout.addLayout(corrective)
        self.itemsLayout.addWidget(lining())

    def show_dialog_for_minus(self):
        cash, ok = QInputDialog.getText(self, 'Расход', 'Сколько потратили?')

        if ok:
            self.outgo = QLabel(f'-{str(cash)}', self)
            self.my_balance -= int(cash)
            self.balance.setText(f'Ваш баланс: {str(self.my_balance)}')
            self.database[0] = str(self.my_balance)
            self.database.append(' '.join([dating(), f'-{cash}']))
            f = open('database.txt', 'w')
            f.write('#'.join(self.database))
            f.close()


if __name__ == '__main__':
    my_balance = 0
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
