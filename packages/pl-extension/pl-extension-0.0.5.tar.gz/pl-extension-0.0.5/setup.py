# -*- coding: utf-8 -*-

import io
import re

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    readme = f.read()

with open("LICENSE", "r") as f:
    license = f.read()

with open("requirements/build.txt", "r") as f:
    requires = []
    for line in f:
        line = line.strip()
        if not line.startswith("#"):
            requires.append(line)

with io.open("pl_extension/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

setup(
    name="pl-extension",
    version=version,
    description="extension for pytorch-lightning",
    long_description=readme,
    author="duinodu",
    author_email="472365351@qq.com",
    url="https://github.com/duinodu/pl-extension",
    project_urls={
        "Bug Tracker": "https://github.com/duinodu/pl-extension/issues",
    },
    license=license,
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests/*", "docs"]),
    python_requires=">=3.6",
    install_requires=requires,
)
