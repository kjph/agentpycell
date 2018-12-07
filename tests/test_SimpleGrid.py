import pytest

from patraffic import SimpleGrid
from patraffic.cell import ConwayCell

def test_size():

    g = SimpleGrid(15, 20, cell=ConwayCell)
    assert g.dim == (15, 20)

    width = 17
    height = 13

    init_cond = [[0 for y in range(height)] for x in range(width)]
    g2 = SimpleGrid(17, 13, cell=ConwayCell, initial_conditions=init_cond)
    assert g2.dim == (17, 13)

def test_subset():

    init_cond = [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        [0, 0, 1, 1]
    ]

    g = SimpleGrid(4, 4, cell=ConwayCell, initial_conditions=init_cond)
    assert g.dim == (4, 4)

    test_cases = [
        #r, c, n_active
        (0, 0, 0)
        ,(0, 1, 1)
        ,(0, 2, 2)
        ,(0, 3, 2)
        ,(1, 0, 1)
        ,(1, 1, 3)
        ,(1, 2, 4)
        ,(1, 3, 3)
        ,(2, 0, 1)
        ,(2, 1, 3)
        ,(2, 2, 6)
        ,(2, 3, 5)
        ,(3, 0, 1)
        ,(3, 1, 3)
        ,(3, 2, 4)
        ,(3, 3, 3)
    ]

    for r, c, expected in test_cases:

        target = g.get_neighbours(r, c)
        n_active = 0
        for cell in target:
            if cell is not None:
                n_active += cell.val
        assert n_active == expected
   