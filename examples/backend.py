# atom runner fix for terminal
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from cdpprocessor.io import pipelines
from cdpprocessor.utils import seattle
from pprint import pprint

import datetime

city = "seattle"
s_bodies = pipelines.BodyPipe(city, seattle.body_name_shortener)
pprint(s_bodies.short_names)
