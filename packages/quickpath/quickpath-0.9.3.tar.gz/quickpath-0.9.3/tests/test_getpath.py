from collections import namedtuple
from quickpath import getpath, getpaths, getlistpath, getlistpaths, All


Node = namedtuple("Node", "id name data")

test_a = [
    {"id": 1, "values": [4, 5]},
    {"id": 2, "values": [4, 7]},
    {"id": 3, "values": [6, 9]},
]

test_b = [
    [
        Node(id=1, name="hmmm", data="something"),
        Node(id=2, name="hmmmmm", data="something else"),
    ],
    [Node(id=3, name="hh", data="something again")],
]


def test_getpath_a():
    assert getpath(test_a, (0, "id")) == 1


def test_getpath_a_missing():
    assert getpath(test_a, (0, "x")) == None
    assert getpath(test_a, (0, "x"), default="-") == "-"


def test_getpaths_a():
    assert getpaths(test_a, "0.id") == 1
    assert getpaths(test_a, "5.id") == None
    assert getpaths(test_a, "0.values.1") == 5
    assert getpaths(test_a, "0/values/1", sep="/") == 5


def test_getlistpath_a():
    assert getlistpath(test_a, (All, "values", All)) == [4, 5, 4, 7, 6, 9]


def test_getlistpaths_a():
    assert getlistpaths(test_a, "*.id") == [1, 2, 3]
    assert getlistpaths(test_a, "*.values.*") == [4, 5, 4, 7, 6, 9]


def test_getlistpaths_b():
    assert getlistpaths(test_b, "*.*.id") == [1, 2, 3]
    assert getlistpath(test_b, (All, 0, "id")) == [1, 3]


def test_getlistpaths_emptystr():
    empty_str_dict = {"": {"": 1}}
    assert getlistpaths(empty_str_dict, ".") == [1]
    assert getlistpath(empty_str_dict, ("", "")) == [1]


def test_doc():
    item = [{"id": 1}, {"id": 2}]
    value = getpath(item, (0, "id"))
    assert value == 1
    value = getpaths(item, "0.id")
    assert value == 1
    all_ids = getlistpath(item, (All, "id"))
    assert all_ids == [1, 2]
    all_ids = getlistpaths(item, "*.id")
    assert all_ids == [1, 2]
