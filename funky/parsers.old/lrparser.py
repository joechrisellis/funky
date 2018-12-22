from copy import deepcopy

class Item:
    """LR(0) item."""

    def __init__(self, rule, dot):
        self.rule = rule
        self.dot = dot

    def __hash__(self):
        return hash((self.rule, self.dot))

class LRParser:
    """Class implementing an LR parser."""
    
    def __init__(self, cfg, source):
        self.cfg = cfg.get_augmented()

    def closure(self, I):
        pass

    def goto(self):
        pass

    def make_automaton(self):
        item_sets = []
        item_sets.append([])
