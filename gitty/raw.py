PROVIDERS = {
    'github.com': ('raw.githubusercontent.com', ),
    'gitlab.com': ('gitlab.com', '/raw'),
}


def raw(url, providers=PROVIDERS):
    """Return a raw version of the URL if there is one.
    Otherwise, it returns the original URL.

    Many repos have "raw" and "user-friendly" versions of each URL.  Usually
    when you want to download something programmatically, you want the raw
    version, but users will want to enter the user-friendly version.

    In those cases this functions converts the user-friendly URL into the raw
    one - otherwise it returns the original URL.

    The function works by default for two providers: github and gitlab.
    You can use others by passing in your own providers list.
    """
    try:
        # https: /        /github.com/user/project/blob / master/tox.ini
        protocol, nothing, provider, user, project, sep, *rest = url.split('/')
        raw_provider, *path = providers[provider]

    except:
        # Not as we expected.
        return url

    if nothing or not (protocol and user and project and sep and rest):
        # Not as we expected.
        return url

    parts = [protocol, nothing, raw_provider, user, project] + path + rest
    return '/'.join(parts)


def request(url, providers=PROVIDERS, json=True):
    """Return data at the raw version of a URL, or raise an exception.

    If the URL ends in .json and json=True, convert the data from JSON.
    """
    try:
        import requests

    except ImportError as e:
        e.args += (_REQUESTS_ERROR, )
        raise

    r = requests.get(raw(url))
    if not r.ok:
        raise ValueError('Couldn\'t read %s with code %s:\n%s' %
                         url, r.status_code, r.text)
    return r.json if json and url.endswith('.json') else r.text


_REQUESTS_ERROR = """\
You need to import the requests library.  Try typing:

    pip import requests

at the command line.
"""


"""Motivating examples were:

https://github.com /ManiacalLabs/BiblioPixel /blob /master/tox.ini
https://raw.githubusercontent.com /ManiacalLabs/BiblioPixel /master/tox.ini

https://github.com /ManiacalLabs/BiblioPixel /blob /dev/test/project.json
https://raw.githubusercontent.com /ManiacalLabs/BiblioPixel /dev/test/project.json

https://gitlab.com/ase/ase /blob /fix_wannier/doc/Makefile
https://gitlab.com/ase/ase /raw /fix_wannier/doc/Makefile

https://gitlab.com/ase/ase /blob /master/ase/geometry/distance.py
https://gitlab.com/ase/ase /raw /master/ase/geometry/distance.py

"""
