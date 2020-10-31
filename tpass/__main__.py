#! /usr/bin/env python3
import os

from tpass.app import App
from tpass.config import Config
from tpass.console import Console
from tpass.store_listing import StoreListing
from tpass.widgets import SearchStore


PASSWORD_STORE_DIR = os.environ.get(
    "PASSWORD_STORE_DIR", os.path.expanduser("~/.password-store")
)

CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

TPASS_CONFIG_HOME = os.path.join(CONFIG_HOME, "tpass")
if not os.path.exists(TPASS_CONFIG_HOME):
    os.makedirs(TPASS_CONFIG_HOME)
TPASS_CONFIG_FILE = os.path.join(TPASS_CONFIG_HOME, "tpass.json")
if not os.path.exists(TPASS_CONFIG_FILE):
    raise NotImplementedError("No config file!")


def main():
    search = SearchStore()
    listing = StoreListing(password_store_dir=PASSWORD_STORE_DIR)
    console = Console()
    config = Config(TPASS_CONFIG_FILE)
    app = App(config=config, search=search, listing=listing, console=console)
    app.run()


if __name__ == "__main__":
    main()
