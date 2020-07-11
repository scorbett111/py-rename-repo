import collections
from .option import Option
from .utils import (
    transform_configs
)

class OptionGroup(collections.Mapping):

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

    def __dict__(self):
        options_dict = {}
        for option_name, option_value in self.options:
            options_dict[option_name] = options_dict[option_value]

        return options_dict

    def __iter__(self):
        for option_name in self.options:
            yield option_name

    def __getitem__(self, option):
        return self.options.get(option).value

    def get(self, option, default=None):
        result = self.options.get(option)
        if result is None:
            return default

        return result.value

    def __len__(self):
        return len(self.options)

    def items(self):
        return self.options.values()

    def names(self):
        return self.options.keys()