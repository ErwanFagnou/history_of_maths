import networkx as nx
import numpy as np
import igraph as ig

from scripts.build_graphs import get_all_data, get_math_graph


def draw_math_graph(nx_graph, file, size_decay=2):
    print(f'Generating image for the math {nx_graph}...')

    print(' - Computing PageRank...')
    pr = nx.pagerank(nx_graph, alpha=0.85)

    m = np.max([pr[i] for i in nx_graph.nodes])

    print(' - Preparing the graph...')
    node_min_size = 3
    node_max_size = 300
    # size_decay = 2  # size proportional to: (pagerank / m) ** decay
    node_sizes = [node_min_size + (node_max_size - node_min_size) * (pr[i] / m) ** size_decay for i in nx_graph.nodes]

    node_colors = ['#%02x%02x%02xAA' % (int(255 * pr[i] / m), 0, int(255 * (1 - pr[i] / m))) for i in nx_graph.nodes]

    node_labels = [nx_graph.nodes[node]['title'] for node in nx_graph.nodes]

    label_min_size = 10
    label_max_size = 100
    label_sizes = [label_min_size + (label_max_size - label_min_size) * pr[i] / m for i in nx_graph.nodes]

    label_min_transparency = 127
    label_colors = ['#%02x%02x%02x%02x' % (int(255 * pr[i] / m), 0, 0, label_min_transparency + int((255-label_min_transparency)*pr[i]/m)) for i in nx_graph.nodes]

    g = ig.Graph()
    g = g.from_networkx(nx_graph)
    # pos = g.layout(layout='auto')
    # g.layout

    print(' - Creating the file...')
    ig.plot(g,
            bbox=(20000, 20000),
            vertex_size=node_sizes,
            vertex_color=node_colors,
            vertex_label=node_labels,
            vertex_label_color=label_colors,
            vertex_label_size=label_sizes,
            vertex_label_dist=1,
            vertex_order=np.argsort(node_sizes),
            edge_width=0.5,
            edge_arrow_size=0.5,
            edge_arrow_width=0.5,
            edge_curved=0.5,
            target=file,
            )


if __name__ == '__main__':
    all_data = get_all_data()
    # theorem_graph = get_math_graph(all_data, keep_isolated_nodes=True)
    theorem_graph = get_math_graph(all_data, keep_isolated_nodes=False)
    draw_math_graph(theorem_graph, '../images/math_graph_test.png')
