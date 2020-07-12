from .github_branch import GithubBranch

class GithubBranchCollection:

    def __init__(self, branches=None, options=None, repository=None):
        self.branches = {}
        self.options = options
        
        for branch in branches:
            self.branches[branch.name] = GithubBranch(
                branch=branch,
                repository=repository
            )

    def __iter__(self):
        for branch in self.branches.values():
            yield branch

    def __getitem__(self, branch):
        return self.branches.get(branch)

    def __setitem__(self, branch_name, branch):
        self.branches[branch_name] = branch