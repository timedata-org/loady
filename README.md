# gitty

Dynamically load Python libraries, JSON and raw text from git repositories.

# Basic usage

    import gitty

    # Permanently extend sys path with this github repo.
    gitty.extend_sys_path('//git/github.com/timedata-org/simple'):

    # Temporarily extend sys path with this github repo.
    with gitty.sys_path.extender('//git/github.com/timedata-org/simple'):
        # Do stuff.

    # Get raw data from URLs.
    result = gitty.raw.request(
        'https://github.com/timedata-org/simple/blob/master/simple.json')

    # Actualy gets the raw data from this URL:
    # https://raw.githubusercontent.com/timedata-org/simple/master/simple.json
    # and reads it as JSON.
