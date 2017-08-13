# loady

Dynamically load Python libraries, JSON and raw text from git repositories and
the web.

# Basic usage

    import loady

    # Permanently extend sys path with this github repo.
    loady.extend_sys_path('//git/github.com/timedata-org/simple'):

    # Temporarily extend sys path with this github repo.
    with loady.sys_path.extender('//git/github.com/timedata-org/simple'):
        # Do stuff.

    # Get raw data from URLs.
    result = loady.raw.request(
        'https://github.com/timedata-org/simple/blob/master/simple.json')

    # Actualy gets the raw data from this URL:
    # https://raw.githubusercontent.com/timedata-org/simple/master/simple.json
    # and reads it as JSON.
