import pytest

from tpass.body import Body, NORMAL, KEYPRESS
from tpass.signals import OPEN_SHORTCUT_PASSWORD


RAW = None


config = {"shortcuts": {"1": "hello"}, "commands": {"2": ["world", "WORLD"]}}


@pytest.fixture
def body():
    return Body(config, [])


def test_regular_mode_input_filter_key_is_shortcut(body, mocked_emit_signal):
    assert body.input_filter(["1"], RAW) == []
    mocked_emit_signal.assert_called_with(body, OPEN_SHORTCUT_PASSWORD, "hello")


def test_regular_mode_input_filter_key_is_command(body, mocked_emit_signal):
    assert body.input_filter(["2"], RAW) == []
    mocked_emit_signal.assert_called_with(body, "WORLD")


def test_regular_mode_input_filter_key_is_not_shortcut_or_command(
    body, mocked_emit_signal
):
    assert body.input_filter(["a"], RAW) == ["a"]
    assert not mocked_emit_signal.called


def test_get_keypress_mode_input_filter(body, mocked_emit_signal):
    body._mode = KEYPRESS
    body._keypress_prompt_callback_signal = "CALLBACK_SIGNAL"
    body._keypress_prompt_callback_kwargs = {"hello": "world"}
    assert body.input_filter(["a"], RAW) == []
    assert body._mode == NORMAL
    assert body._keypress_prompt_callback_signal is None
    assert body._keypress_prompt_callback_kwargs == {}
    mocked_emit_signal.assert_called_with(
        body, "CALLBACK_SIGNAL", "a", {"hello": "world"}
    )


def test_get_keypress_and_callback(body):
    body.get_keypress_and_return_through_signal(signal="CALLBACK_SIGNAL", hello="world")
    assert body._mode == KEYPRESS
    assert body._keypress_prompt_callback_signal == "CALLBACK_SIGNAL"
    assert body._keypress_prompt_callback_kwargs == {"hello": "world"}
