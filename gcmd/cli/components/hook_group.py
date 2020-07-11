from .hook import Hook

class HookGroup:

    def __init__(self, hooks=None, config=None):
        self.hooks = {}

        for hook in config:
            self.hooks[hook] = Hook(config=hooks.get(hook))

    def __iter__(self):
        for hook_name in self.hooks:
            yield self.hooks.get(hook_name)

    def __getitem__(self, hook):
        return self.hooks.get(hook)

    def get(self, hook, default=None):
        return self.hooks.get(hook, default)

    def items(self):
        return self.hooks.values()

    def names(self):
        return self.hooks.keys()

        