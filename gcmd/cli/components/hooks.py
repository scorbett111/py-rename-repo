from .event import Event

class Hooks:

    def __init__(self, hooks=None, config=None):

        self.hooks = {}

        if config:
            for event in config:
                self.hooks[event] = Event(
                    event=event,
                    hooks=hooks,
                    config=config.get(event)
                )

    def __getitem__(self, event):
        return self.hooks.get(event)

    def __iter__(self):
        for event in self.hooks:
            yield self.hooks.get(event)
    