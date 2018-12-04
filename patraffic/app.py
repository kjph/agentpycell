import sys
import time

import random
from patraffic import SimpleGrid
from patraffic.cell import ConwayCell

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def main():
    """ Application entry point
    """

    g = SimpleGrid(15, 15, cell=ConwayCell, real_time=False)

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

        self._abm.reset_grid()
        width, height = self._abm.size
        y_sweep = [y for y in range(height)]
        x_sweep = [x for x in range(width)]

        for i in range(self._ticks):
            time.sleep(0.05)
            self._abm.tick()

            for y in y_sweep:
                for x in x_sweep:
                    cell = self._abm.get_cell(x,y)
                    if cell.val:
                        self._ui[x][y].setText('O')
                    else:
                        self._ui[x][y].setText('')

class MainWindow(QWidget):

    def __init__(self, ABMGrid, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._abm = ABMGrid
        self._init_ui()
        #self._init_menu()

        self.button = QPushButton("Start")
        self.button.clicked.connect(self.simulate)
        self.CellGrid = CellGrid(self._abm)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.CellGrid)
        self.setLayout(layout)

        self.threads = []

        self.show()

    def simulate(self):
        s = SimThred(self._abm, 100, self.CellGrid._grid)
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

        height, width = self._abm.size

        positions = [(i,j) for i in range(width) for j in range(height)]
        self._grid = [[None for y in range(height)] for x in range(width)]

        for position in positions:

            x,y = position
            label = QLabel('')
            self._grid[x][y] = label

            _grid.addWidget(label, *position)

        self.move(300, 150)
        self.setLayout(_grid)


if __name__ == '__main__':

    main()