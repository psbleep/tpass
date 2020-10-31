import collections

import pytest
import urwid

from tpass.app import App

from tpass.console import Console, NORMAL, PROMPT
from tpass.widgets import SearchStore
from tpass.store_listing import StoreListing

from tests import TEST_PASSWORD_STORE_DIR


RAW = None


@pytest.fixture
def app():
    return App(
        config={
            "shortcuts": {"1": "hello"},
            "commands": {"2": "world"},
            "settings": {
                "copy password to clipboard": True,
                "quit after opening password": False,
            },
        },
        search=SearchStore(),
        listing=StoreListing(TEST_PASSWORD_STORE_DIR),
        console=Console(),
    )


def test_setup_console_prompt(app):
    app._setup_console_prompt("Prompt: ", prompt_callback=None)
    assert app._body.get_focus_column() == 1
    assert app._console.mode == PROMPT
    assert app._console.data == ["Prompt: "]
    assert app._right_column.focus_position == 2


def test_cleanup_console_prompt(app):
    app._console.mode = PROMPT
    app._cleanup_console_prompt("Console output!")
    assert app._console.mode == NORMAL
    assert app._console.data == ["Console output!"]


def test_setup_keypress_prompt(app):
    app._setup_keypress_prompt(
        "Enter keypress: ", callback_signal="TEST_SIGNAL", hello="world"
    )
    assert app._console.data == ["Enter keypress: "]


def test_clear_search_term(app):
    app._search.edit_text = "hello"
    app._listing.selected = 2
    app._clear_search_term()
    assert app._search.edit_text == ""
    assert app._listing.selected == 0


@pytest.fixture
def mocked_password_store_open_password(mocker):
    return mocker.patch(
        "tpass.app.password_store.open_password", return_value="31337h4x0r5"
    )


def test_call_open_password_not_set_to_quit_after_opening(
    app, mocked_password_store_open_password
):
    app._call_open_password("hello")
    assert app._console.data == ["31337h4x0r5"]
    assert app._last_opened == "hello"


def test_call_open_password_is_set_to_quit_after_opening(
    app, mocked_password_store_open_password
):
    app._config["settings"]["quit after opening password"] = True
    with pytest.raises(urwid.ExitMainLoop):
        app._call_open_password("hello")


def test_add_shortcut_for_password_callback(app):
    app._add_shortcut_for_password_callback("1", {"password": "email"})
    assert app._config["shortcuts"]["1"] == "email"


proc = collections.namedtuple("Proc", ["stdout"])


def test_get_otp(
    app, mocked_password_store_open_password, mocked_pyperclip_copy, mocker
):
    mocked_oathtool_subprocess = mocker.patch(
        "tpass.app.subprocess.run", return_value=proc(b"123456")
    )
    app._last_opened = "hello"
    app._get_otp()
    mocked_password_store_open_password.assert_called_with("2fa/hello", copy=False)
    mocked_oathtool_subprocess.assert_called_with(
        ["oathtool", "--totp", "--base32", "31337h4x0r5"], stdout=-1, stderr=-1
    )
    mocked_pyperclip_copy.assert_called_with("123456")
    assert app._console.data == ["OTP copied for hello"]
