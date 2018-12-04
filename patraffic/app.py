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

    init_cond = list2(width, height)
    toggle = [(6,6), (6,7), (6,8), (6,9), (6,10), (10,6), (10,7), (10,8), (10,9), (10,10), (8,6), (8,10)]
    #toggle = [(1,1)]
    for x,y in toggle:
        init_cond[x][y] = 1

    g = SimpleGrid(width, height, cell=ConwayCell, real_time=False, initial_conditions=init_cond)

    app = QApplication(sys.argv)
    main_window = MainWindow(g)
    sys.exit(app.exec_())

class SimThred(QThread):
    def __init__(self, abm, ticks, ui_grid):
        QThread.__init__(self)
        self._abm = abm
        self._ticks = ticks
        self._ui = ui_grid

    def run(self):

        #self._abm.reset_grid()
        width, height = self._abm.dim
        y_sweep = [y for y in range(height)]
        x_sweep = [x for x in range(width)]

        for i in range(self._ticks):
            time.sleep(0.05)
            self._abm.tick()

            for y in y_sweep:
                for x in x_sweep:
                    cell = self._abm[x][y]
                    if cell.val:
                        self._ui[x][y].setText('X')
                    else:
                        self._ui[x][y].setText('')

class MainWindow(QWidget):

    def __init__(self, ABMGrid, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._abm = ABMGrid
        self._init_ui()
        #self._init_menu()

        self.NTicks = QLineEdit()
        self.NTicks.setObjectName("#Ticks")
        self.NTicks.setText("100")

        self.button = QPushButton("Start")
        self.button.setObjectName("Start")
        self.button.setText("Start") 

        self.button.clicked.connect(self.simulate)
        self.CellGrid = CellGrid(self._abm)

        layout = QVBoxLayout()
        layout.addWidget(self.NTicks)
        layout.addWidget(self.button)
        layout.addWidget(self.CellGrid)
        self.setLayout(layout)

        self.threads = []
        self.update_grid()

        self.show()

    def update_grid(self):

        width, height = self._abm.dim
        y_sweep = [y for y in range(height)]
        x_sweep = [x for x in range(width)]

        for y in y_sweep:
            for x in x_sweep:
                cell = self._abm[x][y]
                if cell.val:
                    self.CellGrid._grid[x][y].setText('X')
                else:
                    self.CellGrid._grid[x][y].setText('')

    def simulate(self):

        n_ticks = int(self.NTicks.text())
        s = SimThred(self._abm, n_ticks, self.CellGrid._grid)
        self.threads.append(s)
        s.start()

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

class CellGrid(QWidget):

    def __init__(self, abm):
        super(QWidget, self).__init__()
        self._abm = abm
        _grid = QGridLayout()

        width, height = self._abm.dim

        positions = [(i,j) for i in range(width) for j in range(height)]
        self._grid = [[None for y in range(height)] for x in range(width)]

        for x,y in positions:

            label = QLabel('')
            self._grid[x][y] = label

            _grid.addWidget(label, *(y,x))

        #self.move(300, 150)
        self.setLayout(_grid)


if __name__ == '__main__':

    main()