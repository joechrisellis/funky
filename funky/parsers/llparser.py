from funky.parsers import ParsingError, InvalidSyntaxError, \
                          AbstractSyntaxTree, EPSILON, END

class LLParser: 
    """An LL(1) parser."""

    INVALID_SYNTAX = "Invalid syntax in source. '{}' was the offending " \
                     "character.".format

    def __init__(self, cfg):
        self.cfg = cfg
        self.parse_table = self.create_parse_table()

    def parse(self, source):
        """Parses the given string according to the context-free grammar.
        
        Input:
            source -- the string to parse

        Returns:
            an abstract syntax tree representing the parse
        """
        i, stack = 0, [END, self.cfg.start_symbol]
        root = AbstractSyntaxTree(self.cfg.start_symbol)
        tree_stack = [root]

        x = stack[-1]
        while x != END:
            a = source[i]
            if x == a:
                stack.pop()
                t = tree_stack.pop()
                t.value = a
                i += 1
            elif x in self.cfg.terminals:
                print("x in terminals", x, i, a)
                raise ParsingError(LLParser.INVALID_SYNTAX(a))
            else:
                v = self.parse_table[x].get(a,
                                            self.parse_table[x].get(a.strip_value(),
                                                                    None))
                if v:
                    rule = v[0]
                    stack.pop()
                    t = tree_stack.pop()

                    children = [AbstractSyntaxTree(x) for x in rule]

                    if rule != [EPSILON]:
                        t.children = children
                        tree_stack.extend(children[::-1])
                        stack.extend(rule[::-1])
                else:
                    raise InvalidSyntaxError(LLParser.INVALID_SYNTAX(a))
                
            x = stack[-1]

        return root
            
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
