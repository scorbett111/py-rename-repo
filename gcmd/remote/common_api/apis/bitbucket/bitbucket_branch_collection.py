from .bitbucket_branch import BitbucketBranch

class BitbucketBranchesCollection:

    def __init__(self, branches=None, options=None, config=None):
        self.collection = {}
        self.options = options
        self.config = config

        if branches:
            for branch in branches:
                branch[branch.get('name')] = BitbucketBranch(
                    branch=branch,
                    options=options,
                    config=config
                )

    def __iter__(self):
        for branch in self.collection:
            yield branch

    def __getitem__(self, branch_name):
        return self.collection.get(branch_name)

    def __setitem__(self, branch_name, branch):
        self.collection[branch_name] = branch

    def delete(self, branch_name):
        if self.collection.get(branch_name):
            del self.collection[branch_name]