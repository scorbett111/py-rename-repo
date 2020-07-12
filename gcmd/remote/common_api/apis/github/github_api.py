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
        self.user = self.api.get_user()
        self.repositories = GithubRepositoryCollection()

    def __iter__(self):
        for repo in self.user.get_repos():
            yield repo

    def __getitem__(self, repository_name):
        return self.repositories[repository_name]

    def create_repository(self):
        repo_name = self.options.get('repo_name')
        repo_description = self.options.get('repo_description')
        self.repository = self.user.create_repo(
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

        return self
        
