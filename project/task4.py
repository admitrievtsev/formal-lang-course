import numpy as np
from networkx.classes import MultiDiGraph
from scipy.sparse import vstack
from scipy.sparse import csr_matrix

from project.utils import transpose_boolean_matrix
from project.task3 import AdjacencyMatrixFA
from project.task2 import regex_to_dfa
from project.task2 import graph_to_nfa


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    adj_matrix_of_graph = AdjacencyMatrixFA(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )
    adj_matrix_of_regex = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_bool_t = transpose_boolean_matrix(adj_matrix_of_graph.boolean_matrix)

    g_size = len(adj_matrix_of_graph.states)
    r_size = len(adj_matrix_of_regex.states)

    visited = {
        graph_state: csr_matrix((g_size, r_size))
        for graph_state in adj_matrix_of_graph.start_states
    }
    for graph_state in adj_matrix_of_graph.start_states:
        for regex_state in adj_matrix_of_regex.start_states:
            visited[graph_state][
                adj_matrix_of_graph.map_state_to_idx[graph_state],
                adj_matrix_of_regex.map_state_to_idx[regex_state],
            ] = True

    visited = vstack(list(visited.values()), format="csr")
    front = visited.copy()

    symbols = adj_matrix_of_graph.symbols & adj_matrix_of_regex.symbols
    while True:
        front = sum({
            symbol: vstack(
                [
                    (graph_bool_t[symbol] @ front[idx * g_size : g_size * (idx + 1)])
                    for idx in range(0, len(adj_matrix_of_graph.start_states))
                ],
                format="csr",
            )
            @ adj_matrix_of_regex.boolean_matrix[symbol]
            for symbol in symbols
        }.values())
        if (visited >= front).toarray().all():
            break
        else:
            visited += front

    set_reachable = set()
    for idx, state_from in enumerate(adj_matrix_of_graph.start_states):
        for regex_final in adj_matrix_of_regex.final_states:
            for graph_final in adj_matrix_of_graph.final_states:
                if visited[g_size * idx : (idx + 1) * g_size].getcol(
                    adj_matrix_of_regex.map_state_to_idx[regex_final]
                )[adj_matrix_of_graph.map_state_to_idx[graph_final], 0]:
                    set_reachable.add((state_from.value, graph_final.value))

    return set_reachable
