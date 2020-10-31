import re
import subprocess

import pyperclip


def open_password(password_name, copy=False):
    proc = subprocess.run(
        ["pass", password_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output = proc.stdout.decode()
    if copy:
        output = output.splitlines()[0]
        pyperclip.copy(output)
        return "{password_name!r} copied to clipboard.".format(
            password_name=password_name
        )
    return output.strip("\n")


def generate_password(password_name, copy=False):
    proc = subprocess.run(
        ["pass", "generate", password_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    output = ansi_escape.sub("", proc.stdout.decode("utf-8")).splitlines()
    if copy:
        pyperclip.copy(output[-1])
    return output


def delete_password(password_name):
    proc = subprocess.run(
        ["pass", "rm", "-f", password_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.decode().splitlines()
