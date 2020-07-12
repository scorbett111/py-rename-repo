from .bitbucket_branch import BitbucketBranch

class BitbucketBranchesCollection:

    def __init__(self, branches=None, options=None, api=None, project_key=None, repository_name=None):
        self.branches = {}
        self.options = options

        for branch in branches:
            branch[branch.get('name')] = BitbucketBranch(
                branch=branch,
                options=options,
                api=api,
                project_key=project_key,
                repository_name=repository_name
            )