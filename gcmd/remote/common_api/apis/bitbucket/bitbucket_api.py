from .utils import HttpSession
import requests_oauthlib
from .bitbucket_repository import BitbucketRepository
from .bitbucket_repository_collection import BitbucketRepositoryCollection

class Bitbucket:

    def __init__(self, auth=None, command=None):

        self.api = HttpSession(auth=auth, base_url='https://bitbucket.org/api/2.0')
        self.service_name = 'bitbucket'
        self.command = command.name
        self.options = command.options
        self.hooks = command.hooks
        self.repositories = BitbucketRepositoryCollection(
            options=self.options,
            config={
                'api': self.api
            }
        )
        self.custom = {
            'workspace': self.options.get('repo_workspace')
        }

    def get_repositories(self):
        request_url = 'repositories/{workspace}'.format(
            workspace=self.custom.get('workspace')
        )
        repositories = self.api.get(endpoint=request_url)

        while(repositories.get('next')):        
            for repository in repositories.get('values'):     
                self.repositories[repository.get('name')] = BitbucketRepository(
                    repository=repository,
                    options=self.options,
                    config={
                        'api': self.api
                    }
                )

            
            repositories = self.api.get(endpoint=request_url)

        return self.repositories

    def get_repository(self):
        repo_name = self.options.get('repo_name')
        request_url = 'repositories/{workspace}/{repo_name}'.format(
            workspace=self.custom.get('workspace'),
            repo_name=repo_name
        )
        
        if repo_name in self.repositories.collection:
            return self.repositories[repo_name]

        repository = self.api.get(endpoint=request_url)

        self.repositories[repository.get('name')] = BitbucketRepository(
            repository=repository,
            options=self.options,
            config={
                'api': self.api
            }
        )

        return self.repositories[repo_name]

    def create_repository(self):
        repo_name = self.options.get('repo_name')
        request_url = 'repositories/{workspace}/{repo_name}'.format(
            workspace=self.custom.get('workspace'),
            repo_name=repo_name
        ) 

        repo_config = {
            "name": repo_name,
            "description": self.options.get('repo_description'),
            "is_private": self.options.get('repo_privacy')
        }
        repository = self.api.post(endpoint=request_url, data=repo_config)

        self.repositories[repo_name] = BitbucketRepository(
            repository=repository,
            options=self.options,
            config={
                'api': self.api
            }
        )

        return self.repositories[repo_name]

    def delete_repository(self):
        repo_name = self.options.get('repo_name')
        self.repositories[repo_name].delete()
        self.repositories.delete(repo_name)
        self.api.delete_url(key=repo_name)

        return self
    