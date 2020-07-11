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
            if target.hooks:
                target.hooks = Hooks(
                    hooks=hooks,
                    config=target.hooks
                )

        for option in self.options:
            if option.hooks:
                option.hooks = Hooks(
                    hooks=hooks,
                    config=option.hooks
                )

    