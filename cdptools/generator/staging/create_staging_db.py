def create_staging_db(client="seattle", storage="/cdp/stg/", update=False):
    # ensure param types
    checks.check_types(client, [str])
    checks.check_types(storage, [str])
    checks.check_types(update, [bool])

    client = client.lower()
    if isinstance(storage, str):
        storage = pathlib.Path(storage)

    if client not in str(storage):
        storage /= client

    print("-" * 80)
    print("Creating CDP NoSQL test/ staging database for client:", client,
          "\nWill store completed json at:", storage,
          "\nWill update existing json:", update)
    print("-" * 80)

    for file in os.listdir(storage):
        print(file)

    # TODO:
    # process tables into NoSQL schema

    print("-" * 80)
    print("CDP NoSQL test/ staging database complete")
    print("-" * 80)
