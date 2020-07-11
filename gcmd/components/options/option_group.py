from .option import Option
from gcmd.components.iters import (
    HooksIter
)
from gcmd.components.utils import (
    transform_configs
)

class OptionGroup:

    def __init__(self, options=None, config=None):
        self.options = {}
        self.option_names = {}
        self.hooks = HooksIter()

        if config.get('options'):
            if options:
                config = transform_configs(
                    from_config=options,
                    to_config=config,
                    key='options'
                )

                for option_name, option_config in options.items():
                    self.option_names[option_config.get('map')] = option_name

            for map_field, option_config in config.get('options').items():
                self.options[map_field] = Option(
                    name=self.option_names.get(map_field) or map_field,
                    map_field=map_field,
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