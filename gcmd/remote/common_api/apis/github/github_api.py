import github
from .github_repository import GithubRepository
from .github_repository_collection import GithubRepositoryCollection

class Github:

    def __init__(self, auth=None, command=None):

        if auth.type == 'token':
            self.api = github.Github(auth.token)
        
        else:
            self.api = github.Github(
                auth.user,
                auth.password
            )

        self.service_name = 'github'
        self.command = command.name
        self.options = command.options
        self.hooks = command.hooks
        self.repositories = GithubRepositoryCollection(
            options=self.options
        )
        self.custom = {
            'user': self.api.get_user()
        }

    def __iter__(self):
        for repo in self.repositories:
            yield repo

    def __getitem__(self, repository_name):
        return self.repositories[repository_name]

    def get_repositories(self):
        repositories = self.custom.get('user').get_repos()
        
        for repository in repositories:
            self.repositories[repository.name] = GithubRepository(
                repository=repository,
                options=self.options
            )

        return self.repositories

    def get_repository(self):
        repo_name = self.options.get('repo_name')
        if repo_name in self.repositories.collection:
            return self.repositories[repo_name]

        repository = self.custom.get('user').get_repo()
        self.repositories[repo_name] = GithubRepository(
            repository=repository,
            options=self.options
        )

        return self.repositories[repo_name]

    def create_repository(self):
        repo_name = self.options.get('repo_name')
        repo_description = self.options.get('repo_description')
        self.repository = self.custom.get('user').create_repo(
            name=repo_name,
            description=repo_description
        )

        if self.options.get('with_readme'):
            repository = self.repository.create_file(
                "README.md",
                "Init commit with README.md",
                ""
            )

            self.repositories[repository.name] = GithubRepository(
                repository=repository,
                options=self.options
            )

        return self.repositories[repo_name]

    def delete_repository(self):
        repo_name = self.options.get('repo_name')
        self.repositories[repo_name].delete()
        self.repositories.delete(repo_name)

        return self