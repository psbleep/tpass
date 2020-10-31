from collections import namedtuple

from tpass import presenters
from tpass.console import NORMAL, PROMPT


def test_config_presenter():
    config = {
        "shortcuts": {"b": "foo bar", "a": "hello world"},
        "commands": {
            "1": ["set greeting", "SET_GREETING"],
            "2": ["set foo", "SET_FOO"],
        },
        "settings": {"quit after opening": True},
    }
    presented = presenters.present_config(config)
    assert presented[0].text == "SHORTCUTS"
    assert presented[1].text == "a: hello world"
    assert presented[2].text == "b: foo bar"
    assert presented[4].text == "COMMANDS"
    assert presented[5].text == "1: set greeting"
    assert presented[6].text == "2: set foo"
    assert presented[8].text == "SETTINGS"
    assert presented[9].text == "quit after opening: true"


MockStoreListing = namedtuple("StoreListing", ["data", "selected"])


def test_present_store_listing_when_column_is_focused():
    store_listing = MockStoreListing(data=["1", "2"], selected=1)
    presented = presenters.present_store_listing(store_listing, focused=True)
    assert presented[0].attr_map == {None: "password"}
    assert presented[0].original_widget.text == "1"
    assert presented[1].attr_map == {None: "selected_password"}
    assert presented[1].original_widget.text == "2"


def test_present_store_listing_when_column_is_not_focused():
    store_listing = MockStoreListing(data=["1", "2"], selected=1)
    presented = presenters.present_store_listing(store_listing, focused=False)
    assert presented[0].attr_map == {None: "password"}
    assert presented[0].original_widget.text == "1"
    assert presented[1].attr_map == {None: "password"}
    assert presented[1].original_widget.text == "2"


MockConsole = namedtuple("Console", ["data", "mode"])


def test_present_console_display_mode():
    console = MockConsole(data=["hello world"], mode=NORMAL)
    presented = presenters.present_console(console)
    assert presented[0].text == "tpass"
    assert presented[2].text == "hello world"


def test_present_console_empty_console():
    console = MockConsole(data=[], mode=NORMAL)
    presented = presenters.present_console(console)
    assert len(presented) == 2
    assert presented[0].text == "tpass"


def test_present_console_prompt_mode():
    console = MockConsole(data=["hello? "], mode=PROMPT)
    presented = presenters.present_console(console)
    assert presented[0].text == "tpass"
    assert presented[2].caption == "hello? "
