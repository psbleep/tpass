import pytest


@pytest.fixture
def mocked_emit_signal(mocker):
    return mocker.patch("tpass.widgets.urwid.emit_signal")


@pytest.fixture
def mocked_pyperclip_copy(mocker):
    return mocker.patch("tpass.password_store.pyperclip.copy")
