from gcmd.components.options import OptionGroup
from gcmd.components.targets import TargetGroup
from gcmd.components.hooks import Hooks

class Command:
    
    def __init__(self, name=None, config=None, targets=None, options=None, hooks=None):
        self.name = name
        self.targets = TargetGroup(
            targets=targets,
            config=config
        )
        self.options = OptionGroup(
            options=options,
            config=config
        )
        self.hooks = Hooks(
            hooks=hooks,
            config=config.get('hooks')
        )

        for target in self.targets:
            target.hooks = Hooks(
                hooks=hooks,
                config=target.hooks
            )
            self.targets.hooks[target.map] = target.hooks

        for option in self.options:
            option.hooks = Hooks(
                hooks=hooks,
                config=option.hooks
            )
            self.options.hooks[option.map] = option.hooks

    