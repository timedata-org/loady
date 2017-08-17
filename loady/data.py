import functools, json, os, requests
from . import raw, whitelist


@functools.lru_cache()
def load(location, use_json=None):
    """Return data at either a file location or at the raw version of a
    URL, or raise an exception.

    A file location either contains no colons like /usr/tom/test.txt,
    or a single character and a colon like C:/WINDOWS/STUFF.

    A URL location is anything that's not a file location.

    If the URL ends in .json and json=True, convert the data from JSON."""
    if not whitelist.is_file(location):
        r = requests.get(raw.raw(location))
        if not r.ok:
            raise ValueError('Couldn\'t read %s with code %s:\n%s' %
                             (location, r.status_code, r.text))
        data = r.text
    else:
        try:
            f = os.path.realpath(os.path.abspath(os.path.expanduser(location)))
            data = open(f).read()
        except Exception as e:
            e.args = (
                'There was an error reading the file', location, f) + e.args
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


cache_clear = load.cache_clear