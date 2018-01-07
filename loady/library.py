import os, shutil
from . import config, files, whitelist

try:
    import git
except:
    git = None


def clear(prompt=True, cache=None):
    """Clear loady's cache."""
    cache = cache or config.cache()
    if prompt:
        answer = input(
            'Clear library cache files in %s/? (yN) ' % cache)
        if not answer.startswith('y'):
            return False
    shutil.rmtree(cache, ignore_errors=True)
    return True


class Library(object):
    """Represents a single Python library loaded from a git repository."""

    GIT_URL = 'https://:@{provider}/{user}/{project}.git'

    def __init__(self, provider, user, project,
                 branch='master', commit=None, cache=None):
        whitelist.check_entry(provider, user, project, branch, commit)

        self.provider = provider
        self.user = user
        self.project = project
        self.branch = branch
        self.commit = commit
        cache = cache or config.cache()

        path = [config.cache(), provider, user, project, commit or branch]
        path = [files.sanitize(p) for p in path]
        self.path = os.path.join(*path)

    def pull(self):
        """
        Pull the git repo from its origin.  Can only be called after load()
        has been called.
        """
        git.Repo(self.path).remote().pull(self.branch)

    def load(self):
        """Load the library."""
        if not git:
            raise EnvironmentError(MISSING_GIT_ERROR)

        if os.path.exists(self.path):
            if not config.CACHE_DISABLE:
                return
            shutil.rmtree(self.path, ignore_errors=True)

        with files.remove_on_exception(self.path):
            url = self.GIT_URL.format(**vars(self))
            repo = git.Repo.clone_from(
                url=url, to_path=self.path, b=self.branch)
            if self.commit:
                repo.head.reset(self.commit, index=True, working_tree=True)


def create(gitpath, cache=None):
    """
    Create a Library from a git path.

    """
    if gitpath.startswith(config.LIBRARY_PREFIX):
        path = gitpath[len(config.LIBRARY_PREFIX):]
        return Library(*path.split('/'), cache=cache)


def to_path(gitpath, cache=None):
    library = create(gitpath, cache)
    if not library:
        return gitpath

    library.load()
    return library.path


MISSING_GIT_ERROR = """
Unable to load the Python library GitPython.  The cause might be that
the program git is not installed on your computer.

Try installing git using these instructions:

    https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
"""
