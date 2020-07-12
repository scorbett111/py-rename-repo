from .github_branch_collection import GithubBranchCollection
from .github_branch import GithubBranch

class GithubRepository:

    def __init__(self, repository=None, options=None):
        branches = GithubBranchCollection(
            branches=repository.get_branches(),
            options=options,
            repository=repository
        )

        self.repository = repository
        self.branches = branches
        self.id = repository.id
        self.name = repository.name
        self.description = repository.description
        self.private = repository.private
        self.default_branch = branches[repository.default_branch]
        self.url = repository.clone_url
        self.ssh_url = repository.ssh_url

        self.options = options

    def update_repository(self):
        update_config = {}
        self.name = self.options.get('repo_name', self.name)
        if self.name:
            update_config['name'] = self.name

        self.description = self.options.get('repo_description', self.description)
        if self.description:
            update_config['description'] = self.description

        self.private = self.options.get('repo_privacy', self.private)
        if self.private:
            update_config['private'] = self.private

        self.default_branch = self.branches[self.options.get('repo_branch', self.default_branch)]
        if self.default_branch:
            update_config['default_branch'] = self.default_branch

        self.repository.edit(**self.options)

        return self

    def delete_repository(self):
        self.repository.delete()
        return self

    def create_merge_request(self):
        title = self.options.get('merge_request_title')
        message = self.options.get('merge_request_message')
        from_branch = self.options.get('from_branch')
        to_branch = self.options.get('to_branch', 'main')
        self.repository.create_pull(
            title=title,
            body=message,
            head=from_branch,
            base=to_branch
        )

        return self

    def create_branch(self):
        repo_branch = self.options.get('repo_branch')
        default_branch_head = self.default_branch.branch.commit.sha

        branch_ref = 'refs/heads/{repo_branch}'.format(
            repo_branch=repo_branch
        )

        self.repository.create_git_ref(
            refs=branch_ref,
            sha=default_branch_head
        )

        return self
        