import networkx as nx
import numpy as np
import igraph as ig

from scripts.build_graphs import get_all_data, get_math_and_mathematicians_graph


def draw_math_and_mathematicians_graph(nx_graph, file):
    print(f'Generating image for the Math-Mathematicians {nx_graph}...')

    print(' - Computing PageRank...')
    pr = nx.pagerank(nx_graph, alpha=0.85)
    m_math = np.max([pr[i] for i in nx_graph.nodes if nx_graph.nodes[i]['bipartite'] == 0])
    m_mathematicians = np.max([pr[i] for i in nx_graph.nodes if nx_graph.nodes[i]['bipartite'] == 1])

    print(' - Preparing the graph...')

    node_min_size = 3
    node_max_size = 300
    size_decay = 2  # size proportional to: (pagerank / m) ** decay

    label_min_size = 10
    label_max_size = 100
    label_min_transparency = 127

    node_sizes = []
    node_colors = []
    node_shapes = []
    node_labels = []
    label_sizes = []
    label_colors = []
    for node in nx_graph.nodes:
        is_mathematician = nx_graph.nodes[node]['bipartite']

        m = m_math if not is_mathematician else m_mathematicians  # max pr value for the category
        node_sizes.append(node_min_size + (node_max_size - node_min_size) * (pr[node] / m) ** size_decay)

        node_colors.append('#%02x%02x%02xAA' % (int(255 * pr[node] / m), 0, int(255 * (1 - pr[node] / m))))

        node_shapes.append('circle' if not is_mathematician else 'rectangle')

        node_labels.append(nx_graph.nodes[node]['title'])

        label_sizes.append(label_min_size + (label_max_size - label_min_size) * pr[node] / m)

        label_colors.append('#%02x%02x%02x%02x' % (
            int(255 * pr[node] / m), 0, 0, label_min_transparency + int((255 - label_min_transparency) * pr[node] / m)))

    edge_curved = [0.5 if nx_graph.edges[e]['type'] == 'see_also' else 0 for e in nx_graph.edges]

    g = ig.Graph()
    g = g.from_networkx(nx_graph)

    print(' - Creating the file...')
    ig.plot(g,
            bbox=(20000, 20000),
            vertex_size=node_sizes,
            vertex_color=node_colors,
            vertex_shape=node_shapes,
            vertex_label=node_labels,
            vertex_label_color=label_colors,
            vertex_label_size=label_sizes,
            vertex_label_dist=1,
            vertex_order=np.argsort(node_sizes),
            edge_width=0.5,
            edge_arrow_size=0.5,
            edge_arrow_width=0.5,
            edge_curved=edge_curved,
            target=file,
            )


if __name__ == '__main__':
    all_data = get_all_data()
    math_and_mathematicians_graph = get_math_and_mathematicians_graph(all_data,
                                                                      keep_only_references_with_year=True,
                                                                      keep_isolated_nodes=False,
                                                                      reference_weight=1)
    draw_math_and_mathematicians_graph(math_and_mathematicians_graph, '../images/math_and_mathematicians_graph_test.png')
