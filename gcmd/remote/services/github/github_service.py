import github


class GithubService:

    def __init__(self, auth=None):

        if auth.type == 'token':
            self.service = github.Github(auth.token)
        
        else:
            self.service = github.Github(
                auth.user,
                auth.password
            )

        self.service_name = 'github'

    def get_repositories(self):
        return self.service.get_user().get_repos()
            
            
        


        