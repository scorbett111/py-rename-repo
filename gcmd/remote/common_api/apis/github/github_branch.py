import github

class GithubBranch:

    def __init__(self, branch=None, options=None, repository=None):
        self.repository = repository
        self.branch = branch
        self.options = options
        self.name = branch.name
        self.ref = 'refs/head/{branch_name}'.format(branch_name=branch.name)

    def delete_branch(self):
        branch = self.repository.get_git_ref(refs=self.ref)
        branch.delete()
        
        return self
        