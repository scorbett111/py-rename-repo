import atlassian
from .bitbucket_repository import BitbucketRepository
from .bitbucket_repository_collection import BitbucketRepositoryCollection

class Bitbucket:

    def __init__(self, auth=None, command=None):

        if auth.type == 'key_cert':
            self.api = atlassian.Bitbucket(
                auth.url,
                key=auth.key,
                cert=auth.cert
            )
        
        else:
            self.api = atlassian.Bitbucket(
                auth.url,
                username=auth.user,
                password=auth.password
            )

        self.service_name = 'github'
        self.command = command.name
        self.options = command.options
        self.hooks = command.hooks
        self.user = self.api.get_user()
        self.repositories = BitbucketRepositoryCollection(
            projects=self.api.project_list(),
            options=command.options,
            api=self.api
        )

    def create_repository(self):
        repository = self.api.create_repo(
            self.options.get('project'),
            self.options.get('repo_name'),
            forkable=self.options.get('forkable'),
            is_private=self.options.get('private')
        )
        self.repositories[repository.get('name')] = BitbucketRepository(
            repository=repository,
            options=self.options
        )

    def delete_repository(self):
        repo_name = self.options.get('repo_name')
        self.repositories[repo_name].delete()
        self.repositories.delete(repo_name)
    