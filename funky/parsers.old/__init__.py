"""Package contains code for the syntax analysis component of the compiler.
Syntax analysis involves taking the tokenized source code and building an
abstract syntax tree (AST) to represent the structure of the program.
"""
from copy import deepcopy

from funky import FunkyError
from funky import lexer as lexer

END     = lexer.Token(lexer.TokenType.END)
EPSILON = "epsilon"

class ParsingError(FunkyError):
    """Base class for all parsing errors."""
    pass

class InvalidSyntaxError(ParsingError):
    """Raised when the syntax of the program is invalid."""
    pass

class AbstractSyntaxTree:

    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def __repr__(self):
        s = str(self.value)
        for child in self.children:
            s += " [{}]".format(repr(child))
        return s

    def __str__(self):
        return self.__repr__()

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
        
        self.first = {}
        self.follow = {}
        self._compute_first_sets()
        self._compute_follow_sets()

    def first_of(self, symbols):
        """Computes the first set of a string of symbols X1X2...Xn.
        Algorithm adapted from Dragon Book, Aho et al. To compute FIRST for any
        string X1X2...Xn:

            1. Add to FIRST all non-epsilon symbols of FIRST(X1).
            2. Also add the non-epsilon symbols of FIRST(X2), if epsilon is in
               FIRST(X1); the non-epsilon symbols of FIRST(X3), if epsilon is in
               FIRST(X1) and FIRST(X2), and so on.
            3. Finally, add epsilon to FIRST(X1X2...Xn) if, for all i, epsilon
               is in FIRST(Xi).
        
        Input:
            symbols -- a string of symbols, i.e. ["S", "A", "B"]

        Returns:
            the first set for that string of symbols.
        """
        first = set()
        for symbol in symbols:
            first |= self.first[symbol] - set([EPSILON])
            if EPSILON not in self.first[symbol]:
                break
        else:
            first.add(EPSILON)
        return first

    def _compute_first_sets(self):
        """Computes the first set for all of the symbols in the grammar.
        Algorithm adapted from Dragon Book, Aho et al. To compute FIRST(X) for
        all grammar symbols X, apply the following rules until no more
        terminals or epsilon can be added to any FIRST set.

            1. If X is a terminal, first(X) = { X }
            2. If X is a nonterminal and X -> Y1Y2...Yk is a production for
               some k >= 1, then a is a member of FIRST(X) if, for some i, a is
               in FIRST(Yi), and epsilon is in all of FIRST(Y1), ..., FIRST(Yi-1).
            3. If X -> epsilon is a produciton, then add epsilon to FIRST(X).
        """
        for t in self.terminals:
            self.first[t] = set([t])
        for v in self.nonterminals:
            self.first[v] = set()

        break_next = False
        i = 0
        while True:
            buf = deepcopy(self.first) # TODO: definitely inefficient, fix
            for X in self.nonterminals:
                for alternatives in [s for v, s in self.rules.items() if v == X]:
                    for alternative in alternatives:
                        add_epsilon = True
                        for symbol in alternative:
                            self.first[X] |= self.first[symbol] - set([EPSILON])
                            if EPSILON not in self.first[symbol]:
                                add_epsilon = False
                                break

                        if add_epsilon:
                            self.first[X] |= set([EPSILON])

            if break_next and buf == self.first:
                break
            break_next = buf == self.first

    def _compute_follow_sets(self):
        """Computes the follow set for all of the symbols in the grammar.
        Algorithm adapted from Dragon Book, Aho et al. To compute FOLLOW(A) for
        all nonterminals A, apply the following rules until nothing can be
        added to any follow set:
        
        1. Place the end marker in FOLLOW(S), where S is the start symbol.
        2. If there is a production A -> xBz, then everything in FIRST(Z) except
           epsilon is in FOLLOW(B).
        3. If there is a production A -> xB, or a production A -> xBz, where
           FIRST(z) contains epsilon, then everything in FOLLOW(A) is in
           FOLLOW(B).
        """
        for v in self.nonterminals:
            self.follow[v] = set()
        self.follow[self.start_symbol].add(END)

        break_next = False
        while True:
            buf = deepcopy(self.follow)
            for A in self.nonterminals:
                for v, alternatives in self.rules.items():
                    for alternative in alternatives:
                        if not A in alternative: continue
                        i = alternative.index(A)
                        if i + 1 < len(alternative):
                            self.follow[A] |= self.first_of(alternative[i + 1:]) - \
                                              set([EPSILON])
                            if EPSILON in self.first_of(alternative[i + 1:]):
                                self.follow[A] |= self.follow[v]
                        else:
                            self.follow[A] |= self.follow[v]

            if break_next and buf == self.follow:
                break
            break_next = buf == self.follow

    def get_augmented(self):
        """For a grammar G with start symbol S, G' is the augmented grammar --
        it is just G with a new start symbol S' and production S' -> S. The
        purpose of this new starting production is to indicate to the parser
        when it should stop parsing and announce acceptance of the input. That
        is, acceptance occurs when and only when the parser is about to reduce
        by S' -> S.
        """
        new_rules = dict(self.rules)
        new_start_symbol = cfg.start_symbol + "'"
        new_rules[new_start_symbol] = [[cfg.start_symbol]]

        augmented = ContextFreeGrammar(new_start_symbol, new_rules)
        return augmented
