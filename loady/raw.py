import json, requests
from bs4 import BeautifulSoup


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


def raw(url):
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

    There is also a special case for Github gists.
    """
    try:
        # If it's a user-friendly gist URL, get the real data by parsing
        # the file.
        parts = url.split('/')
        if parts[2] == 'gist.github.com' and '.' not in parts[:-1]:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            raw_links = [i for i in soup.find_all('a') if i.text == 'Raw']
            return ('https://gist.githubusercontent.com' +
                    raw_links[0].attrs['href'])
    except Exception as e:
        print('Failed open and parse', url, e)
        pass

    # https: /     /github.com/user/ project/ blob/ master/tox.ini
    try:
        protocol, empty, provider, user, project, _, *rest = url.split('/')
    except:
        return url

    rewriter = URL_REWRITERS.get(provider)

    if protocol and (not empty) and user and project and rest and rewriter:
        parts = [protocol, empty, rewriter['provider'], user, project]
        return '/'.join(parts + rewriter['path'] + rest)

    return url
