from .target import Target
from gcmd.components.utils import (
    transform_configs
)

class TargetGroup:

    def __init__(self, targets=None, config=None, run_setup=True):
        self.targets = {}

        if config.get('targets'):
            if targets:
                config['targets'] = transform_configs(
                    from_config=targets,
                    to_config=config,
                    key='targets'
                ).get('targets')

            for target_name, target_value in config.get('targets').items():
                self.targets[target_value] = Target(map_field=target_name, value=target_value)

    def __iter__(self):
        for target_name in self.targets:
            yield self.targets.get(target_name)

    def __getitem__(self, target):
        return self.targets.get(target)

    def get(self, target, default=None):
        return self.targets.get(target, default)

    def names(self):
        return self.targets.keys()

