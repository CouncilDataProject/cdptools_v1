from cdptools.utils import checks
import requests

def get_legistar_object(city, query="Bodies", begin=0, pages=1):
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

    err_footer = """
Ex: http://webapi.legistar.com/v1/seattle/Matters?$skip=1000
Would query for a list of matters against the Seattle Legistar API and skip the
first 1000 results.
"""

    check_city_err = """
get_legistar_object requires the "city" parameter to be a string to complete.
""" + err_footer

    check_query_err = """
get_legistar_object requires the "query' parameter to be a string to complete.
""" + err_footer

    check_begin_err = """
get_legistar_object requires the "begin" parameter to be an integer to complete.
""" + err_footer

    check_pages_err = """
get_legistar_object requires the "pages" parameter to be an integer or string
    "all" to complete.
""" + err_footer

    check_types(city, [str], check_city_err)
    check_types(query, [str], check_query_err)
    check_types(begin, [int], check_begin_err)
    check_types(pages, [int, str], check_pages_err)

    url = "http://webapi.legistar.com/v1/{c}/{q}?$skip={s}"
    results = []

    if pages == "all":
        pages = sys.maxsize

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
