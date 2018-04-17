from pprint import pprint
import requests

def get_legistar_obj(city, obj):
    if not isinstance(city, str) or not isinstance(obj, str):
        raise TypeError("""
get_legistar_object requires a legistar city name and
which object should be queried for.

Ex: http://webapi.legistar.com/v1/seattle/Bodies
Would query for a list of bodies against the Seattle legistar API.
""")

    url = "http://webapi.legistar.com/v1/{c}/{o}"
    r = requests.get(url.format(c=city, o=obj))

    if r.status_code == 200:
        return r
    else:
        raise ValueError("""
Something went wrong with legistar get.
Status Code: {er}
""".format(er=r.status_code))

class BodyPipe:
    def __init__(self, city, name_shortener=None, prints=False):
        self.city = self.check_city_name(city)
        self.shortener = self.check_name_shortener(name_shortener)

    def check_city_name(self, city):
        if isinstance(city, str):
            return city
        else:
            raise TypeError("""
BodyPipe requires a legistar city name to initialize.
Given: {city_type}
Please view our documentation for an example.
""".format(city_type=type(city)))

    def check_name_shortener(self, shortener):
        if callable(shortener) or shortener is None:
            return shortener
        else:
            raise TypeError("""
If you want to add a custom name body name shortener function
to a BodyPipe, it must be a callable function.
Given: {s_type}
Please view our documentation for an example.
""".format(s_type=type(shortener)))

    def bodies(self):
        if not hasattr(self, "_bodies"):
            self._bodies = get_legistar_obj(self.city, "Bodies").json()

        return self._bodies

    def body_types(self):
        if not hasattr(self, "_body_types"):
            self._body_types = get_legistar_obj(self.city, "BodyTypes").json()

        return self._body_types

    def active(self):
        if not hasattr(self, "_active"):
            active = list()
            for i, body in enumerate(self.bodies()):
                if body["BodyActiveFlag"] == 1:
                    active.append(body)
            self._active = active

        return self._active

    def names(self):
        if not hasattr(self, "_names"):
            self._names = [b["BodyName"] for b in self.bodies()]

        return self._names

    def short_names(self):
        if not hasattr(self, "_short_names"):
            if self.shortener is None:
                self._short_names = self.names()
            else:
                self._short_names = self.shortener(self.bodies())

        return self._short_names

class VideoPipe:
    def __init__(self, func=None, prints=False):
        if not callable(func):
            raise TypeError("""
VideoPipe requires a video url collection function to initialize.
Given: {func_type}
Please view our documentation for an example.
""".format(func_type=type(func)))

        self.getter = func
