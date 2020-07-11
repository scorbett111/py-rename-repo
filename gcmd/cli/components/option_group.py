from .option import Option
from .utils import (
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

            for option_name, option_value in config.get('options').items():
                self.options[option_name] = Option(map_field=option_name,value=option_value)

    def __iter__(self):
        for option_name in self.options:
            yield self.options.get(option_name)

    def __getitem__(self, option):
        return self.options.get(option).value

    def get(self, option, default=None):
        result = self.options.get(option)
        if result:
            return result.value

        return default

    def items(self):
        return self.options.values()

    def names(self):
        return self.options.keys()