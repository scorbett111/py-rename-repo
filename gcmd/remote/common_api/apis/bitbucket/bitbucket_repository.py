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
            'workspace': repository.get('workspace').get('slug'),
        }
        self.api.update_url_store(
            key=self.name,
            endpoint='repositories/{workspace}/{repository}'.format(
                workspace=self.custom.get('workspace'),
                repository=repository.get('slug')
            )
        )
        
        self.branches = BitbucketBranchesCollection(
            options=options,
            config={
                'api': self.api,
                'repo_workspace': self.custom.get('workspace'),
                'repo_name': repository.get('slug')
            }
        )
        self.options = options

        self.default_branch = BitbucketBranch(
            branch=self.api.get(
                key=self.name,
                endpoint=repository.get('mainbranch').get('name')
            ),
            options=self.options,
            config={
                'api': self.api,
                'repo_workspace': self.custom.get('workspace'),
                'repo_name': repository.get('slug')
            }
        )

    def get_branches(self):
        branches = self.api.get(key=self.name, endpoint='refs/branches')

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
            
            branches = self.api.get(key=self.name, endpoint='refs/branches')
        
        return self.branches

    def get_branch(self):
        repo_branch = self.options.get('repo_branch')
        if repo_branch is self.branches.collection:
            return self.branches[repo_branch]

        branch = self.api.get(
            key=self.name,
            endpoint='refs/branches/{branch_name}'.format(branch_name=repo_branch)
        )

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

        self.api.put(key=self.name, data=update_config)
        
        return self

    def delete_repository(self):
        self.api.delete(key=self.name)

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

        self.api.post(key=self.name, endpoint='/pullrequests', data=merge_request)

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

        branch = self.api.post(key=self.name, endpoint='refs/branches', data=branch_config)

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

    def delete_branch(self):
        repo_branch = self.options.get('repo_branch')
        self.branches[repo_branch].delete()
        self.branches.delete(repo_branch)
        self.api.delete_url(key=repo_branch)

        return self
