from typing import Set
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """
    Esta función crea un DFA según la expresión regular dada.

    # Opciones

    @ `regex` - expresión regular.

    # Devoluciones

    Devuelve un DFA para la expresión dada.
    """
    epsilon_nfa = Regex(regex).to_epsilon_nfa()
    return epsilon_nfa.to_deterministic()

def graph_to_nfa(
  graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton: 
    """
    Esta función crea un NFA dado un graph y un conjunto de nodos de start y final.

    # Opciones

    @ `graph` - este graph.
    @ `start_states` - lista con los estados de start.
    @ `final_states` - lista con los estados de final.

    # Devoluciones

    Devuelve un DFA para las graph y states dada.
    """
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    moved_nodes = None 
    if len(start_states) == 0:
        moved_nodes = list(map(lambda x: State(x), graph.nodes))
        for state in moved_nodes:
            nfa.add_start_state(state)
    else:
        for state in start_states:
            nfa.add_start_state(state)
    if len(final_states) == 0:
        if moved_nodes is None:
            moved_nodes = list(map(lambda x: State(x), graph.nodes))
        for state in moved_nodes:
            nfa.add_final_state(state)
    else:
        for state in final_states:
            nfa.add_final_state(state)
    return nfa