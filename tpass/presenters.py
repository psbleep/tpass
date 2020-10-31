import urwid

from tpass.console import NORMAL, PROMPT

from tpass.signals import PROMPT_CALLBACK

from tpass.widgets import ConsolePrompt


def present_store_listing(store_listing, focused=True):
    presented = []
    for idx, password in enumerate(store_listing.data):
        if idx == store_listing.selected and focused:
            style = "selected_password"
        else:
            style = "password"
        styled_password = urwid.AttrMap(urwid.Text(password), style)
        presented.append(styled_password)
    return presented


def present_config(config):
    presented = [urwid.Text("SHORTCUTS")]
    shortcuts = config["shortcuts"]
    for shortcut in sorted(shortcuts.keys()):
        shortcut_text = "{shortcut}: {password}".format(
            shortcut=shortcut, password=shortcuts[shortcut]
        )
        presented.append(urwid.Text(shortcut_text))
    presented.extend([urwid.Text(""), urwid.Text("COMMANDS")])
    commands = config["commands"]
    for command_key in sorted(commands.keys()):
        command_text = "{command_key}: {command_display_name}".format(
            command_key=command_key, command_display_name=commands[command_key][0]
        )
        presented.append(urwid.Text(command_text))
    presented.extend([urwid.Text(""), urwid.Text("SETTINGS")])
    for setting, value in config["settings"].items():
        presented.append(
            urwid.Text(
                "{setting}: {value}".format(setting=setting, value=str(value).lower())
            )
        )
    return presented


def present_console(console, prompt_callback=None):
    presented = [urwid.Text("tpass"), urwid.Text("")]
    if not console.data:
        return presented
    presented.extend(
        [urwid.Text(console.data[i]) for i in range(len(console.data) - 1)]
    )
    if console.mode == NORMAL:
        presented.append(urwid.Text(console.data[-1]))
    elif console.mode == PROMPT:
        prompt = ConsolePrompt(console.data[-1])
        urwid.connect_signal(prompt, PROMPT_CALLBACK, prompt_callback)
        presented.append(prompt)
    return presented
