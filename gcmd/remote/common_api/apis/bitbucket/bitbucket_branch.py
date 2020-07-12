class BitbucketBranch:

    def __init__(self, branch=None, options=None, api=None, project_key=None, repository_name=None):
        self.branch = branch
        self.options = options
        self.api = api
        self.project_key = project_key
        self.repository_name = repository_name