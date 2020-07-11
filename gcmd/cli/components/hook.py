from .option_group import OptionGroup
from .target_group import TargetGroup

class Hook:
    
    def __init__(self, name=None, config=None):
        self.name = name
        self.targets = TargetGroup(config=config)
        self.options = OptionGroup(config=config)
    