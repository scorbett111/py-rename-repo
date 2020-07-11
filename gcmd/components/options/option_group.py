from .option import Option
from gcmd.components.utils import (
    transform_configs
)

class OptionGroup:

    def __init__(self, options=None, config=None):
        self.options = {}

        if config.get('options'):
            if options:
                config = transform_configs(
                    from_config=options,
                    to_config=config,
                    key='options'
                )

            for option_name, option_config in config.get('options').items():
                self.options[option_name] = Option(
                    map_field=option_name,
                    value=option_config.get('value'),
                    hooks=option_config.get('hooks')
                )

    def __iter__(self):
        for option_name in self.options:
            yield self.options.get(option_name)

    def __getitem__(self, option):
        return self.options.get(option).value

    def get(self, option, default=None):
        result = self.options.get(option)
        if result is None:
            return default

        return result.value

    def items(self):
        return self.options.values()

    def names(self):
        return self.options.keys()