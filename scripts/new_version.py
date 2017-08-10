import os, subprocess, sys

DRY_RUN = False


def call(s, *args):
    caller = print if DRY_RUN else subprocess.check_call
    return caller(s.split() + list(args))


def split_version(s):
    return tuple(int(i) for i in s.split('.'))


def new_version(new_version_string, comment):
    root_file = os.path.dirname(os.path.dirname(__file__))
    version_file = os.path.join(root_file, 'gitty', 'VERSION')

    old_version = split_version(open(version_file).read())
    new_version = split_version(new_version_string)

    assert new_version > old_version

    if not DRY_RUN:
        with open(version_file, 'w') as fp:
            fp.write(new_version_string)
            fp.write('\n')

    commit_comment = 'Update to version %s' % new_version_string
    call('git commit gitty/VERSION -m', commit_comment)
    call('git push')
    call('git tag v%s -am' % new_version_string, comment)
    call('git push --tag')
    call('python3.5 setup.py sdist upload -r pypi')


new_version(*sys.argv[1:])
