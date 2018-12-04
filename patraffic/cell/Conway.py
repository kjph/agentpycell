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
        self._state = not(self._state)

    @property
    def val(self):
        return int(bool(self._state))

    def update(self, neighbours):
        """
        Rules:
            - Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
            - Any live cell with two or three live neighbours lives on to the next generation.
            - Any live cell with more than three live neighbours dies, as if by overpopulation.
            - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """

        n_active_neighbours = 0
        for cell in neighbours:
            if cell is not None:
                n_active_neighbours += cell.val

        if self._state and ((n_active_neighbours < 2) or (n_active_neighbours > 3)):
            self.toggle()
        elif not(self._state) and n_active_neighbours == 3:
            self.toggle()