from pl_extension.utilities import rand
from pl_extension.utilities.config import update_config


def test_time_string():
    rand_str = rand.time_string()
    assert rand_str


def test_update_config():
    config = dict(
        a="python",
        b="FILENAME",
        c=["python", "FILENAME", "python FILENAME"],
    )
    vars_dict = {"FILENAME": "rust"}
    update_config(config, vars_dict)
    assert config["b"] == "rust"
    assert config["c"][1] == "rust"
    assert config["c"][2] == "python rust"
