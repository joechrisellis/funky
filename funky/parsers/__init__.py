"""Package contains code for the syntax analysis component of the compiler.
Syntax analysis involves taking the tokenized source code and building an
abstract syntax tree (AST) to represent the structure of the program.
"""

from funky import FunkyError

END     = "$"
EPSILON = "epsilon"

test_grammar = {
    "E" : [["T", "E'"]],
    "E'" : [["+", "T", "E'"], [EPSILON]],
    "T" : [["F", "T'"]],
    "T'" : [["*", "F", "T'"], [EPSILON]],
    "F" : [["(", "E", ")"], ["id"]],
}

class ParsingError(FunkyError):
    """Base class for all parsing errors."""
    pass

class InvalidSyntaxException(ParsingError):
    """Raised when the syntax of the program is invalid."""
    pass

class TreeNode:

    def __init__(self, node_type, params=[]):
        self.node_type = node_type
        self.params = params

    def __str__(self):
        children = " ".join(str(x) for x in self.params)
        return "{} {}".format(self.node_type, children)

class ContextFreeGrammar:
    """Class to represent context-free grammars."""
    
    def __init__(self, start_symbol, rules):
        """Initialises the CFG.
        
        Input:
            start_symbol -- the start symbol for the grammar.
            rules        -- a formatted dict representing the productions of
                            the grammar. The dictionary should have
                            NONTERMINALS as keys, mapping to a list of lists
                            for each alternative. I.e. S -> x | yz becomes
                            {"S" : [["x"], ["y", "z"]]}
        """
        self.start_symbol = start_symbol
        self.rules = rules
        self.nonterminals = set(rules.keys())

        # Anything that appears in the body of a production rule that is not
        # a nonterminal.
        self.terminals = set(symbol for alternatives in rules.values()
                                    for alternative  in alternatives
                                    for symbol       in alternative) - \
                         self.nonterminals

    def get_first_sets(self):
        """Returns a dictionary mapping each nonterminal to its first set."""
        return {v : self.first(v) for v in self.nonterminals}
    
    def first(self, symbol):
        """returns the first set of a symbol. if a terminal symbol is given,
        returns a singleton set containing only that symbol. if a nonterminal
        symbol is given, returns its 'first set'.
        
        input:
            symbol -- the symbol for which you want a first set, as a string.

        returns:
            the first set associated with the symbol.
        """
        if symbol not in self.terminals and symbol not in self.nonterminals:
            raise ParsingError("Symbol '{}' not defined for this " \
                               "grammar.".format(symbol))

        # TODO: write unit tests for this function
        first = set()
        if symbol in self.terminals:
            first.add(symbol)
            return first
        
        for alternative in self.rules[symbol]:
            for a in alternative:
                sub_problem = self.first(a)
                first |= sub_problem - set([EPSILON])
                if EPSILON not in sub_problem:
                    break
            else:
                # all epsilon symbols!
                first.add(EPSILON)

        return first

    def get_follow_sets(self):
        """Returns a dictionary mapping each nonterminal to its follow set."""
        return {v : self.follow(v) for v in self.nonterminals}

    def follow(self, symbol):
        """Returns the follow set of a symbol. If a terminal symbol is given,
        returns a singleton set containing only that symbol. If a nonterminal
        symbol is given, returns its 'first set'.
        
        Input:
            symbol -- the symbol for which you want a first set, as a string.

        Returns:
            the first set associated with the symbol.
        """

        if symbol in self.terminals:
            raise ParsingError("Cannot compute follow set for a terminal " \
                               "'{}'.".format(symbol))
        
        follow = set()
        if symbol == self.start_symbol:
            follow.add(END)

        for v, alternatives in self.rules.items():
            for alternative in alternatives:
                if symbol not in alternative or \
                   v == symbol: continue

                i = alternative.index(symbol)
                if i + 1 < len(alternative):
                    f = self.first(alternative[i + 1])
                    follow |= f
                    if EPSILON in f:
                        follow |= self.follow(v)
                else:
                    follow |= self.follow(v)

        return follow - set([EPSILON])
