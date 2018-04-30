# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = 1
_version_extra = 'dev'

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research/Government",
               "License :: OSI Approved :: GNU License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering/Government"]

# Description should be a one-liner:
description = "cdp: tools and functions to support CouncilDataProject servers"
# Long description will go up on the pypi page
long_description = """
cdp
========
cdp is the tools and functions library built to help run CouncilDataProject
supported cities. It includes Legistar and video IO and processing tools and
incorporates tools from other CouncilDataProject created libraries that assist
in simple transcription task and topic and sentiment analysis.
Contact
=======
Jackson Maxfield Brown
jmaxfieldbrown@gmail.org
License
=======
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see http://www.gnu.org/licenses/.
"""

NAME = "cdp"
MAINTAINER = "Jackson Maxfield Brown"
MAINTAINER_EMAIL = "jmaxfieldbrown@gmail.org"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/CouncilDataProject/cdp"
DOWNLOAD_URL = "https://github.com/CouncilDataProject/cdp"
LICENSE = "GNU"
AUTHOR = "Jackson Maxfield Brown"
AUTHOR_EMAIL = "jmaxfieldbrown@gmail.org"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
REQUIRES = [
            "bs4",
            "pydub",
            "requests",
            "speechrecognition"
            ]
SCRIPTS = [
            "cdp/bin/run_cdp_server.py"
            ]
