# gitty

A library to load Python code and raw text from git repositories.

# Basic usage

    import gitty

    # Permanently extend sys path with this github repo.
    gitty.sys_path.extend(['github.com/timedata-org/simple']):

    from simple import basic
    basic.run(basic.FOO, basic.BAR)

    with gitty.sys_path.extender():

    with gitty.
