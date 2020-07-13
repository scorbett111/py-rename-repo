import urllib

class BitbucketBranch:

    def __init__(self, branch=None, options=None, config=None):
        self.options = options
        self.api = config.get('api')
        self.name = branch.get('name')
        self.custom = {
            'hash': branch.get('target').get('hash'),
            'repo_workspace': config.get('repo_workspace'),
            'repo_name': config.get('repo_name'),
            'base_url': urllib.parse.urljoin(
                'https://bitbucket.org/api/2.0',
                'repositories/{workspace}/{repository}/refs/branches/{branch_name}'.format(
                    workspace=config.get('repo_workspace'),
                    repository=config.get('repo_name'),
                    branch_name=self.name
                )
            )
        }

    def delete_branch(self):
        self.api.delete(self.custom.get('base_url'))

        return self