import requests

def get_legistar_object(city, query="Bodies"):
    """
    Parameters
    ----------
    city: str
        A Legistar supported city to query against.
    query: str
        Which type of data to query for.
        (Default: "Bodies")

    Output
    ----------
    Returns the json object found from the successful query.
    Unsuccessful queries will raise a ValueError.
    """

    check_city_err = """
get_legistar_object requires a legistar city name to complete.
Given: {s_type}
Please view our documentation for an example.

Ex: http://webapi.legistar.com/v1/seattle/Bodies
Would query for a list of bodies against the Seattle Legistar API.
"""

    check_query_err = """
get_legistar_object requires a query type to complete.
Given: {s_type}
Please view our documentation for an example.

Ex: http://webapi.legistar.com/v1/seattle/Bodies
Would query for a list of bodies against the Seattle Legistar API.
"""

    check_string(city, check_city_err)
    check_string(query, check_query_err)

    url = "http://webapi.legistar.com/v1/{c}/{q}"
    try:
        r = requests.get(url.format(c=city, q=query))

        if r.status_code == 200:
            return r.json()
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
