import collections

class Option:

    def __init__(self, map_field=None, value=None):
        self.map = map_field
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __lt__(self, other):
        return self.value < other

    def __ge__(self, other):
        return self.value >= other

    def __le__(self, other):
        return self.value <= other

    def __len__(self):
        if hasattr(self.value, '__len__'):
            return len(self.value)
        return 0

    def __dict__(self):
        return {self.map: self.value}