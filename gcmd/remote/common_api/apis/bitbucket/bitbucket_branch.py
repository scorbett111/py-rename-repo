class BitbucketBranch:

    def __init__(self, branch=None, options=None, config=None):
        self.name = branch.get('name')
        self.api = config.get('api')
        self.api.update_url_store(
            key=self.name,
            base=config.get('repo_name'),
            endpoint='refs/branches/{branch_name}'.format(branch_name=self.name)
        )

        self.options = options
        self.custom = {
            'hash': branch.get('target').get('hash'),
            'repo_workspace': config.get('repo_workspace'),
            'repo_name': config.get('repo_name')
        }

    def delete_branch(self):
        self.api.delete(key=self.name)

        return self