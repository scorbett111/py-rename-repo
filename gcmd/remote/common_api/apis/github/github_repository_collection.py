import github
from .github_repository import GithubRepository

class GithubRepositoryCollection:

    def __init__(self, repositories=None, options=None):
        self.collection = {}
        self.options = options

        if repositories:
            for repository in self.collection:
                self.collection[repository.name] = GithubRepository(
                    repository=repository,
                    options=options
                )

    def __iter__(self):
        for repository in self.collection:
            yield repository

    def __getitem__(self, repository_name):
        return self.collection.get(repository_name)

    def __setitem__(self, repository_name, repository):
        self.collection[repository_name] = repository

    def delete(self, repository_name):
        if self.collection.get(repository_name):
            del self.collection[repository_name]
