import pytest

from tpass.widgets import ConsolePrompt, SearchStore
from tpass.signals import PROMPT_CALLBACK, SEARCH_TERM_UPDATED


SIZE = (1,)

TEST_SIGNAL = "TEST_SIGNAL"


@pytest.fixture
def search():
    return SearchStore()


def test_search_keypress_changes_search_term_triggers_listing_update(
    mocked_emit_signal, search
):
    search.keypress(SIZE, "a")
    mocked_emit_signal.assert_called_with(search, SEARCH_TERM_UPDATED, "a")


def test_search_keypress_beginning_of_line_updates_cursor_position(search):
    search.edit_text = "hello world"
    search.edit_pos = len(search.edit_text) - 1
    search.keypress(SIZE, "ctrl a")
    assert search.edit_pos == 0


def test_search_keypress_end_of_line_updates_cursor_position(search):
    search.edit_text = "hello world"
    search.edit_pos = 0
    search.keypress(SIZE, "ctrl e")
    assert search.edit_pos == 11


def test_search_keypress_clear_line(search):
    search.edit_text = "hello world"
    search.edit_pos = 5
    search.keypress(SIZE, "ctrl k")
    assert search.edit_text == "hello"


def test_search_regular_keypress_updates_edit_text(search):
    search.keypress(SIZE, "a")
    assert search.search_term == "a"


def test_search_keypress_other_does_not_trigger_signal(mocked_emit_signal, search):
    search.keypress(SIZE, "ctrl-w")
    assert not mocked_emit_signal.called


def test_console_prompt_enter_keypress_triggers_handler_signal(mocked_emit_signal):
    prompt = ConsolePrompt("hello? ")
    prompt.edit_text = "world"
    prompt.keypress(SIZE, "enter")
    mocked_emit_signal.assert_called_with(prompt, PROMPT_CALLBACK, "world")


def test_console_prompt_regular_keypress_updated_edit_text():
    prompt = ConsolePrompt("hello? ")
    prompt.keypress(SIZE, "w")
    assert prompt.edit_text == "w"
