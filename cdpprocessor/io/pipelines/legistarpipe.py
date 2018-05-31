from ...utils.checks import *
import requests
import sys

ERR_FOOTER = """
Ex:
    query="Matters"
    begin=1200
    pages=2

Would query for a list of matters against the city Legistar API, skip the
first 1200 results, and return the next 2000 results.
"""

CHECK_CITY_ERR = """
LegistarPipe requires the "city" parameter to be a string to initialize.
"""

CHECK_QUERY_ERR = """
LegistarPipe requires the "query" parameter to be a string to complete.
""" + ERR_FOOTER

CHECK_BEGIN_ERR = """
LegistarPipe requires the "begin" parameter to be an integer to complete.
""" + ERR_FOOTER

CHECK_PAGES_ERR = """
LegistarPipe requires the "pages" parameter to be an integer or string
    "all" to complete.
""" + ERR_FOOTER

class LegistarPipe:
    """
    Parameters
    ----------
    city: str
        A Legistar supported city to query against.

    Usage
    ----------
    Contains the default update method for how attributes will be reset to None.
    By setting each attribute in the list of updatable attributes to None,
    the LegistarPipe getattr method will repull the data when requested.

    Contains a self referencing Legistar object get.
    """

    def __init__(self, city):
        """
        Parameters
        ----------
        city: str
            A Legistar supported city to query against.
        """

        self.city = check_types(city, [str], CHECK_CITY_ERR)

        self.updatable = []
        self.update()

    def get_legistar_object(self, query="Bodies", begin=0, pages=1):
        """
        Parameters
        ----------
        self: LegistarPipe
            The LegistarPipe that stores which city to query data for.
        query: str
            Which type of data to query for.
            (Default: "Bodies")
        begin: int
            What index should the results start from.
            (Default: 0)
        pages: int, str
            Due to the paging style return of the legistar api, how many pages
            should be returned from the request. Pass "all" to return all pages.
            (Default: 1)

        Output
        ----------
        Returns the json object found from the successful query.
        Unsuccessful queries will raise a ValueError.
        """

        # TODO:
        # cache results in _query dict

        if pages == "all":
            pages = sys.maxsize

        check_types(query, [str], CHECK_QUERY_ERR)
        check_types(begin, [int], CHECK_BEGIN_ERR)
        check_types(pages, [int], CHECK_PAGES_ERR)

        url = "http://webapi.legistar.com/v1/{c}/{q}?$skip={s}"
        results = []

        process = range(begin, begin + (pages*1000), 1000)
        for skip in process:
            try:
                r = requests.get(url.format(c=self.city, q=query, s=skip))

                if r.status_code == 200:
                    results += r.json()
                    if len(results) % 1000 != 0:
                        break

                else:
                    raise ValueError("""
Something went wrong with legistar get.
Status Code: {err}
""".format(err=r.status_code))

            except requests.exceptions.ConnectionError:
                raise requests.exceptions.ConnectionError("""
Something went wrong with legistar connection.
Could not connect to server.
""")

        return results

    def update(self):
        """
        Parameters
        ----------
        self: LegistarPipe
            The LegistarPipe that stores which city to query data for.

        Output
        ----------
        Will set all attributes found in the LegistarPipe's updatable attribute
        list to None as a way to force the next getattr call on an updatable
        attribute to reinitialize the desired attribute.
        """

        for attr in self.updatable:
            setattr(self, attr, None)
