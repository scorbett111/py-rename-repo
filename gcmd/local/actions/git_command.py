
from gcmd.local.repository import LocalRepository

class GitCommand:

    def __init__(self, command=None):
        self.type = 'command'
        self.command = command.name
        self.options = command.options
        self.hooks = command.hooks
        self.repo = LocalRepository(options=command.options)

    def execute(self, command=None):

        for option in self.options:
            if option.hooks and option.hooks['on_pre']:
                for hook in option.hooks['on_pre']:
                    print(hook.name)
                    # self.repo.execute(command=hook.name)
        
        try:
            self.repo.execute(command=self.command)
        
        except Exception as execution_failure:
            if self.hooks.get('on_failure'):
                for hook in self.hooks.get('on_failure'):
                    self.repo.execute(command=hook.name)
            
            else:
                raise execution_failure

        if self.hooks.get('on_success'):
            for hook in self.hooks.get('on_success'):
                self.repo.execute(command=hook.name)

