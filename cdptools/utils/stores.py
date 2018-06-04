from cdptools.utils import checks
import pathlib
import json
import os

def store_json_data(data, store_path, overwrite=False):
    """
    Store the provided data at the provided path.

    Example:
    ==========
    ```
        >>> data = {"foo": "bar"}
        >>> path = "/foo/bar/baz.json"
        >>> store_json_data(data, path)
        Stored: /foo/bar/baz.json

        >>> store_json_data(data, path)
        FileExistsError: File exists already and overwrite is False

        >>> store_json_data(data, path, True)
        Stored: /foo/bar/baz.json

        >>> path = "/foo/bar/baz"
        >>> real_path = store_json_data(data, path, True)
        >>> Stored: /foo/bar/baz.json

        >>> print(real_path)
        /foo/bar/baz.json
    ```

    Parameters
    ==========
    data: list, dict
        The data to store at the provided path.
    store_path: str, pathlib.Path
        Where to store the provided data.
    overwrite: bool
        Should the file be overwritten if a file already exists at the provided
        path.

    Returns
    ==========
    real_path: pathlib.Path
        Returns the true path of where the data was stored.

    Errors
    ==========
    FileExistsError:
        A file already exists at the provided path and overwrite is False.
    """

    # enforce types
    checks.check_types(data, [list, dict])
    checks.check_types(store_path, [str, pathlib.Path])
    checks.check_types(overwrite, bool)

    # convert to pathlib.Path
    if not isinstance(store_path, pathlib.Path):
        store_path = pathlib.Path(store_path)

    # ensure the file will be stored as json
    if ".json" not in store_path.suffixes:
        store_path = store_path.with_suffix(".json")

    # dump data
    if not os.path.exists(store_path) or overwrite:
        with open(store_path, 'w') as outfile:
            json.dump(data, outfile)
            print("Stored:", store_path)
            return store_path

    # raise error
    raise FileExistsError("File exists already and overwrite is False")
