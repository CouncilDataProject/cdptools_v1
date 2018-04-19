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
                        "bodies",
                        "body_types",
                        "active",
                        "names",
                        "short_names"
                        ]
        self.update()

    def get_bodies(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a json object of bodies queried from the Legistar API.
        """

        return self.get_legistar_object("Bodies").json()

    def get_body_types(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a json object of body_types queried from the Legistar API.
        """

        return self.get_legistar_object("BodyTypes").json()

    def get_active(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a list of active bodies queried from the Legistar API.
        """

        active = list()
        for body in self.bodies:
            if body["BodyActiveFlag"] == 1:
                active.append(body)

        return active

    def get_names(self):
        """
        Parameters
        ----------
        self: BodyPipe
            The BodyPipe that stores which city to query data for.

        Output
        ----------
        Returns a list of body names queried from the Legistar API.
        """

        return [body["BodyName"] for body in self.bodies]

    def get_short_names(self):
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

        if self.shortener is None:
            short_names = self.names
        else:
            short_names = self.shortener(self.bodies)

        return short_names
