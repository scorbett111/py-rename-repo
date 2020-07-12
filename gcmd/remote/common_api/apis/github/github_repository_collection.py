import github
from .github_repository import GithubRepository

class GithubRepositoryCollection:

    def __init__(self, repositories=None, options=None):
        self.repositories = {}
        self.options = options

        for repository in self.repositories:
            self.repositories[repository.name] = GithubRepository(
                repository=repository,
                options=options
            )

    def __iter__(self):
        for repository in self.repositories:
            yield repository

    def __getitem__(self, repository_name):
        return self.repositories.get(repository_name)

    def __setitem__(self, repository_name, repository):
        self.repositories[repository_name] = repository

    def delete(self, repository_name):
        if self.repositories.get(repository_name):
            del self.repositories[repository_name]
