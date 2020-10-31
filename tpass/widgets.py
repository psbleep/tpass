import urwid

from tpass.signals import PROMPT_CALLBACK, OPEN_SELECTED_PASSWORD, SEARCH_TERM_UPDATED


class SearchStore(urwid.Edit):
    __metaclass__ = urwid.MetaSignals
    signals = [OPEN_SELECTED_PASSWORD, SEARCH_TERM_UPDATED]

    def __init__(self, prompt="Password: ", search_term=""):
        super().__init__(caption=prompt, edit_text=search_term)

    @property
    def search_term(self):
        return self.edit_text

    @search_term.setter
    def search_term(self, val):
        self.edit_text = val

    def keypress(self, size, key):
        old_search_term = self.search_term
        resp = None
        if key == "enter":
            urwid.emit_signal(self, OPEN_SELECTED_PASSWORD)
        elif key == "ctrl a":
            self.edit_pos = 0
        elif key == "ctrl e":
            self.edit_pos = len(self.edit_text)
        elif key == "ctrl k":
            self.search_term = self.search_term[0 : self.edit_pos]
        else:
            resp = super().keypress(size, key)
        if old_search_term != self.search_term:
            urwid.emit_signal(self, SEARCH_TERM_UPDATED, self.edit_text)
        return resp


class ConsolePrompt(urwid.Edit):
    __metaclass__ = urwid.MetaSignals
    signals = [PROMPT_CALLBACK]

    def keypress(self, size, key):
        if key == "enter":
            urwid.emit_signal(self, PROMPT_CALLBACK, self.edit_text)
        else:
            return super().keypress(size, key)
