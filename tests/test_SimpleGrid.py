import pytest

from patraffic import SimpleGrid
from patraffic.cell import ConwayCell

def test_size():

    g = SimpleGrid(15, 20, cell=ConwayCell)
    assert g.size == (15, 20)

    width = 17
    height = 13

    init_cond = [[0 for y in range(height)] for x in range(width)]
    g2 = SimpleGrid(17, 13, cell=ConwayCell, initial_conditions=init_cond)
    assert g2.size == (17, 13)

