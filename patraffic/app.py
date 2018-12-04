import sys
import time

import random
from patraffic import SimpleGrid
from patraffic.cell import ConwayCell
from patraffic.utils import list2

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def main():
    """ Application entry point
    """

    width = 17
    height = 17

    # init_cond = list2(width, height, init=0)
    # toggle = [(6,6), (6,7), (6,8), (6,9), (6,10), (10,6), (10,7), (10,8), (10,9), (10,10), (8,6), (8,10)]
    # for x,y in toggle:
    #     init_cond[x][y] = 1

    g = SimpleGrid(width, height, cell=ConwayCell, real_time=False, initial_conditions=init_cond)

    app = QApplication(sys.argv)
    main_window = MainWindow(g)
    sys.exit(app.exec_())

class MainWindow(QWidget):

    def __init__(self, CellGrid, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.CellGrid = CellGrid
        self.threads = []
        self._init_ui()

    def _init_ui(self):

        # Title
        self.setWindowTitle('Test')

        # Size window
        self.resize(300, 300)

        # centre window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Widgets
        self.NTicks = QLineEdit()
        self.NTicks.setText("10")

        self.button = QPushButton("Start")
        self.button.setText("Start")

        self.button.clicked.connect(self.simulate)
        self.LabelGrid = LabelGrid(*(self.CellGrid.dim))

        layout = QVBoxLayout()
        layout.addWidget(self.NTicks)
        layout.addWidget(self.button)
        layout.addWidget(self.LabelGrid)
        self.setLayout(layout)

        self.update_labels()
        self.show()

    def update_labels(self):

        for cell, (r,c) in self.CellGrid.items():
            text = 'X' if cell.val else ''
            self.LabelGrid[r][c].setText(text)

    def simulate(self):

        n_ticks = int(self.NTicks.text())
        s = SimThred(n_ticks, self.CellGrid, self.LabelGrid)
        self.threads.append(s)
        s.start()

class LabelGrid(QWidget):

    def __init__(self, nrow, ncol):

        super().__init__()
        qgid = QGridLayout()
        self._array = list2(nrow, ncol)

        for _, (r,c) in self._array.items():
            label = QLabel('')
            self._array[r][c] = label
            qgid.addWidget(label, *(c,r))

        self.setLayout(qgid)

    def __getitem__(self, key):

        return self._array[key]

class SimThred(QThread):
    def __init__(self, nticks, CellGrid, LabelGrid):

        QThread.__init__(self)
        self.CellGrid = CellGrid
        self.nticks = nticks
        self.LabelGrid = LabelGrid

    def run(self):
        for i in range(self.nticks):
            time.sleep(0.05)
            self.CellGrid.tick()
            self.update_grid()

    def update_grid(self):

        for cell, (r,c) in self.CellGrid.items():
            text = 'X' if cell.val else ''
            self.LabelGrid[r][c].setText(text)

if __name__ == '__main__':

    main()