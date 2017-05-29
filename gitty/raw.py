PROVIDERS = {
    'github.com': ('raw.githubusercontent.com', ),
    'gitlab.com': ('gitlab.com', '/raw'),
}


def raw_url(url, providers=PROVIDERS):
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


"""

Motivating examples were:

https://github.com /ManiacalLabs/BiblioPixel /blob /master/tox.ini
https://raw.githubusercontent.com /ManiacalLabs/BiblioPixel /master/tox.ini

https://github.com /ManiacalLabs/BiblioPixel /blob /dev/test/project.json
https://raw.githubusercontent.com /ManiacalLabs/BiblioPixel /dev/test/project.json

https://gitlab.com/ase/ase /blob /fix_wannier/doc/Makefile
https://gitlab.com/ase/ase /raw /fix_wannier/doc/Makefile

https://gitlab.com/ase/ase /blob /master/ase/geometry/distance.py
https://gitlab.com/ase/ase /raw /master/ase/geometry/distance.py

"""
