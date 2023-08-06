import argparse
import logging
from typing import Any, Dict

__all__ = ["add_options", "apply_options", "update_config"]

logger = logging.getLogger(__name__)


def add_options(parser: argparse.ArgumentParser) -> None:
    """
    Add options to parser.
    """
    parser.add_argument(
        "opts",
        help="modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )


def apply_options(config: Dict[str, Any], args: argparse.Namespace) -> None:
    """
    Update config using opts.
    """
    try:
        from yacs.config import CfgNode as CN
    except ImportError as e:
        logger.error(
            "`apply_options` requiring yacs(version==0.1.8), "
            "but not installed."
        )
        raise e
    opts = args.opts
    config_CN = CN(config)
    if opts is not None and len(opts) > 0:
        config_CN.merge_from_list(opts)
    config.update(config_CN)


def update_config(config: Dict[str, Any], vars_dict: Dict[str, Any]) -> None:
    """Update str in config, with vars_dict.

    When you want to set some lazy-compute value in config, `update_config` is
    very useful.

    Args:
        config: input config dict.
        vars_dict: key-value pair.

    Examples:

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

    """

    def _find_and_replace(_str):
        for _k, _v in vars_dict.items():
            _str = _str.replace(_k, _v)
        return _str

    if isinstance(config, dict):
        for k in config:
            if isinstance(config[k], str):
                config[k] = _find_and_replace(config[k])
            elif isinstance(config[k], dict):
                update_config(config[k], vars_dict)
            elif isinstance(config[k], list):
                update_config(config[k], vars_dict)
    elif isinstance(config, list):
        for i, _ in enumerate(config):
            if isinstance(config[i], str):
                config[i] = _find_and_replace(config[i])
            elif isinstance(config[i], dict):
                update_config(config[i], vars_dict)
            elif isinstance(config[i], list):
                update_config(config[i], vars_dict)
    elif isinstance(config, (int, float, bool)):
        pass
    else:
        raise ValueError(f"Unknown type: {type(config)}")
