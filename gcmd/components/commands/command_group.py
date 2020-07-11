from .command import Command
from gcmd.components.iters import (
    HooksIter
)

class CommandGroup:

    def __init__(self, commands=None):

        self.commands = {}
        self.hooks = HooksIter()

        if commands:
            for command in commands:
                self.commands[command] = Command(config=commands.get(command))

    def __iter__(self):
        for command in self.commands:
            yield self.commands.get(command)

    def __getattr__(self, command_name):
        return self.commands.get(command_name)

    def __setitem__(self, command_name, value):
        self.commands[command_name] = value

    def __getitem__(self, command_name):
        return self.commands.get(command_name)

    def get(self, command_name):
        return self.commands.get(command_name)

    def names(self):
        return self.commands.keys()
