# atom runner fix for terminal
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from cdp.io.pipelines import BodyPipe as bp
from cdp.utils.seattle import *
from pprint import pprint

city = "seattle"
seattle_bodies = bp(city, body_name_shortener)

pprint(seattle_bodies.short_names())
