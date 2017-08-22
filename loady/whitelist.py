import os, itertools, json
from . import config

"""

An entry in the whitelist looks like:

   [provider, user, project, filepath, branch, commit]

where the last four components are optional.

Empty components mean "match anything".
"""


def read_whitelist(filename=None):
    filename = filename or config.whitelist()
    if os.path.exists(filename):
        return json.load(open(filename))

    return []


def write_whitelist(whitelist, filename=None):
    with open(filename or config.whitelist(), 'w') as f:
        json.dump(whitelist, f)


def matches(target, entry):
    """Does the target match the whitelist entry?"""

    # It must match all the non-empty entries.
    for t, e in itertools.zip_longest(target, entry):
        if e and t != e:
            return False

    # ...and the provider and user can't be empty.
    return entry[0] and entry[1]


def matches_any(target, whitelist):
    """Does target match any entry in the whitelist?"""
    return any(matches(target, e) for e in whitelist)


def check_allow_prompt(entry, whitelist, input=input):
    def prompt(message, names):
        msg = message.format(**names)
        return input(msg).lower().strip().startswith('y')

    if matches_any(entry, whitelist):
        return True

    if config.WHITELIST_PROMPT:
        provider, user, *rest = entry[:3]
        project = rest and rest[0] or ''

        if prompt(MESSAGES[0], locals()) and prompt(MESSAGES[1], locals()):
            return False

    raise ValueError('Did not whitelist %s' % ' '.join(entry))


def check_entry(*entry):
    """Throws an exception if the entry isn't on the whitelist."""
    whitelist = read_whitelist()
    if not check_allow_prompt(entry, whitelist):
        whitelist.append(entry)
        write_whitelist(whitelist)


def is_file(name):
    if ':' not in name:
        return True

    # It might be a local Windows file!
    prefix, _ = name.split(':', 1)
    return len(prefix) == 1


def check_url(url):
    if not config.USE_WHITELIST or is_file(url):
        return

    try:
        protocol, nothing, provider, user, project = url.split('/', 5)
        if not nothing:
            raise ValueError
    except:
        raise ValueError('Cannot understand URL', url)

    check_entry(provider, user, project)


MESSAGES = [
    """
DANGER:

You are trying to download Python executable code from
https://{provider}/{user}/{project}.

That is, project {project}, user {user} at {provider}.

This Python code could do anything it wanted on your computer, including
deleting or rewriting files!

If you are sure you want this to happen, if you completely trust
{user}@{provider} to never try to harm you, then you can whitelist this project
and download the code.

Do you want to whitelist https://{provider}/{user}/{project}? (yN)""",

    """
DANGER:


Are you SURE you want to whitelist https://{provider}/{user}/{project}?

Any malicious code they write could destroy all your files!? (yN) """
]
