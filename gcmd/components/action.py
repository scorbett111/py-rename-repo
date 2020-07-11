from gcmd.components.commands import (
    CommandGroup,
    Command
)
from gcmd.components.utils import (
    transform_configs
)

class Action:

    def __init__(self, cli=None):
        self.config = cli.action_config
        self.cli = cli
        self.name = self.config.get('name')
        self.commands = CommandGroup()

        if self.cli.hooks:
            for hook in self.cli.hooks.values():
                hook = transform_configs(
                    from_config=self.cli.options,
                    to_config=hook,
                    key='options'
                )

    def setup(self):
        for command_name in self.config.get('recipe'):
            command = Command(
                name=command_name,
                config=self.config.get('commands').get(command_name),
                targets=self.cli.targets,
                options=self.cli.options,
                hooks=self.cli.hooks
            )
            self.commands[command_name] = command
            self.commands.hooks[command_name] = command.hooks
            
            


