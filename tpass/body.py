import urwid

from tpass.signals import (
    ADD_SHORTCUT_FOR_SELECTED_PASSWORD,
    ADD_SHORTCUT_FOR_PASSWORD_CALLBACK,
    DELETE_PASSWORD,
    GENERATE_PASSWORD,
    GET_OTP,
    MOVE_DOWN,
    MOVE_UP,
    OPEN_SELECTED_PASSWORD,
    OPEN_SHORTCUT_PASSWORD,
    RETURN_KEYPRESS,
    QUIT,
)


NORMAL = "NORMAL"
KEYPRESS = "KEYPRESS"


class Body(urwid.Columns):
    __metaclass__ = urwid.MetaSignals
    signals = [
        ADD_SHORTCUT_FOR_SELECTED_PASSWORD,
        ADD_SHORTCUT_FOR_PASSWORD_CALLBACK,
        DELETE_PASSWORD,
        GENERATE_PASSWORD,
        GET_OTP,
        MOVE_DOWN,
        MOVE_UP,
        OPEN_SELECTED_PASSWORD,
        OPEN_SHORTCUT_PASSWORD,
        RETURN_KEYPRESS,
        QUIT,
    ]

    def __init__(self, config, *args, **kwargs):
        self._config = config
        self._mode = NORMAL
        self._keypress_prompt_callback_signal = ""
        self._keypress_prompt_callback_kwargs = {}
        super().__init__(*args, **kwargs)

    def input_filter(self, keys, raw):
        if self._mode == NORMAL:
            return self._regular_mode_input_filter(keys, raw)
        elif self._mode == KEYPRESS:
            return self._keypress_mode_input_filter(keys, raw)

    def _regular_mode_input_filter(self, keys, raw):
        resp = []
        for key in keys:
            shortcut_password = self._config["shortcuts"].get(key)
            if shortcut_password:
                urwid.emit_signal(self, OPEN_SHORTCUT_PASSWORD, shortcut_password)
                continue
            command_data = self._config["commands"].get(key)
            if command_data:
                urwid.emit_signal(self, command_data[1])
                continue
            resp.append(key)
        return resp

    def _keypress_mode_input_filter(self, keys, raw):
        urwid.emit_signal(
            self,
            self._keypress_prompt_callback_signal,
            keys[0],
            self._keypress_prompt_callback_kwargs,
        )
        self._mode = NORMAL
        self._keypress_prompt_callback_signal = None
        self._keypress_prompt_callback_kwargs = {}
        return []

    def get_keypress_and_return_through_signal(self, signal, **kwargs):
        self._mode = KEYPRESS
        self._keypress_prompt_callback_signal = signal
        self._keypress_prompt_callback_kwargs = kwargs
