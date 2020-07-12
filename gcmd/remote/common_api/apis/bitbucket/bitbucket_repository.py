from .bitbucket_branch_collection import BitbucketBranchesCollection

class BitbucketRepository:

    def __init__(self, repository=None, options=None, api=None, project_key=None):
        self.repository = repository
        self.options = options
        self.name = repository.get('name')
        self.id = repository.get('id')
        self.api = api
        self.project_key = project_key
        self.branchs = BitbucketBranchesCollection(
            branches=api.get_branches(
                project_key,
                repository.get('name')
            ),
            options=options,
            api=api,
            project_key=project_key,
            repository_name=repository.get('name')
        )

    def update_repository(self):
        if not self.api.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos'.format(
                projectKey=self.project_key
            )
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos'.format(
                projectKey=self.project_key
            )

    def delete_repository(self):
        self.api.delete_repo(
            self.project_key,
            self.name
        )
