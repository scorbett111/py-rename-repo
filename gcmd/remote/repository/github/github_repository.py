class GithubRepository:
    def __init__(self, repo=None):
        self.repo = repo
        self.name = repo.name
        self.id = repo.id

    def __str__(self):
        return self.name

    def get_branches(self):
        return self.repo.get_branches()

    def get_branch(self, branch_name=None):
        return self.repo.get_branch(branch=branch_name)

    def create_merge_request(self, config=None):
        return self.repo.create_pull(
            title=config.get('title'),
            body=config.get('message'),
            head=config.get('from_branch'),
            base=config.get('to_branch')
        )