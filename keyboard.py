import urwid


def input_filter(keys, raw):
    raise ValueError(keys, raw)


def show_or_exit(key):
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()
    txt.set_text(repr(key))


txt = urwid.Text(u"Hello World")
fill = urwid.Filler(txt, "top")
loop = urwid.MainLoop(fill, input_filter=input_filter, unhandled_input=show_or_exit)
loop.run()
