from collections import UserList


NORMAL = "NORMAL"
PROMPT = "PROMPT"


class Console(UserList):
    def __init__(self, output=None):
        output = output or []
        self.set_output(output)
        self.mode = NORMAL

    def set_output(self, output):
        if isinstance(output, str):
            output = output.splitlines()
        self.data = output
