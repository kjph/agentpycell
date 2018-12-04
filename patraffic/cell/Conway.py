""" Based on John Conway's Game of Life
"""

import random

from .. import SimpleCell

class ConwayCell(SimpleCell):

    def __init__(self, initial_conditions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if initial_conditions is None:
            self._state = random.getrandbits(1)
        else:
            self._state = initial_conditions

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