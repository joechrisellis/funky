from . import EPSILON, END

class LLParserGenerator:
    """Class implementing an LL predictive parser."""
    
    def __init__(self, cfg):
        self.cfg = cfg
    
    def get_parse_table(self):
        """Returns the parse table for the grammar. Parse table takes the form
        of a nested dictionary such that table[nonterminal][terminal] gives the
        production.
        """
        table = {v : {terminal : [] for terminal in self.cfg.terminals | set([END]) if terminal != EPSILON}
                 for v in self.cfg.nonterminals}

        for v, alternatives in self.cfg.rules.items():
            for alternative in alternatives:
                for terminal in self.cfg.first(v):
                    if terminal == EPSILON: continue
                    table[v][terminal].append(alternative)

                if EPSILON in self.cfg.first(alternative[0]):
                    for terminal in self.cfg.follow(v):
                        table[v][terminal].append(alternative)
        from pprint import pprint
        pprint(table)
