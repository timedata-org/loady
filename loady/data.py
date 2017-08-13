import json, requests
from . import raw


def load(location, use_json=None):
    """Return data at either a file location or at the raw version of a
    URL, or raise an exception.

    locations containing a : are URLs, otherwise they are file
    locations.

    If the URL ends in .json and json=True, convert the data from JSON."""
    if ':' in location:
        r = requests.get(raw.raw(location))
        if not r.ok:
            raise ValueError('Couldn\'t read %s with code %s:\n%s' %
                             location, r.status_code, r.text)
        data = r.text
    else:
        try:
            data = open(location).read()
        except Exception as e:
            e.args = ('There was an error reading the file', location) + e.args
            raise

    if use_json is None:
        use_json = location.endswith('.json')

    if not use_json:
        return data

    try:
        return json.loads(data)
    except Exception as e:
        e.args = ('There was a JSON error in the file', location) + e.args
        raise
