import git, os, shutil
from . import files

CHECKOUT_ROOT = os.path.expanduser('~/.gitty')
GIT_CHECKOUT = 'git@{provider}:{user}/{project}.git'
HTTPS_CHECKOUT = 'https://{provider}/{user}/{project}.git'



def clear_cache(cache_files=CHECKOUT_ROOT):
    shutil.rmtree(cache_files, ignore_errors=True)


class Library(object):

    def __init__(self, provider, user, project,
                 branch='master', commit=None, root=CHECKOUT_ROOT):
        self.provider = provider
        self.user = user
        self.project = project
        self.branch = branch
        self.commit = commit
        self.root = root

        path = [root, provider, user, project, commit or branch]
        path = (files.sanitize(p) for p in path)
        self.path = os.path.join(*path)

    def pull(self):
        git.Repo(self.path).remote().pull(self.branch)

    def load(self, force_reload=False):
        """Load a library.  Returns true if the library was loaded or reloaded,
           false if the library already existed."""
        if os.path.exists(self.path):
            if not force_reload:
                return False
            shutil.rmtree(self.path)

        with files.remove_on_exception(self.path):
            def load_at(address):
                url = address.format(**vars(self))
                repo = git.Repo.init(self.path)
                origin = repo.create_remote('origin', url)
                origin.fetch()
                origin.pull(self.branch)

                if self.commit:
                    repo.head.reset(self.commit, index=True, working_tree=True)

            try:
                load_at(GIT_CHECKOUT)
            except:
                load_at(HTTPS_CHECKOUT)

            return True
