from collections.abc import Iterable
from scipy.sparse import dok_matrix


def make_iterable(value):
    if not isinstance(value, Iterable):
        return {value}
    else:
        return value


def make_boolean_matrix_from_fa(symbols, states, finite_automata, size):
    map_state_to_idx = {state: idx for (idx, state) in enumerate(states)}
    # mapa init
    map_symbol_to_matrix = dict()

    for symbol in symbols:
        map_symbol_to_matrix[symbol] = dok_matrix((size, size))

    # automata.to_dict() has no 'orient' option, so we're forced to do this:
    for state_from, transitions in finite_automata.to_dict().items():
        for symbol, targets in transitions.items():
            for state_to in make_iterable(targets):
                map_symbol_to_matrix[symbol][
                    map_state_to_idx[state_from], map_state_to_idx[state_to]
                ] = True
    return map_symbol_to_matrix


def make_set_idx(map, states):
    return set(map[s] for s in states)
