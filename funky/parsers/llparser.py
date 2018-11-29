from funky.parsers import ParsingError, InvalidSyntaxError, EPSILON, END

class LLParser: 

    INVALID_SYNTAX = "Invalid syntax in source. '{}' was the offending " \
                     "character.".format

    def __init__(self, cfg):
        self.cfg = cfg
        self.parse_table = self.create_parse_table()

    def parse(self, source):
        i, stack = 0, [END, self.cfg.start_symbol]

        x = stack[-1]
        while x != END:
            a = source[i]
            if x == a:
                stack.pop()
                i += 1
            elif x in self.cfg.terminals:
                raise ParsingError(LLParser.INVALID_SYNTAX(a))
            else:
                v = self.parse_table[x].get(a,
                                            self.parse_table[x].get(a.strip_value(),
                                                                    None))
                if v:
                    rule = v[0]
                    stack.pop()
                    if rule != [EPSILON]:
                        stack.extend(rule[::-1])
                else:
                    # TODO: better error mesage here.
                    raise InvalidSyntaxError(LLParser.INVALID_SYNTAX(a))
                
            x = stack[-1]
            
    def create_parse_table(self):
        """Returns the parse table for the grammar. Parse table takes the form
        of a nested dictionary such that table[nonterminal][terminal] gives the
        production. Algorithm adapted from Dragon Book, Aho et al. For each
        production A -> a of the grammar, do the following:

            1. For each terminal t in FIRST(a), add A -> a to M[A, t].
            2. If epsilon is in FIRST(a), then for each terminal b in FOLLOW(A),
               add A -> a to M[A, b]. If epsilon is in FIRST(a) and the end
               marker is in FOLLOW(A), add A -> a to M[A, end_marker] as well.
        """
        table = {v : {terminal : [] for terminal in self.cfg.terminals | set([END]) if terminal != EPSILON}
                 for v in self.cfg.nonterminals}
        
        for v, alternatives in self.cfg.rules.items():
            for alternative in alternatives:
                first_set = self.cfg.first_of(alternative)
                for terminal in first_set:
                    if terminal == EPSILON: continue # dont add epsilons
                    table[v][terminal].append(alternative)

                if EPSILON in first_set:
                    for terminal in self.cfg.follow[v]: 
                        table[v][terminal].append(alternative)

        return table
