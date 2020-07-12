from .bitbucket_repository import BitbucketRepository

class BitbucketRepositoryCollection:

    def __init__(self, projects=None, options=None, api=None):
        self.repositories = {}

        for project in projects:
            for repository in project.list_repos(project.get('key')):
                self.repositories[repository.get('name')] = BitbucketRepository(
                    repository=repository,
                    options=options,
                    api=api,
                    project_key=project.get('key')
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

