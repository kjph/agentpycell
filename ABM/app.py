import sys
import time

import random
import ABM

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def main():
    """ Application entry point
    """

    g = ABM.Grid(15, 15, cell=SimpleCell, real_time=False)

    app = QApplication(sys.argv)
    main_window = MainWindow(g)
    sys.exit(app.exec_())

    for i in range(50):
        print('\niter={}'.format(i))
        g.tick()
        g.print_grid()  

class SimpleCell(ABM.Cell):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = random.getrandbits(1)
        self._new = None

    def toggle(self):
        self._state = int(not(self._state))

    @property
    def val(self):
        return self._state

    def update(self, neighbours):
        """
        Rules:
            - Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
            - Any live cell with two or three live neighbours lives on to the next generation.
            - Any live cell with more than three live neighbours dies, as if by overpopulation.
            - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        
        n_active_neighbours = -self._state
        for row in neighbours:
            for cell in row:
                n_active_neighbours += cell.val

        # TODO: need to keep original state same within one tick
        if self._state:
            if n_active_neighbours < 2:
                self._state = 0
            elif n_active_neighbours in (2,3):
                self._state = 1
            elif n_active_neighbours > 3:
                self._state = 0
        else:
            if n_active_neighbours == 3:
                self._state = 1
            else:
                self._state = 0

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
                        self._ui[x][y].setText('x')
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
        self.setWindowTitle('Calculator')
        self.setLayout(_grid)
        #self.show()

if __name__ == '__main__':

    main()