# atom runner fix for terminal
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from cdp.io import pipelines
from cdp.utils import seattle
from pprint import pprint

city = "seattle"
s_bodies = pipelines.BodyPipe(city, seattle.body_name_shortener)

pprint(s_bodies.short_names)
