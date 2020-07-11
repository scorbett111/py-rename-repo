import sys
from gcmd.cli.options_interface import OptionsInterface
from .utils import (
    splice_argv,
    remove_argv
)

class CommandLineInterface:

    def __init__(self, recipies_file=None, registry=None):
        self.registry = registry
        self.action = {
            'commands': []
        }
        self.action_config = None
        self.targets = None
        self.options = None
        self.hooks = None
        self.known_flags = []

    def parse_action(self):
        action_name = sys.argv[1]
        self.action['name'] = action_name
        self.action_config = self.registry.recipies.get(action_name)
        self.targets = self.action_config.get('targets')
        self.options = self.action_config.get('options')
        self.hooks = self.action_config.get('hooks')

        for option in self.options.values():
            if option.get('short_flag'):
                self.known_flags.append(option.get('short_flag'))
            else:
                self.known_flags.append(option.get('long_flag'))

        remove_argv(index=1, remove=1)

        if self.action_config is None:
            raise Exception('Error: Action not registered or found.')

        return self

    def parse_targets(self):
        if self.targets:
            args = list(
                filter(
                    lambda arg: arg not in self.known_flags,
                    splice_argv(index=1, splice=len(self.targets.keys()))
                )
            )

            for index, target in enumerate(self.targets.values()):
                try:
                    target['value'] = args[index]        
                    remove_argv(index=1, remove=len(self.targets.keys()))
                except IndexError:
                    if target.get('default'):
                        target['value'] = target.get('default')
                    else:
                        raise Exception('Error: required target not found.')

        return self

    def parse_options(self):
        if self.options:
            options_interface = OptionsInterface(options=list(self.options.values()))
            options_interface.add_arguments()
            option_values = options_interface.parse_arguments()
            
            for option in option_values:
                option_value = option_values.get(option)
                if option_value is None:
                    option_value = self.options.get(option).get('default')

                self.options[option]['value'] = option_value

        return self
        