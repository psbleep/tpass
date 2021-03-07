import collections

import pytest

from tpass import password_store


proc = collections.namedtuple("Proc", ["stdout"])


@pytest.fixture
def mocked_open_password_subprocess(mocker):
    mocker.patch(
        "tpass.password_store.subprocess.run", return_value=proc(b"h3ll0 w0rld")
    )


def test_open_password_not_copied_to_clipboard_returns_password(
    mocked_open_password_subprocess,
):
    assert password_store.open_password("greeting", copy=False) == "h3ll0 w0rld"


def test_open_password_copied_to_clipboard_calls_pyperclip(
    mocked_open_password_subprocess, mocked_pyperclip_copy
):
    password_store.open_password("greeting", copy=True)
    mocked_pyperclip_copy.assert_called_with("h3ll0 w0rld")


def test_open_password_copied_to_clipboard_returns_console_output(
    mocked_open_password_subprocess, mocked_pyperclip_copy
):
    assert (
        password_store.open_password("greeting", copy=True)
        == "'greeting' copied to clipboard."
    )


def test_open_multiline_password_copies_first_line_to_clipboard_displays_rest(
    mocker, mocked_pyperclip_copy,
):
    mocker.patch(
        "tpass.password_store.subprocess.run",
        return_value=proc(b"h3ll0 w0rld\nusername: foo\nurl: bar.org"),
    )
    assert (
        password_store.open_password("greeting", copy=True)
        == "'greeting' copied to clipboard.\n\nusername: foo\nurl: bar.org"
    )
    mocked_pyperclip_copy.assert_called()


@pytest.fixture
def mocked_generate_password_subprocess(mocker):
    mocker.patch(
        "tpass.password_store.subprocess.run",
        return_value=proc(b"The generated password for hello is:\nh3ll0 w0rld"),
    )


def test_generate_password_returns_console_output(mocked_generate_password_subprocess):
    assert password_store.generate_password(password_name="hello") == [
        "The generated password for hello is:",
        "h3ll0 w0rld",
    ]


def test_generate_password_copied_to_clipboard_calls_pyperclip(
    mocked_generate_password_subprocess, mocked_pyperclip_copy
):
    password_store.generate_password("hello", copy=True)
    mocked_pyperclip_copy.assert_called_with("h3ll0 w0rld")


@pytest.fixture
def mocked_delete_password_subprocess(mocker):
    mocker.patch(
        "tpass.password_store.subprocess.run", return_value=proc(b"Removed hello")
    )


def test_delete_password_returns_console_output(mocked_delete_password_subprocess):
    assert password_store.delete_password(password_name="hello") == ["Removed hello"]
