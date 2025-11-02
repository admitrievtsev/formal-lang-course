from typing import Set

import networkx as nx
import pyformlang
from scipy.sparse import csr_matrix

from project.task6 import cfg_to_weak_normal_form


def matrix_based_cfpq(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:
    wnf = cfg_to_weak_normal_form(cfg)
    productions = wnf.productions
    variables = len(set(wnf.variables))
    map_node = dict()
    map_idx = dict()
    for i, node in enumerate(graph.nodes):
        map_node[node] = i

    decomposed = dict()
    for variable in wnf.variables:
        decomposed[variable] = csr_matrix((len(graph), len(graph)), dtype=bool)

    for nullable in wnf.get_nullable_symbols():
        decomposed[nullable].setdiag(True, 0)

    for production in productions:
        for p1, p2, label in graph.edges.data("label"):
            if [n.value for n in production.body] == [label]:
                decomposed[production.head][map_node[p1], map_node[p2]] = True

    while variables > 0:
        for production in productions:
            if not (len(production.body) < 2):
                multiplied = decomposed[production.head].__add__(
                    decomposed[production.body[0]].__matmul__(
                        decomposed[production.body[1]]
                    )
                )
                if (decomposed[production.head].__ne__(multiplied)).count_nonzero():
                    variables += 1
                    decomposed[production.head] = multiplied
        variables -= 1

    pairs = zip(*decomposed[wnf.start_symbol].nonzero())

    new_cfpq = set()

    for i, node in enumerate(graph.nodes):
        map_idx[i] = node

    if not map_idx:
        return new_cfpq

    for n_from, n_to in pairs:
        if map_idx[n_from] in start_nodes and map_idx[n_to] in final_nodes:
            new_cfpq.add((map_idx[n_from], map_idx[n_to]))

    return new_cfpq
