from .option_group import OptionGroup
from .target_group import TargetGroup
from .hooks import Hooks

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

    