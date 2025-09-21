from project.task2 import regex_to_dfa, graph_to_nfa
from project.utils import make_boolean_matrix_from_fa, make_set_idx
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from networkx import MultiDiGraph
from scipy.sparse import dok_matrix, identity, kron
from collections.abc import Iterable


class AdjacencyMatrixFA:
    def __init__(self, finite_automata: NondeterministicFiniteAutomaton):
        self.symbols = finite_automata.symbols
        self.states = finite_automata.states
        self.map_state_to_idx = {state: idx for (idx, state) in enumerate(self.states)}
        self.start_states = finite_automata.start_states
        self.final_states = finite_automata.final_states
        self.boolean_matrix = make_boolean_matrix_from_fa(
            finite_automata.symbols,
            finite_automata.states,
            finite_automata,
            len(finite_automata.states),
        )

    def get_transitive_closure(self) -> dok_matrix:
        n = len(self.states)
        transitive_closure = dok_matrix((n, n))
        transitive_closure += identity(n, format="dok")

        for symbol in self.boolean_matrix:
            transitive_closure += self.boolean_matrix[symbol]

        for k in range(0, n):
            for i in range(0, n):
                if not transitive_closure[i, k]:
                    continue
                else:
                    for j in range(0, n):
                        if not transitive_closure[k, j]:
                            continue
                        else:
                            transitive_closure[i, j] = True
        return transitive_closure

    def accepts(self, word: Iterable[Symbol]) -> bool:
        states = make_set_idx(self.map_state_to_idx, self.start_states)
        for symbol in word:
            if symbol in self.boolean_matrix:
                reached_states = set()
                mat = self.boolean_matrix[symbol]
                for state_from in states:
                    reached_states = reached_states.union(
                        set(mat.getrow(state_from).indices)
                    )
                states = reached_states
            else:
                return False
        intersected = states.intersection(
            make_set_idx(self.map_state_to_idx, self.final_states)
        )
        return intersected != set()

    def is_empty(self) -> bool:
        transitive_closure = self.get_transitive_closure()
        for state_from in make_set_idx(self.map_state_to_idx, self.start_states):
            for state_to in make_set_idx(self.map_state_to_idx, self.final_states):
                if transitive_closure[state_from, state_to]:
                    return False
        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    intersected_automation = AdjacencyMatrixFA.__new__(AdjacencyMatrixFA)
    intersected_automation.symbols = automaton1.symbols.intersection(automaton2.symbols)
    intersected_automation.states = set()
    intersected_automation.map_state_to_idx = dict()
    intersected_automation.start_states = set()
    intersected_automation.final_states = set()
    intersected_automation.boolean_matrix = dict()

    for idx1, state_first in enumerate(automaton1.states):
        for idx2, state_second in enumerate(automaton2.states):
            intersected_automation.map_state_to_idx[
                State((state_first.value, state_second.value))
            ] = idx2 + len(automaton2.states) * idx1
            intersected_automation.states.add(
                State((state_first.value, state_second.value))
            )

    for state_first in automaton1.start_states:
        for state_second in automaton2.start_states:
            intersected_automation.start_states.add((state_first, state_second))

    for state_first in automaton1.final_states:
        for state_second in automaton2.final_states:
            intersected_automation.final_states.add((state_first, state_second))

    for symbol in intersected_automation.symbols:
        intersected_automation.boolean_matrix[symbol] = kron(
            automaton1.boolean_matrix[symbol], automaton2.boolean_matrix[symbol]
        )

    return intersected_automation


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_boolean_matrix = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_boolean_matrix = AdjacencyMatrixFA(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )
    intersected_boolean_matrix = intersect_automata(
        regex_boolean_matrix, graph_boolean_matrix
    )
    transitive_closure = intersected_boolean_matrix.get_transitive_closure()
    states = set()
    for state_from in intersected_boolean_matrix.start_states:
        for state_to in intersected_boolean_matrix.final_states:
            if transitive_closure[
                intersected_boolean_matrix.map_state_to_idx[state_from],
                intersected_boolean_matrix.map_state_to_idx[state_to],
            ]:
                temp_state_from = state_from
                temp_state_to = state_to
                if len(state_from) != 1:
                    temp_state_from = state_from[1]
                if len(state_to) != 1:
                    temp_state_to = state_to[1]
                states.add((temp_state_from.value, temp_state_to.value))
    return states
