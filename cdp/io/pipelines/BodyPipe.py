from .LegistarPipe import *

class BodyPipe(LegistarPipe):
    """
    Extends
    ---------
    cdp.io.pipelines.LegistarPipe

    Parameters
    ----------
    city: str
        A Legistar supported city to query against.
    name_shortener: function
        A custom name shortening function.
    """

    def __init__(self, city, name_shortener=None):
        """
        Parameters
        ----------
        city: str
            A Legistar supported city to query against.
        name_shortener: function
            A custom body name shortening function.
        """

        check_city_err = """
BodyPipe requires a legistar city name to initialize.
Given: {s_type}
Please view our documentation for an example.
"""

        check_shortener_err = """
The provided custom body name shortener function is not callable.
Given: {f_type}
Please view our documentation for an example.
"""

        self.city = check_string(city, check_city_err)
        if name_shortener is not None:
            self.shortener = check_function(name_shortener, check_shortener_err)
        else:
            self.shortener = None

        self.updatable = [
                            "_bodies",
                            "_body_types",
                            "_active",
                            "_names",
                            "_short_names"
                            ]

        self.update()

    @property
    def bodies(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a json object of bodies queried from the Legistar API.
        """

        if self._bodies is None:
            self._bodies = self.get_legistar_object("Bodies").json()

        return self._bodies

    @property
    def body_types(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a json object of body_types queried from the Legistar API.
        """
        if self._body_types is None:
            self._body_types = self.get_legistar_object("BodyTypes").json()

        return self._body_types

    @property
    def active(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a list of active bodies queried from the Legistar API.
        """

        if self._active is None:
            self._active = list()
            for body in self.bodies:
                if body["BodyActiveFlag"] == 1:
                    self._active.append(body)

        return self._active

    @property
    def names(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a list of body names queried from the Legistar API.
        """

        if self._names is None:
            self._names = [body["BodyName"] for body in self.bodies]

        return self._names

    @property
    def short_names(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a list of shortened body names queried from the Legistar API.
        If no name_shortener has been provided to the BodyPipe, this will return
        the default list of names stored in self.names.
        """

        if self._short_names is None:
            if self.shortener is None:
                self._short_names = self.names
            else:
                self._short_names = self.shortener(self.bodies)

        return self._short_names
