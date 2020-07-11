
from gcmd.local.repository import LocalRepository

class GitCommand:

    def __init__(self, command=None, options=None):
        self.type = 'command'
        self.command = command
        self.options = options
        self.repo = LocalRepository(options=options)

    def execute(self, command=None):
        return self.repo.execute(command=self.command)