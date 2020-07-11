class HooksIter:

    def __init__(self, items=None):

        self.hooks = {}

        if items:
            for item in items:
                self.hooks[item] = item.hooks

    def __iter__(self):
        for hooks in self.hooks.values():
            for event in hooks:
                for hook in event:
                    yield hook

    def __getitem__(self, *args):
        results = self.hooks
        for arg in args:
            if results.get(arg):
                results = results.get(arg)
            else:
                results = None
        return results

    def __setitem__(self, item, hooks):
        self.hooks[item] = hooks

    def get(self, item):
        return self.hooks.get(item)
