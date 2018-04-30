#!/usr/bin/env python

from cdp.io import pipelines
from cdp.utils import seattle
from pprint import pprint

import datetime

city = "seattle"
s_bodies = pipelines.BodyPipe(city, seattle.body_name_shortener)
pprint(s_bodies.short_names)
