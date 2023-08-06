import os
from distutils.version import LooseVersion

PL_EXTENSION_CACHE = os.getenv(
    "PL_EXTENSION_CACHE", os.path.expanduser("~/.cache/pl_extension/")
)

HDFS_CACHE = PL_EXTENSION_CACHE


def check_version(name, version, strict=False):
    if strict:
        status = LooseVersion(name.__version__) == LooseVersion(version)
        msg = (
            f"{name.__name__}=={version} is required, "
            f"but found {name.__version__}."
        )
    else:
        status = LooseVersion(name.__version__) >= LooseVersion(version)
        msg = (
            f"{name.__name__}>={version} is required, "
            f"but found {name.__version__}."
        )
    if not status:
        raise ImportError(msg)
