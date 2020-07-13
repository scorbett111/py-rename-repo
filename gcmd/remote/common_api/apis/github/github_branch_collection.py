from .github_branch import GithubBranch

class GithubBranchCollection:

    def __init__(self, branches=None, options=None, repository=None):
        self.collection = {}
        self.options = options

        if branches: 
            for branch in branches:
                self.collection[branch.name] = GithubBranch(
                    branch=branch,
                    repository=repository
                )

    def __iter__(self):
        for branch in self.collection.values():
            yield branch

    def __getitem__(self, branch):
        return self.collection.get(branch)

    def __setitem__(self, branch_name, branch):
        self.collection[branch_name] = branch

    def delete(self, branch_name):
        if self.collection.get(branch_name):
            del self.collection[branch_name]