URL_REWRITERS = {
    'github.com': {
        'provider': 'raw.githubusercontent.com',
        'path': [],
    },
    'gitlab.com': {
        'provider': 'gitlab.com',
        'path': ['raw'],
    },
}


def raw(url, url_rewriters=URL_REWRITERS):
    """Return a raw version of the URL if there is one.
    Otherwise returns the original URL.

    Many repos have "raw" and "user-friendly" versions of each URL.  Usually
    when you want to download something programmatically, you want the raw
    version, but users will enter the user-friendly version as it is the one
    they usually see.

    If this function recognizes one of those cases, it converts the
    user-friendly URL into the raw - otherwise it returns the original URL.

    The function works by default for two git providers: github and gitlab.
    You can use others by passing in your own url_rewriters list.
    """
    # https: /     /github.com/user/ project/ blob/ master/tox.ini
    try:
        protocol, empty, provider, user, project, _, *rest = url.split('/')
    except:
        return url

    rewriter = url_rewriters.get(provider)

    if protocol and (not empty) and user and project and rest and rewriter:
        parts = [protocol, empty, rewriter['provider'], user, project]
        return '/'.join(parts + rewriter['path'] + rest)

    return url


def request(url, url_rewriters=URL_REWRITERS, json=True):
    """Return data at the raw version of a URL, or raise an exception.

    If the URL ends in .json and json=True, convert the data from JSON.
    """
    try:
        import requests
    except ImportError as e:
        e.args += (_REQUESTS_ERROR, )
        raise

    r = requests.get(raw(url, url_rewriters))
    if not r.ok:
        raise ValueError('Couldn\'t read %s with code %s:\n%s' %
                         url, r.status_code, r.text)
    return r.json if json and url.endswith('.json') else r.text


_REQUESTS_ERROR = """\
You need to import the requests library.  Try typing:

    pip import requests

at the command line.
"""
