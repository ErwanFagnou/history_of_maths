import pickle

import networkx as nx


def get_all_data():
    file = '../data/all_data.pkl'

    with open(file, 'rb') as f:
        all_data = pickle.load(f)
        return all_data


def get_math_graph(all_data, keep_isolated_nodes=True):
    print('Building the math graph (directed):')
    g = nx.DiGraph()
    n = len(all_data)
    print(f' - Building {n} nodes...')
    for i, (url, (topic_paths, _, _)) in enumerate(all_data.items()):
        title = topic_paths[0][-1]
        g.add_node(url, title=title)

    print(' - Building edges...')
    for i, (url, (topic_paths, see_also_urls, _)) in enumerate(all_data.items()):
        if g.has_node(url):
            for see_also_url in see_also_urls:
                if g.has_node(see_also_url):
                    g.add_edge(url, see_also_url)

    if not keep_isolated_nodes:
        print(' - Removing isolated nodes...')
        g.remove_nodes_from(list(nx.isolates(g)))
    return g


def get_math_and_mathematicians_graph(all_data, keep_only_references_with_year=False, keep_isolated_nodes=True, reference_weight=1, min_year=1000, max_year=2022):
    print('Building the math & mathematician graph:')
    g = nx.DiGraph()

    print(f' - Building math nodes...')
    for i, (url, (topic_paths, _, _)) in enumerate(all_data.items()):
        title = topic_paths[0][-1]
        g.add_node(url, title=title, bipartite=0)

    print(' - Building mathematician nodes and edges...')
    # mathematician_nb_refs = dict()
    nb_edges_see_also = 0
    nb_edges_reference = 0
    for i, (url, (topic_paths, see_also_urls, referenced_mathematicians)) in enumerate(all_data.items()):

        # see also
        for see_also_url in see_also_urls:
            if g.has_node(see_also_url):
                g.add_edge(url, see_also_url, type='see_also', weight=1)  # directed edge
                nb_edges_see_also += 1

        # mathematicians
        for mathematician, publication_year in referenced_mathematicians.items():
            mathematician = mathematician.split('.')[0]  # keep only the first part of the complete name
            if not keep_only_references_with_year or (publication_year is not None and min_year <= publication_year < max_year):
                if not g.has_node(mathematician):
                    g.add_node(mathematician, title=mathematician, bipartite=1)
                    # mathematician_nb_refs[mathematician] = 0
                g.add_edge(url, mathematician, year=publication_year, type='reference', weight=reference_weight)  # undirected edge
                g.add_edge(mathematician, url, year=publication_year, type='reference', weight=reference_weight)
                # mathematician_nb_refs[mathematician] += 1
                nb_edges_reference += 1

    # regularize edges
    for u, v in g.edges:
        if g.edges[u, v]['type'] == 'reference':
            g.edges[u, v]['weight'] = reference_weight * nb_edges_see_also / nb_edges_reference

    if not keep_isolated_nodes:
        print(' - Removing isolated nodes...')
        g.remove_nodes_from(list(nx.isolates(g)))

    return g
