import pytest

from tpass.console import Console


@pytest.fixture
def console():
    return Console()


def test_set_output_string(console):
    console.set_output("hello world")
    assert console == ["hello world"]


def test_set_output_string_with_line_breaks(console):
    console.set_output("hello world\ngoodbye void")
    assert console == ["hello world", "goodbye void"]


def test_set_output_list(console):
    console.set_output(["hello world", "goodbye void"])
    assert console == ["hello world", "goodbye void"]
