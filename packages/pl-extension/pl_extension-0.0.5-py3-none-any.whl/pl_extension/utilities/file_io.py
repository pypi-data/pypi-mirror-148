import logging
import os
from contextlib import contextmanager
from typing import Dict

from pl_extension.utilities.env import HDFS_CACHE

import mmcv
from iopath.common.file_io import HTTPURLHandler, PathManagerFactory

__all__ = ["load_file", "open_file", "path_manager"]


logger = logging.getLogger(__name__)


def load_file(file_path: str) -> Dict:
    """
    load file from .py/.yaml/.json/.yml/.pkl
    """
    file_ext = os.path.splitext(file_path)[1]
    assert file_ext in [
        ".py",
        ".yaml",
        "yml",
        "json",
        "pkl",
    ], f" Bad file ext: {file_path}"

    if file_ext == ".py":
        content = mmcv.Config.fromfile(file_path)
        content = dict(content)
    else:
        content = mmcv.load(file_path)
    assert isinstance(content, dict)
    return content


@contextmanager
def open_file(path: str, mode: str = None, cachedir: str = HDFS_CACHE):
    """
    Open file in hdfs, support local cache.
    """
    tmp_path = None
    if "hdfs://" in path:
        tmp_path = path.replace("/", "_").replace(":", "_")
        if cachedir:
            if not os.path.exists(cachedir):
                os.makedirs(cachedir)
            tmp_path = os.path.join(cachedir, tmp_path)
            if not os.path.exists(tmp_path):
                copy_command = "hdfs dfs -get %s %s" % (path, tmp_path)
                logger.info(copy_command)
                os.system(copy_command)
            else:
                logger.info("use cache %s" % tmp_path)
        else:
            tmp_path = "%s_%s" % (os.path.basename(path), str(os.getpid()))
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            copy_command = "hdfs dfs -get %s %s" % (path, tmp_path)
            logger.info(copy_command)
            os.system(copy_command)
        r = open(tmp_path, mode)
    else:
        r = open(path, mode)
    try:
        yield r
    finally:
        r.close()
        if tmp_path is not None and cachedir is None:
            os.remove(tmp_path)


path_manager = PathManagerFactory.get(defaults_setup=True)

path_manager.register_handler(HTTPURLHandler())
