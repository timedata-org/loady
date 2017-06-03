import git, os, shutil
from . import files, config


def clear_library_cache(prompt=True):
    """Clear gitty's cache."""
    if prompt:
        answer = input('Clear library cache at %s? (yN)' + config.root())
        if not answer.startswith('y'):
            return False
    shutil.rmtree(config.root(), ignore_errors=True)
    return True


class Library(object):
    GIT_CHECKOUT = 'git@{provider}:{user}/{project}.git'
    HTTPS_CHECKOUT = 'https://{provider}/{user}/{project}.git'

    def __init__(self, provider, user, project, branch='master', commit=None):
        self.provider = provider
        self.user = user
        self.project = project
        self.branch = branch
        self.commit = commit

        path = [library_cache(), provider, user, project, commit or branch]
        path = [files.sanitize(p) for p in path]
        self.path = os.path.join(*path)

    def pull(self):
        git.Repo(self.path).remote().pull(self.branch)

    def load(self):
        """Load a library.  Returns true if the library was loaded or reloaded,
           false if the library already existed."""
        if os.path.exists(self.path):
            if not config.NOCACHE:
                return False
            shutil.rmtree(self.path)

        with files.remove_on_exception(self.path):
            try:
                self._load(self.GIT_CHECKOUT)
            except:
                self._load(self.HTTPS_CHECKOUT)

            return True

    def _load(self, address):
        url = address.format(**vars(self))
        repo = git.Repo.init(self.path)
        origin = repo.create_remote('origin', url)
        origin.fetch()
        origin.pull(self.branch)

        if self.commit:
            repo.head.reset(self.commit, index=True, working_tree=True)
