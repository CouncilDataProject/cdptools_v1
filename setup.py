#!/usr/bin/env python

import os
from setuptools import setup, find_packages

exclude_dirs = ["v1.0",
                "docker",
                "examples",
                "work_in_progress"]

PACKAGES = find_packages(exclude=exclude_dirs)

# Get version and release info, which is all stored in cdpprocessor/version.py
ver_file = os.path.join("cdpprocessor", "version.py")
with open(ver_file) as f:
    exec(f.read())

opts = dict(name=NAME,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            classifiers=CLASSIFIERS,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            platforms=PLATFORMS,
            version=VERSION,
            packages=PACKAGES,
            install_requires=REQUIRES,
            requires=REQUIRES,
            scripts=SCRIPTS)

if __name__ == "__main__":
    setup(**opts)
