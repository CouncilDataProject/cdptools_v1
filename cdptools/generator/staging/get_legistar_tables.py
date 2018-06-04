from cdptools.processor.io.pipelines import LegistarPipe
from cdptools.utils import checks
from cdptools.utils import stores
import requests
import pathlib
import json
import os

SIMPLE = ["Actions",
          "Bodies",
          "BodyTypes",
          "CodeSections",
          "Events",
          "Indexes",
          "Matters"]
FORMATTING = {"Actions": "ActionId",
              "Bodies": "BodyId",
              "BodyTypes": "BodyTypeId",
              "CodeSections": "CodeSectionId",
              "Events": "EventId",
              "Indexes": "IndexId",
              "Matters": "MatterId"}
EXTENDED = ["Actions/{ActionId}",
            "Bodies/{BodyId}",
            "Bodies/{BodyTypeId}",
            "CodeSections/{CodeSectionId}",
            "EventDates/{BodyId}?FutureDatesOnly=True",
            "Events/{EventId}?\
                EventItems=1\
                &AgendaNote=1\
                &MinutesNote=1\
                &EventItemAttachments=1",
            "Indexes/{IndexId}",
            "Matters/{MatterId}"]

# TODO:
# instead of always getting tables
# check if they are in the storage dir provided
# if so: load from there

def get_legistar_tables(client="seattle", storage="/cdp/stg/", update=False):
    """

    """

    # ensure param types
    checks.check_types(client, [str])
    checks.check_types(storage, [str])
    checks.check_types(update, [bool])
    checks.check_string(client, "^[a-zA-Z]+$")

    # ensure client
    client = client.lower()

    # ensure and create storage dirs
    if isinstance(storage, str):
        storage = pathlib.Path(storage)
    if client not in str(storage):
        storage /= client
    if not os.path.isdir(storage):
        os.makedirs(storage)

    # begin process
    print("-" * 80)
    print("Pulling Legistar tables from client:", client,
          "\nWill store tables and completed database at:", storage,
          "\nWill update existing tables:", update)
    print("-" * 80)

    # setting up table queries
    pipe = LegistarPipe(client)

    # simple tables
    results = {}
    for query in SIMPLE:
        formatted_query = query.replace(" ", "")
        request = "v1/{c}/{q}".format(c=client, q=formatted_query)

        # TODO:
        # actual query completion
        response = pipe.get_legistar_object(formatted_query, pages="all")
        formatted_query = formatted_query.replace("/", "@")
        results[formatted_query] = response
        print("Pulled:", request)

        if isinstance(storage, pathlib.Path):
            table_store = storage / formatted_query
            stores.store_json_data(response, table_store, update)

    # TODO:
    # handle empty results (CodeSections)

    # use the first item in each simple table to get the extended tables
    format_attrs = {id: results[key][0][id] for key, id in FORMATTING.items()}

    # extended tables
    for query in EXTENDED:
        formatted_query = query.replace(" ", "")
        formatted_query = formatted_query.format(**format_attrs)
        request = "v1/{c}/{q}".format(c=client, q=formatted_query)
        request = request.replace(" ", "")

        # TODO:
        # actual query completion
        response = {}
        formatted_query = formatted_query.replace("/", "@")
        results[formatted_query] = response
        print("Pulled:", request)

        if isinstance(storage, pathlib.Path):
            table_store = storage / formatted_query
            stores.store_json_data(response, table_store, update)

    # end process
    print("-" * 80)
    print("Legistar table storage complete")
    print("-" * 80)

    # return the resultant tables
    return results
