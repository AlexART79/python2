import pytest
from ..modules import fibonacci


def test_fib1():
    assert fibonacci.fib(1) == 0


def test_fib2():
    assert fibonacci.fib(2) == 1


def test_fib2():
    assert fibonacci.fib(10) == 34


def test_fibon1():
    assert fibonacci.fibon(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fibon2():
    assert fibonacci.fibon(9) == [0, 1, 1, 2, 3, 5, 8, 13, 21]


@pytest.mark.xfail
def test_fibon3():
    assert fibonacci.fibon(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21]


def test_fibon4():
    assert fibonacci.fibon(0) == []


def test_fibon5():
    assert fibonacci.fibon(1) == [0]


def test_fibon6():
    assert fibonacci.fibon(2) == [0, 1]
