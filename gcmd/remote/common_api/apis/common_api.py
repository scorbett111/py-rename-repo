from gcmd.remote.services.github import (
    GithubAPI
)
from gcmd.remote.repository import (
    Collection,
    Repository
)

class CommonAPI:
    def __init__(self, service_name=None):
        
        if service_name is None:
            raise Exception('Error: Service name is required.')
        
        self.service_name = service_name
        self.registered_services = {
            'github': GithubService
        }
        self.service = None
        self.repositories = None
        self.selected_repository = None

    def login(self, auth=None):
        self.registered_services.get(self.service_name)(
            auth=auth
        )

        return self

    def get_repositories(self):
        if self.service is None:
            raise Exception(
                'Error: Service under name {service_name} not found or registered for Service object'.format(
                    service_name=self.service_name
                )
            )

        self.repositories = Collection(
            repositories=self.service.get_repositories(),
            service_name=self.service_name
        )

        return self.repositories

    def get_repository(self, repository_name=None):
        if self.repositories:
            return next(
                repo for repo in self.repositories if repo.name == repository_name
            )

        return Repository(
            repo=self.service.get_repo(repository_name),
            service_name=self.service_name
        )
