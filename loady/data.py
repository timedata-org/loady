import json, requests
from . import raw


def load_remote(url, use_json):
    """Return data at the raw version of a URL, or raise an exception.

    If the URL ends in .json and json=True, convert the data from JSON.
    """
    r = requests.get(raw.raw(url))
    if not r.ok:
        raise ValueError('Couldn\'t read %s with code %s:\n%s' %
                         url, r.status_code, r.text)
    return r.json if use_json else r.text


def load_local(location, use_json):
    try:
        data = open(location).read()
    except Exception as e:
        e.args = ('There was an error reading the file', location) + e.args
        raise

    if not use_json:
        return data

    try:
        return json.loads(data)
    except Exception as e:
        e.args = ('There was a JSON error in the file', location) + e.args
        raise


def load(location, json=None):
    """Return data at either a file location or at the raw version of a
    URL, or raise an exception.

    locations containing a : are URLs, otherwise they are file
    locations.

    If the URL ends in .json and json=True, convert the data from JSON."""

    if json is None:
        json = location.endswith('.json')

    f = load_remote if ':' in location else load_local
    return f(location, json)
