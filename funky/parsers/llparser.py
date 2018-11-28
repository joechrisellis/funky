from funky.parsers import ParsingError, EPSILON, END

class LLParser: 

    def __init__(self, cfg):
        self.cfg = cfg
        self.parse_table = self.create_parse_table()

    def parse(self, source):
        import time
        i, stack = 0, [END, self.cfg.start_symbol]

        x = stack[-1]
        while x != END:
            print("INPUT", source[i:])
            print("STACK", stack)
            print("",)
            a = source[i]
            if x == a:
                stack.pop()
                i += 1
            elif x in self.cfg.terminals:
                raise ParsingError("Error while parsing: '{}' is a " \
                                   "terminal.".format(x))
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
                    from pprint import pprint
                    pprint(self.parse_table)
                
            x = stack[-1]
            time.sleep(1)
            
    def create_parse_table(self):
        """Returns the parse table for the grammar. Parse table takes the form
        of a nested dictionary such that table[nonterminal][terminal] gives the
        production.
        """
        table = {v : {terminal : [] for terminal in self.cfg.terminals | set([END]) if terminal != EPSILON}
                 for v in self.cfg.nonterminals}

        for v, alternatives in self.cfg.rules.items():
            for alternative in alternatives:
                self.cfg.rules[v] = [alternative]

                for terminal in self.cfg.first(v):
                    if terminal == EPSILON: continue
                    table[v][terminal].append(alternative)

                if EPSILON in self.cfg.first(alternative[0]):
                    for terminal in self.cfg.follow(v):
                        table[v][terminal].append(alternative)
                
                self.cfg.rules[v] = alternatives

        return table
