import networkx as nx
import pyformlang


def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
    normal_form = cfg.to_normal_form()
    productions = set(normal_form.productions)
    for nullable_symbol in cfg.get_nullable_symbols():
        productions.add(
            pyformlang.cfg.Production(
                pyformlang.cfg.Variable(nullable_symbol.value),
                [pyformlang.cfg.Epsilon()],
            )
        )
    wnf = pyformlang.cfg.CFG(
        None,
        None,
        normal_form.start_symbol,
        productions,
    ).remove_useless_symbols()
    return wnf


def hellings_based_cfpq(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    cfpq = set()
    edges = graph.edges(None, "label")
    nodes = graph.nodes()
    wnf = cfg_to_weak_normal_form(cfg)
    productions = set(wnf.productions)
    nullable = wnf.get_nullable_symbols()

    for n in nodes:
        for sym in nullable:
            cfpq.add((n, sym, n))

    for production in productions:
        for n1, n2, label in edges:
            if [i.value for i in production.body] == [label]:
                cfpq.add((n1, production.head, n2))

    fg = False
    while not fg:
        addition = set()
        for n11, x1, n12 in cfpq:
            for n21, x2, n22 in cfpq:
                for prod in productions:
                    if n12 == n21 and prod.body == [x1, x2]:
                        addition.add((n11, prod.head, n22))
        if addition <= cfpq:
            fg = True
            continue
        cfpq |= addition

    new_cfpq = set()
    for n1, x, n2 in cfpq:
        if n1 in start_nodes and n2 in final_nodes and x == wnf.start_symbol:
            new_cfpq.add((n1, n2))

    return new_cfpq
