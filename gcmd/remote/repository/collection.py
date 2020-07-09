import collections
from gcmd.remote.repository.github.github_collection import (
    GithubCollection
)

class Collection:
    def __init__(self, repositories=None, service_name=None):
        self.service_name = service_name
        self.collection = []
        self.registered_services = {
            'github': GithubCollection
        }

        if isinstance(repositories, collections.abc.Iterable):
            try:
                self.collection = self.registered_services.get(service_name)(
                    repositories=repositories,
                    service_name=service_name
                )
            except Exception as e:
                print(str(e))         
        else:
            raise Exception("Error: Repository list from service is required")
        self.size = self.collection.size

    def __iter__(self):
        return self.collection.__iter__()