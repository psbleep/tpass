import subprocess

import pyperclip
import urwid

from tpass import password_store
from tpass.body import Body
from tpass.console import NORMAL, PROMPT

from tpass.presenters import present_config, present_console, present_store_listing

from tpass.signals import (
    ADD_SHORTCUT_FOR_SELECTED_PASSWORD,
    ADD_SHORTCUT_FOR_PASSWORD_CALLBACK,
    DELETE_PASSWORD,
    GENERATE_PASSWORD,
    GET_OTP,
    MOVE_DOWN,
    MOVE_UP,
    SEARCH_TERM_UPDATED,
    OPEN_SELECTED_PASSWORD,
    OPEN_SHORTCUT_PASSWORD,
    QUIT,
)

PALETTE = [("selected_password", "black", "white")]


class App:
    def __init__(self, config, search, listing, console):
        self._config = config
        self._search = search
        self._listing = listing
        self._console = console

        self._left_column = urwid.ListBox(
            urwid.SimpleListWalker(
                [search, urwid.Text(""), *present_store_listing(self._listing)]
            )
        )

        self._right_column = urwid.ListBox(
            urwid.SimpleListWalker(
                [
                    *present_console(console),
                    urwid.Text(""),
                    *present_config(self._config),
                ]
            )
        )

        self._body = Body(
            config=self._config,
            widget_list=[self._left_column, self._right_column],
            dividechars=2,
        )

        self._loop = urwid.MainLoop(
            self._body, palette=PALETTE, input_filter=self._body.input_filter,
        )

        self._connect_signals()

    def _connect_signals(self):
        urwid.connect_signal(
            self._search, OPEN_SELECTED_PASSWORD, self._open_selected_password
        )
        urwid.connect_signal(
            self._search, SEARCH_TERM_UPDATED, self._search_term_updated
        )

        urwid.connect_signal(
            self._body,
            ADD_SHORTCUT_FOR_SELECTED_PASSWORD,
            self._add_shortcut_for_selected_password,
        )
        urwid.connect_signal(
            self._body,
            ADD_SHORTCUT_FOR_PASSWORD_CALLBACK,
            self._add_shortcut_for_password_callback,
        )
        urwid.connect_signal(self._body, DELETE_PASSWORD, self._delete_password)
        urwid.connect_signal(self._body, GENERATE_PASSWORD, self._generate_password)
        urwid.connect_signal(self._body, GET_OTP, self._get_otp)
        urwid.connect_signal(self._body, MOVE_DOWN, self._move_down)
        urwid.connect_signal(self._body, MOVE_UP, self._move_up)
        urwid.connect_signal(
            self._body, OPEN_SELECTED_PASSWORD, self._open_selected_password
        )
        urwid.connect_signal(
            self._body, OPEN_SHORTCUT_PASSWORD, self._open_shortcut_password
        )
        urwid.connect_signal(self._body, QUIT, self._quit)

    def _refresh_left_column(self):
        self._left_column.body = [
            self._search,
            urwid.Text(""),
            *present_store_listing(self._listing, focused=self._left_column_focused),
        ]

    @property
    def _left_column_focused(self):
        return self._body.focus_position == 0

    def _refresh_right_column(self, prompt_callback=None):
        self._right_column.body = [
            *present_console(self._console, prompt_callback=prompt_callback),
            urwid.Text(""),
            *present_config(self._config),
        ]

    def _setup_console_prompt(self, prompt_caption, prompt_callback):
        self._body.set_focus_column(1)
        self._console.mode = PROMPT
        self._console.set_output(prompt_caption)
        self._refresh_right_column(prompt_callback=prompt_callback)
        self._right_column.set_focus(2)

    def _cleanup_console_prompt(self, console_output):
        self._console.mode = NORMAL
        self._console.set_output(console_output)
        self._refresh_right_column()
        self._body.set_focus_column(0)
        self._listing.refresh_file_listing()
        self._refresh_left_column()

    def _setup_keypress_prompt(
        self, console_output, callback_signal, **callback_kwargs
    ):
        self._console.set_output(console_output)
        self._refresh_right_column()
        self._body.get_keypress_and_return_through_signal(
            signal=ADD_SHORTCUT_FOR_PASSWORD_CALLBACK, **callback_kwargs
        )

    def _clear_search_term(self):
        self._search.edit_text = ""
        self._listing.set_search_term("")
        self._listing.refresh_file_listing()
        self._listing.selected = 0

    def _call_open_password(self, password_name):
        console_output = password_store.open_password(
            password_name, copy=self._config["settings"]["copy password to clipboard"]
        )
        if self._config["settings"]["quit after opening password"]:
            self._quit()
        else:
            self._search.edit_text = password_name
            self._search.edit_pos = len(password_name)
            self._console.set_output(console_output)
            self._refresh_right_column()

    def _search_term_updated(self, search_term):
        self._listing.set_search_term(search_term)
        self._refresh_left_column()

    def _add_shortcut_for_selected_password(self):
        console_output = "Enter shortcut for {password}: ".format(
            password=self._listing.selected_password
        )
        self._setup_keypress_prompt(
            console_output,
            callback_signal=ADD_SHORTCUT_FOR_PASSWORD_CALLBACK,
            password=self._listing.selected_password,
        )

    def _add_shortcut_for_password_callback(self, shortcut, kwargs):
        password = kwargs["password"]
        shortcuts = self._config["shortcuts"]
        shortcuts.update({shortcut: password})
        self._config["shortcuts"] = shortcuts
        self._console.set_output(
            "Set shortcut for {password!r}.".format(password=password)
        )
        self._refresh_right_column()

    def _delete_password(self):
        self._setup_console_prompt(
            "Delete {password}? [y/N]: ".format(
                password=self._listing.selected_password
            ),
            prompt_callback=self._delete_password_callback,
        )

    def _delete_password_callback(self, response):
        if response.lower()[0] == "y":
            console_output = password_store.delete_password(
                self._listing.selected_password
            )
            self._clear_search_term()
        else:
            console_output = "Canceled deleting {password}.".format(
                password=self._listing.selected_password
            )
        self._cleanup_console_prompt(console_output)

    def _generate_password(self):
        self._setup_console_prompt(
            "Password name: ", prompt_callback=self._generate_password_callback
        )

    def _generate_password_callback(self, password_name):
        console_output = password_store.generate_password(
            password_name, copy=self._config["settings"]["copy password to clipboard"]
        )
        self._cleanup_console_prompt(console_output)

    def _get_otp(self):
        key_name = "2fa/" + self._search.edit_text
        secret = password_store.open_password(key_name, copy=False)
        oathtool_cmd = "oathtool --totp --base32 " + secret
        proc = subprocess.run(
            oathtool_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        otp = proc.stdout.decode().splitlines()[0]
        pyperclip.copy(otp)
        self._console.set_output("OTP copied for " + self._search.edit_text)
        self._refresh_right_column()

    def _move_down(self):
        self._listing.selected += 1
        self._refresh_left_column()

    def _move_up(self):
        self._listing.selected -= 1
        self._refresh_left_column()

    def _open_selected_password(self):
        if not self._listing:
            return
        self._call_open_password(self._listing.selected_password)

    def _open_shortcut_password(self, password_name):
        self._listing.set_search_term(password_name)
        self._listing.selected_password = password_name
        self._refresh_left_column()
        self._call_open_password(password_name)

    def _quit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        self._loop.run()
