import os
import git
from .utils import (
    execute_option_hooks
)

class LocalRepository:

    def __init__(self, options=None):


        self.repo_name = options.get(
            'repo_name',
            default=os.getcwd().split('/')[-1]
        )
        self.remote_name = options.get('remote_name', default='origin')
        self.remote_branch = options.get('remote_branch', default='main')

        if options.get('repo_subdirectory'):
            self.repo_path = os.path.join(
                os.getcwd(),
                options.get('repo_subdirectory')
            )

        else:
            self.repo_path = os.getcwd()

        if os.path.isdir('{repo_path}/.git'.format(repo_path=self.repo_path)):
            self._repo = git.Repo(path=self.repo_path)
            self._branch = self._repo.head
            self._remote = self._repo.remotes[self.remote_name]
            self.repo_branch = self._repo.active_branch
            self.repo_url = self._remote.url
        
        else:
            self._repo = None
            self._branch = None
            self._remote = None
            self.repo_branch = options.get('repo_branch', default='main') 
            self.repo_url = options.get('repo_url')

        self.options = options

    def execute(self, command=None):
        if command is None:
            raise Exception('Error: Command is not specified.')

        return super(LocalRepository, self).__getattribute__(command)()

    def init(self):

        if self.options.get('bare'):
            self._repo = git.Repo.init(
                self.repo_path,
                bare=self.options.get('bare')
            )

        else:
            self._repo = git.Repo.init(self.repo_path)

        return self

    @execute_option_hooks(options=['untracked', 'files'])
    def add(self):
        untracked = self.options.get('untracked')
        files = self.options.get('files')

        if files:
            self._repo.index.add(files)
        elif untracked:
            self._repo.index.add(self._repo.untracked_files)
        else:
            self._repo.git.add(A=True)

        return self

    def add_remote(self):
        self._remote = self._repo.create_remote(
            self.remote_name,
            self.repo_url
        )

        self._repo.create_head(
            self.repo_branch,
            self._remote.refs.main
        ).set_tracking_branch(
            self._remote.refs.main
        ).checkout()

        return self

    def branch(self):
        self._repo.create_head(self.repo_branch)
        return self

    def checkout(self):
        self._branch = self._repo[self.repo_branch].checkout()
        return self

    def clone(self):
        self._repo = git.Repo.clone_from(
            self.repo_url,
            self.repo_path,
            branch=self.repo_branch
        )
        return self

    @execute_option_hooks(options=['commit_message'])
    def commit(self):
        self._repo.index.commit(self.options.get('commit_message'))

        return self

    def fetch(self):
        self._remote = self._repo.remote(name=self.remote_name)

        if self._remote.exists():
            self._remote.fetch()
        else:
            raise Exception('Error: Remote does not exist or URL is invalid.')

        return self

    def pull(self):
        self._remote = self._repo.remote(name=self.remote_name)

        if self._remote.exists():
            self._remote.pull(self.remote_branch)
        else:
            raise Exception('Error: Remote does not exist or URL is invalid.')

        return self

    @execute_option_hooks(options=[])
    def push(self):
        self._remote = self._repo.remote(name=self.remote_name)

        if self._remote.exists():
            self._remote.push(self.remote_branch)
        else:
            raise Exception('Error: Remote does not exist or URL is invalid.')

        return self
