# loady

Dynamically load Python libraries, JSON and raw text from git repositories and
the web.

# Basic usage

    import loady

    # Permanently extend sys path with this github repo.
    loady.sys_path.extend('//git/github.com/timedata-org/simple'):

    # Temporarily extend sys path with this github repo.
    with loady.sys_path.extender('//git/github.com/timedata-org/simple'):
        # Do stuff.

    # Get raw data from URLs.
    result = loady.data.load(
        'https://github.com/timedata-org/simple/blob/master/simple.json')

    # Actually gets the raw data from this URL:
    # https://raw.githubusercontent.com/timedata-org/simple/master/simple.json
    # and reads it as JSON.

    #  Loads and compiles Python code from that URL.
    result = loady.code.load(
        'https://github.com/timedata-org/simple/blob/master/test.py')
