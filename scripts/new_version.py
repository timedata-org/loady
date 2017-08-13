import os, subprocess, sys

DRY_RUN = False


def call(s, *args):
    caller = print if DRY_RUN else subprocess.check_call
    return caller(s.split() + list(args))


def split_version(s):
    return tuple(int(i) for i in s.split('.'))


def new_version(comment, new_version_string=''):
    root_file = os.path.dirname(os.path.dirname(__file__))
    version_file = os.path.join(root_file, 'loady', 'VERSION')

    old_version = split_version(open(version_file).read())

    if new_version_string:
        new_version = split_version(new_version_string)
    else:
        new_version = old_version[:2] + (old_version[2] + 1,)
        new_version_string = '.'.join(str(i) for i in new_version)

    assert new_version > old_version

    if not DRY_RUN:
        with open(version_file, 'w') as fp:
            fp.write(new_version_string)
            fp.write('\n')

    commit_comment = 'Update to version %s' % new_version_string
    call('git commit loady/VERSION -m', commit_comment)
    call('git push')
    call('git tag v%s -am' % new_version_string, comment)
    call('git push --tag')
    call('python3.5 setup.py sdist upload -r pypi')


new_version(*sys.argv[1:])
