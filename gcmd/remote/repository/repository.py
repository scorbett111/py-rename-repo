from gcmd.remote.repository.github.github_repository import (
    GithubRepository
)

class Repository:
    def __init__(self, repo=None, service_name=None):
        self.service_name = service_name
        self.registered_services = {
            'github': GithubRepository
        }

        self.repository = self.registered_services.get(service_name)(repo=repo)
        self.name = self.repository.name
        self.id = self.repository.id

    def __str__(self):
        return str(self.repository)

    def get_branches(self):
        return self.repository.get_branches()

    def get_branch(self, branch_name=None):
        return self.repository.get_branch(branch_name=branch_name)