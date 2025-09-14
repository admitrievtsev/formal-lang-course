import pytest  # noqa: F401
from filecmp import cmp
from os import remove


from project.graph_processor import generate_graph_report, generate_and_save_graph_with_two_cycles


def test_graph_reporting():
    report = generate_graph_report("generations")
    assert report.nodes_num == 273
    assert report.edges_num == 129
    assert report.labels == [
        "type",
        "first",
        "rest",
        "onProperty",
        "intersectionOf",
        "equivalentClass",
        "someValuesFrom",
        "hasValue",
        "hasSex",
        "hasChild",
        "hasParent",
        "inverseOf",
        "sameAs",
        "hasSibling",
        "oneOf",
        "range",
        "versionInfo",
    ]


def test_two_cycles_graph_saving_simple():
    generate_and_save_graph_with_two_cycles([1, 2], ["label1", "label2"], "temp1.dot")
    cmp("temp1.dot", "tests/resources/task1_cyclecheck1.dot")
    remove("temp1.dot")


def test_two_cycles_graph_saving_multiple():
    generate_and_save_graph_with_two_cycles([10, 20], ["label1", "label2"], "temp2.dot")
    cmp("temp2.dot", "tests/resources/task1_cyclecheck2.dot")
    remove("temp2.dot")
