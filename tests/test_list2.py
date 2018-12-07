import pytest

from patraffic.utils import list2

def test_indexing():

    l = list2(3, 4)

    assert l.dim == (3,4)
    assert len(l) == 12

    l[2][3] = 9912
    assert l[2][3] == 9912

def test_linearIterator():

    l2 = list2(3, 4)
    l2[0][0] = 0
    l2[1][0] = 1
    l2[2][0] = 2
    l2[0][1] = 3
    l2[1][1] = 4
    l2[2][1] = 5
    l2[0][2] = 6
    l2[1][2] = 7
    l2[2][2] = 8
    l2[0][3] = 9
    l2[1][3] = 10
    l2[2][3] = 11

    start = 0
    for e in l2:
        assert e == start
        start += 1

def test_items():

    l2 = list2(3, 4)
    l2[0][0] = 0
    l2[1][0] = 1
    l2[2][0] = 2
    l2[0][1] = 3
    l2[1][1] = 4
    l2[2][1] = 5
    l2[0][2] = 6
    l2[1][2] = 7
    l2[2][2] = 8
    l2[0][3] = 9
    l2[1][3] = 10
    l2[2][3] = 11

    start = 0
    expected_ps = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2), (0,3), (1,3), (2,3)]
    for e, p in l2.items():
        assert e == start
        assert p == expected_ps[start]
        start += 1

    start = 0
    expected_ps = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2), (0,3), (1,3), (2,3)]
    for e, (x,y) in l2.items():
        assert e == start
        assert (x, y) == expected_ps[start]
        assert x == expected_ps[start][0]
        assert y == expected_ps[start][1]
        start += 1