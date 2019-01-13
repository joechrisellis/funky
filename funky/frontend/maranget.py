"""Implementation of Luc Maranget's algorithm for compiling pattern matches
into good decision trees. The paper that describes the algorithm is available
here: http://moscova.inria.fr/~maranget/papers/ml05e-maranget.pdf

The algorithm expects a matrix of patterns. For instance, given the following
function:

    g _ F T = 1
    g F T _ = 2
    g _ _ F = 3
    g _ _ T = 4

The algorithm expects a matrix:

    ( _ F T )
    ( F T _ )
    ( _ _ F )
    ( _ _ T )

A set of binding variables, and a set of possible outcomes.

Where the fields are of type CoreVariable, CoreLiteral, or CorePattern.
"""

from funky.frontend import FunkyDesugarError

from funky.corelang.coretree import CoreCons, CoreVariable, CoreLiteral, \
                                    CoreMatch, CoreAlt

def match(x, y):
    """Does x match y?"""
    if isinstance(x, CoreCons):
        # constructors only bind if they are of the same type and their
        # parameters recursively match.
        if not isinstance(y, CoreCons) or \
           x.constructor != y.constructor or \
           len(x.parameters) != len(y.parameters):
            return False
        return all(match(a, b) for a, b in zip(x.parameters, y.parameters))
    elif isinstance(x, CoreVariable):
        # variables bind to anything.
        return True
    elif isinstance(x, CoreLiteral):
        # literals only bind to ones with the same type and value.
        return isinstance(y, CoreLiteral) and \
               x.value == y.value and x.typ == y.typ
    else:
        raise FunkyDesugarError("Attempted to match things with types " + \
                                "{} and {}.".format(type(x), type(y)))

def get_column_scores(pattern_matrix):
    """Scores the columns. Wildcards do not add anything to a column's score.
    Similarly, anything below a wildcard does not add to a column's score.
    """
    columns = list(zip(*pattern_matrix))
    scores = [0 for _ in columns]
    for i, column in enumerate(columns):
        for pattern in column:
            if isinstance(pattern, CoreVariable):
                break
            scores[i] += 1
    return scores

def get_match_tree(pattern_matrix, variables, outcomes):
    if not pattern_matrix:
        return None
    if all(isinstance(x, CoreVariable) for x in pattern_matrix[0]):
        # all 'wildcards' -- this is the base case.
        return outcomes[0]

    # find the most necessary column
    scores = get_column_scores(pattern_matrix)
    best_column = scores.index(max(scores))

    # swap the first column with the most necessary column in the matrix
    columns = list(zip(*pattern_matrix))
    columns[0], columns[best_column] = columns[best_column], columns[0]
    variables[0], variables[best_column] = variables[best_column], variables[0]
    pattern_matrix = [list(t) for t in zip(*columns)]

    # we now generate the first switch of the decision tree. We compute two new
    # matrices: a specialised matrix that remains after a successful match, and
    # a default matrix for if we don't find a match.

    # assume we matched on the first pattern. We are left with the rows whose 
    # first value matches with the first value of the first row
    specialised, specialised_outcomes = [], []
    default, default_outcomes = [], []
    for row, outcome in zip(pattern_matrix, outcomes):
        if isinstance(row[0], CoreVariable):
            default.append(row)
            default_outcomes.append(outcome)
            specialised.append(row[1:])
            specialised_outcomes.append(outcome)
        elif not match(row[0], pattern_matrix[0][0]):
            default.append(row)
            default_outcomes.append(outcome)
        else:
            specialised.append(row[1:])
            specialised_outcomes.append(outcome)

    alts = [
        CoreAlt(pattern_matrix[0][0], get_match_tree(specialised, variables[1:],
                                                     specialised_outcomes)),
        CoreAlt(CoreVariable("_"), get_match_tree(default, variables[:],
                                                  default_outcomes)),
    ]

    return CoreMatch(CoreVariable(variables[0]), alts)
