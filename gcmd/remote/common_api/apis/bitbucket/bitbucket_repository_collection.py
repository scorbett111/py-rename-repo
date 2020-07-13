from .bitbucket_repository import BitbucketRepository

class BitbucketRepositoryCollection:

    def __init__(self, repositories=None, options=None, config=None):
        self.collection = {}

        if repositories:
            for repository in repositories:
                self.collection[repository.get('name')] = BitbucketRepository(
                    repository=repository,
                    options=options,
                    config=config
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

