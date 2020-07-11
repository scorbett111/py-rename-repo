from .target import Target
from gcmd.components.iters import (
    HooksIter
)
from gcmd.components.utils import (
    transform_configs
)

class TargetGroup:

    def __init__(self, targets=None, config=None, run_setup=True):
        self.targets = {}
        self.hooks = HooksIter()
        self.target_names = {}

        if config.get('targets'):
            if targets:
                config = transform_configs(
                    from_config=targets,
                    to_config=config,
                    key='targets'
                )

                for target_name, target_config in targets.items():
                    self.target_names[target_config.get('map')] = target_name

            for map_field, target_config in config.get('targets').items():
                self.targets[map_field] = Target(
                    name=self.target_names.get(map_field) or map_field,
                    map_field=target_name,
                    value=target_config.get('value'),
                    hooks=target_config.get('hooks')
                )

    def __iter__(self):
        for target_name in self.targets:
            yield self.targets.get(target_name)

    def __getitem__(self, target):
        return self.targets.get(target)

    def get(self, target, default=None):
        return self.targets.get(target, default)

    def names(self):
        return self.targets.keys()

