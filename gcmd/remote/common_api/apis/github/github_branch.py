import github

class GithubBranch:

    def __init__(self, branch=None, options=None, repository=None):
        self.api = repository
        self.options = options
        self.name = branch.name
        self.custom = {
            'ref': 'refs/head/{branch_name}'.format(branch_name=branch.name)
        }

    def delete_branch(self):
        branch = self.api.get_branch(self.name)
        branch.delete()
        
        return self
        