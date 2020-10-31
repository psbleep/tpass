import json
import os

from tpass.config import Config


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG_FILE = os.path.join(TESTS_DIR, ".test_config.json")
OTHER_TEST_CONFIG_FILE = os.path.join(TESTS_DIR, ".other_test_config.json")


def test_config_reads_from_config_file():
    config = Config(TEST_CONFIG_FILE)
    assert config == {
        "shortcuts": {"ctrl a": "greeting/hello", "ctrl b": "greeting/world"},
        "commands": {
            "ctrl y": ["go", "GO_COMMAND"],
            "ctrl z": ["stop", "STOP_COMMAND"],
        },
        "foo": "bar",
    }


def test_config_file_setitem_writes_to_file():
    with open(OTHER_TEST_CONFIG_FILE, "w") as f:
        json.dump({}, f)
    config = Config(OTHER_TEST_CONFIG_FILE)
    config["hello"] = "world"
    with open(OTHER_TEST_CONFIG_FILE) as f:
        assert json.load(f) == {"hello": "world"}
    os.remove(OTHER_TEST_CONFIG_FILE)
