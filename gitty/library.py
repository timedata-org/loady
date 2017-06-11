import git, os, shutil
from . import config, files


def clear_library_cache(prompt=True):
    """Clear gitty's cache."""
    if prompt:
        answer = input(
            'Clear library cache files in %s/? (yN) ' % config.cache())
        if not answer.startswith('y'):
            return False
    shutil.rmtree(config.cache(), ignore_errors=True)
    return True


class Library(object):
    """Represents a single Python library loaded from a git repository."""

    CHECKOUT = 'https://:@{provider}/{user}/{project}.git'

    def __init__(self, provider, user, project, branch='master', commit=None):
        self.provider = provider
        self.user = user
        self.project = project
        self.branch = branch
        self.commit = commit

        path = [config.cache(), provider, user, project, commit or branch]
        path = [files.sanitize(p) for p in path]
        self.path = os.path.join(*path)

    def pull(self):
        git.Repo(self.path).remote().pull(self.branch)

    def load(self):
        """Load a library.  Returns true if the library was loaded or reloaded,
           false if the library already existed."""
        if os.path.exists(self.path):
            if not config.CACHE_DISABLE:
                return False
            shutil.rmtree(self.path, ignore_errors=True)

        with files.remove_on_exception(self.path):
            url = self.CHECKOUT.format(**vars(self))
            repo = git.Repo.clone_from(url=url, to_path=self.path, b=self.branch)
            if self.commit:
                repo.head.reset(self.commit, index=True, working_tree=True)
            return True
