import urllib
import json
from .bitbucket_branch import BitbucketBranch
from .bitbucket_branch_collection import BitbucketBranchesCollection

class BitbucketRepository:

    def __init__(self, repository=None, options=None, config=None):
        self.api = config.get('api')
        self.name = repository.get('name')
        self.description = repository.get('description')
        self.private = repository.get('is_private')
        self.url = repository.get('self').get('href')
        self.ssh_url = next(
            url.get('href') for url in repository.get(
                'clone'
            ) if url.get('name') == 'ssh'
        )
        self.custom = {
            'slug': repository.get('slug'),
            'base_url': urllib.parse.urljoin(
                'https://bitbucket.org/api/2.0',
                'repositories/{workspace}/{repository}'.format(
                    workspace=self.custom.get('workspace'),
                    repository=repository.get('slug')
                )    
            ),
            'workspace': repository.get('workspace').get('slug'),
        }

        self.branches = BitbucketBranchesCollection(
            options=options,
            config={
                'api': self.api,
                'repo_workspace': self.custom.get('workspace'),
                'repo_name': repository.get('slug')
            }
        )
        self.options = options

        default_branch = self.api.get(
            urllib.parse.urljoin(
                self.custom.get('base_url'),
                repository.get('mainbranch').get('name')
            )
        ).json()

        self.default_branch = BitbucketBranch(
            branch=default_branch,
            options=self.options,
            config={
                'api': self.api,
                'repo_workspace': self.custom.get('workspace'),
                'repo_name': repository.get('slug')
            }
        )

    def get_branches(self):
        request_url = urllib.parse.urljoin(
            self.custom.get('base_url'),
            'refs/branches'
        )
        branches = self.api.get(request_url).json()

        while(branches.get('next')):
            for branch in branches.get('values'):
                self.branches[branch.get('name')] = BitbucketBranch(
                    branch=branch,
                    options=self.options,
                    config={
                        'api': self.api,
                        'repo_workspace': self.custom.get('workspace'),
                        'repo_name': self.custom.get('slug')
                    }
                )
            
            branches = self.api.get(request_url).json()
        
        return self.branches

    def get_branch(self):
        repo_branch = self.options.get('repo_branch')
        request_url = urllib.parse.urljoin(
            self.custom.get('base_url'),
            'refs/branches/{branch_name}'.format(branch_name=branch_name)
        )
        if repo_branch is self.branches.collection:
            return self.branches[repo_branch]

        branch = self.api.get(request_url).json()

        self.branches[repo_branch] = BitbucketBranch(
            branch=branch,
            options=self.options,
            config={
                'api': self.api,
                'repo_workspace': self.custom.get('workspace'),
                'repo_name': self.custom.get('slug')
            }
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

        self.private = self.options.get('private', self.private)
        if self.private:
            update_config['is_private'] = self.private

        self.default_branch = self.options.get('repo_branch', self.default_branch)
        if self.default_branch:
            update_config['mainbranch'] = {
                'type': 'branch',
                'name': self.default_branch
            }

        self.api.put(
            self.custom.get('base_url'),
            data=json.dumps(update_config)
        )
        
        return self

    def delete_repository(self):
        self.api.delete(self.custom.get('base_url'))

        return self

    def create_merge_request(self):
        merge_request = {
            'title': self.options.get('merge_request_title'),
            'description': self.options.get('merge_request_message'),
            'source': {
                'branch': {
                    'name': self.options.get('from_branch')
                }
            },
            'destination': {
                'branch': {
                    'name': self.options.get('to_branch', 'main')
                }
            }
        }

        self.api.post(
            '{base_url}/pullrequests'.format(
                base_url=self.custom.get('base_url')
            ),
            data=json.dumps(merge_request)
        )

        return self

    def create_branch(self):
        repo_branch = self.options.get('repo_branch')
        branch_config = {
            'name': self.options.get('repo_branch'),
            'target': {
                'hash': self.options.get(
                    'from_branch',
                    self.default_branch.branch.commit.sha
                )
            }
        }

        branch = self.api.post(
            urllib.parse.urljoin(
                self.custom.get('base_url'),
                'refs/branches'
            ),
            data=json.dumps(branch_config)
        ).json()

        self.branches[repo_branch] = BitbucketBranch(
            branch=branch,
            options=self.options,
            config={
                'api': self.api,
                'repo_workspace': self.custom.get('workspace'),
                'repo_name': self.custom.get('slug')
            }
        )

        return self.branches[repo_branch]
