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

Where the fields are of type CoreVariable, CoreLiteral, or CoreCons.
"""

from funky.util import get_unique_varname
from funky.frontend import FunkyDesugarError

from funky.corelang.coretree import CoreCons, CoreVariable, CoreLiteral, \
                                    CoreMatch, CoreAlt

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

def get_specialised_and_default_matrices(scrutinee, pattern_matrix, outcomes):
    """Given a scrutinee, a pattern matrix, and a list of outcomes
    corresponding to the rows in the pattern matrix, returns the specialised
    and default matrices for that scrutinee.
    """
    specialised, specialised_outcomes = [], []
    default, default_outcomes = [], []

    for row, outcome in zip(pattern_matrix, outcomes):
        x, y = row[0], scrutinee
        if isinstance(x, CoreVariable):
            default.append(row)
            default_outcomes.append(outcome)
            specialised.append(row)
            specialised_outcomes.append(outcome)
        elif isinstance(x, CoreLiteral):
            if isinstance(y, CoreLiteral) and \
               x.value == y.value and x.typ == y.typ:
                specialised.append(row)
                specialised_outcomes.append(outcome)
            else:
                default.append(row)
                default_outcomes.append(outcome)
        elif isinstance(x, CoreCons):
            if isinstance(y, CoreCons) and \
               x.constructor == y.constructor and \
               len(x.parameters) == len(y.parameters):
                specialised.append(row)
                specialised_outcomes.append(outcome)
            else:
                default.append(row)
                default_outcomes.append(outcome)
        else:
            raise FunkyDesugarError("Attempted to match things with types " + \
                                    "{} and {}.".format(type(x), type(y)))
    
    return specialised, specialised_outcomes, default, default_outcomes

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
    scrutinee = pattern_matrix[0][0] # <-- the top left element of the matrix

    specialised, specialised_outcomes, default, default_outcomes = \
    get_specialised_and_default_matrices(scrutinee, pattern_matrix, outcomes)

    # drop the first element for our specialised variables -- we have
    # 'considered' it.
    specialised_variables = variables[1:]

    altcon = None

    # if our scrutinee is a construction, we must 'expand' it, placing its
    # parameters into the specialised matrix explicitly.
    if isinstance(scrutinee, CoreCons):
        for param in reversed(scrutinee.parameters):
            # use the given name if it exists -- otherwise, generate one
            var = param if isinstance(param, CoreVariable) \
                        else CoreVariable(get_unique_varname())
            specialised_variables.insert(0, var)
        for row in specialised:
            x = row.pop(0)
            for param in reversed(x.parameters):
                row.insert(0, param)
        altcon = CoreCons(scrutinee.constructor,
                          specialised_variables[:len(scrutinee.parameters)])
    else:
        # otherwise, just drop the first row.
        specialised = [row[1:] for row in specialised]
        altcon = scrutinee

    alts = [
        CoreAlt(altcon, get_match_tree(specialised, specialised_variables,
                                       specialised_outcomes)),
        CoreAlt(CoreVariable("_"), get_match_tree(default, variables[:],
                                                  default_outcomes)),
    ]

    return CoreMatch(variables[0], alts)
