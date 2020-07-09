import github
from gcmd.remote.repository.repository import (
    Repository
)

class GithubCollection:

    def __init__(self, repositories=None, service_name=None):
        github_collection = []
        for github_repository in repositories:
            github_collection.append(
                Repository(
                    repo=github_repository,
                    service_name=service_name
                )
            )

        self.collection = github_collection
        self.size = len(github_collection)

    def __iter__(self):
        for repository in self.collection:
            yield repository

