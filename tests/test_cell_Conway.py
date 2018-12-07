import pytest

from patraffic.cell import ConwayCell

def test_Conway():
    """ Basic tests"""

    cell = ConwayCell(initial_conditions=1)
    assert cell.val == 1
    cell.toggle()
    assert cell.val == 0
    cell.toggle()
    assert cell.val == 1

    cell2 = ConwayCell()
    start_val = cell2.val
    cell2.toggle()
    assert start_val != cell2.val

    