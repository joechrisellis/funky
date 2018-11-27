
class LRParser:
    """Class implementing an LR parser."""
    
    def __init__(self, cfg, source):
        self.cfg = self.get_augmented_grammar(cfg)
        self.source = source
        self.stack = []

    def get_augmented_grammar(cfg):
        """For a grammar G with start symbol S, G' is the augmented grammar --
        it is just G with a new start symbol S' and production S' -> S. The
        purpose of this new starting production is to indicate to the parser
        when it should stop parsing and announce acceptance of the input. That
        is, acceptance occurs when and only when the parser is about to reduce
        by S' -> 8.
        """
        new_rules = dict(cfg.rules)
        new_start_symbol = cfg.start_symbol + "'"
        new_rules[new_start_symbol] = [[cfg.start_symbol]]

        augmented = ContextFreeGrammar(new_start_symbol, new_rules)
        return augmented
