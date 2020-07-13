from .github_branch_collection import GithubBranchCollection
from .github_branch import GithubBranch

class GithubRepository:

    def __init__(self, repository=None, options=None):
        self.api = repository
        self.branches = GithubBranchCollection(
            options=options,
            repository=repository
        )
        self.id = repository.id
        self.name = repository.name
        self.description = repository.description
        self.private = repository.private
        self.branches = GithubBranchCollection(
            options=options,
            repository=self.api
        )
        self.default_branch = GithubBranch(
            branch=self.api.get_branch(
                branch=repository.default_branch
            ),
            options=options,
            repository=repository
        )
        self.url = repository.clone_url
        self.ssh_url = repository.ssh_url

        self.options = options

    def get_branches(self):
        branches = self.api.get_branches()
        for branch in branches:
            self.branches[branch.name] = GithubBranch(
                branch=branch,
                options=self.options,
                repository=self.api
            )

        return self

    def get_branch(self):
        repo_branch = self.options.get('repo_branch')
        if repo_branch in self.branches.collection:
            return self.branches[repo_branch]

        branch = self.api.get_branch(repo_branch)
        self.branches[repo_branch] = GithubBranch(
            branch=branch,
            options=self.options,
            repository=self.api
        )

        return self.branches[repo_branch]

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

        self.api.edit(**self.options)

        return self

    def delete_repository(self):
        self.api.delete()
        return self

    def create_merge_request(self):
        title = self.options.get('merge_request_title')
        message = self.options.get('merge_request_message')
        from_branch = self.options.get('from_branch')
        to_branch = self.options.get('to_branch', 'main')
        self.api.create_pull(
            title=title,
            body=message,
            head=from_branch,
            base=to_branch
        )

        return self

    def create_branch(self):
        repo_branch = self.options.get('repo_branch')
        branch_head = self.options.get(
            'from_branch',
            self.default_branch.branch.commit.sha
        )

        branch_ref = 'refs/heads/{repo_branch}'.format(
            repo_branch=repo_branch
        )

        self.api.create_git_ref(
            refs=branch_ref,
            sha=branch_head
        )

        branch = self.api.get_branch(repo_branch)
        self.branches[repo_branch] = GithubBranch(
            branch=branch,
            options=self.options,
            repository=self.api
        )

        return self.branches[repo_branch]

    def delete_branch(self):
        repo_branch = self.options.get('repo_branch')
        self.branches[repo_branch].delete()
        self.branches.delete(repo_branch)
        
        return self