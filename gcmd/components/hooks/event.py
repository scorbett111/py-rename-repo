from .hook_group import HookGroup

class Event(HookGroup):

    def __init__(self, event=None, hooks=None, config=None):
        self.type = event
        super().__init__(hooks=hooks, config=config)
