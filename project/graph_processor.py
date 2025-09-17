# Tarea uno & dos
import cfpq_data
import networkx


class GraphReport:
    def __init__(self, edges_num, nodes_num, labels):
        """
        Función que crea una nueva entidad de `GraphReport`.

        # Opciones

        @ `edges_num` - Número de edges entre vértices.
        @ `nodes_num` - Número de nodes.
        @ `labels` - Lista de labels.
        """
        self.edges_num = edges_num
        self.nodes_num = nodes_num
        self.labels = labels


def generate_graph_report(name) -> GraphReport:
    """
    Función que devuelve un `GraphReport` por `name` de gráfico.

    # Opciones

    @ `names` - Nombre del graph.
    """

    graph_path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return GraphReport(
        edges_num=graph.number_of_nodes(),
        nodes_num=graph.number_of_edges(),
        labels=cfpq_data.get_sorted_labels(graph),
    )


def generate_and_save_graph_with_two_cycles(cycle_nodes_num, labels, path):
    """
    Una función que genera y guarda un graph con dos ciclos en formato `.dot`.

    # Opciones

    @ `cycle_nodes_num` - Número de nodes en un ciclo.
    @ `labels` - Lista de labels.
    @ `path` - Path del archivo `.dot`.
    """
    networkx.nx_pydot.write_dot(
        cfpq_data.labeled_two_cycles_graph(
            cycle_nodes_num[0], cycle_nodes_num[1], labels=labels
        ),
        path,
    )
