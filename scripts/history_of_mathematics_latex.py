import networkx as nx

from scripts.build_graphs import get_math_and_mathematicians_graph, get_all_data


def math_ranking_evolution(all_data, latex=True):
    year_step = 25
    start_year = 1800
    end_year = 2021

    all_top_urls = dict()
    k_best = 10

    all_rankings = dict()

    titles = []
    for a in range(start_year, end_year, year_step):
        b = a + year_step
        titles.append(f'{a}-{(b) % 100:02d}')

        # Build graph
        theorem_and_mathematician_graph = get_math_and_mathematicians_graph(all_data,
                                                                            keep_isolated_nodes=True,
                                                                            keep_only_references_with_year=True,
                                                                            min_year=a,
                                                                            max_year=b,
                                                                            reference_weight=100)
        # PageRank
        pr = nx.pagerank(theorem_and_mathematician_graph, alpha=0.85)
        print(theorem_and_mathematician_graph)

        # Sort
        ranked_math = sorted([x for x in pr.items() if theorem_and_mathematician_graph.nodes[x[0]]['bipartite'] == 0],
                             key=lambda x: x[1], reverse=True)
        all_rankings[a] = [x[0] for x in ranked_math]
        for url, score in ranked_math[:k_best]:
            if url not in all_top_urls:
                all_top_urls[url] = []
            all_top_urls[url].append(a)

    if latex:
        print("\\begin{tabular} {|c|" + 'c' * len(titles) + "|}")
        print('\\textbf{Name} &',
              ' & '.join(f'\\begin{{rotate}}{{60}}\\textbf{{{col_title}}}\\end{{rotate}}' for col_title in titles), '\\\\')
    ranked_urls = sorted([url for url in all_top_urls], key=lambda url: len(all_top_urls[url]), reverse=True)

    all_lines = []
    for url in ranked_urls:
        ranks = [(str(all_rankings[a].index(url) + 1) if all_rankings[a].index(url) < 2 * k_best else '') if url in
                                                                                                             all_rankings[
                                                                                                                 a] else ''
                 for a in range(start_year, end_year, year_step)]
        all_lines.append((theorem_and_mathematician_graph.nodes[url]['title'], ranks))

    all_lines = sorted(all_lines, key=lambda x: x[1], reverse=True)

    for name, ranks in all_lines:
        if latex:
            print('\\hline ')
            print(name, *ranks, sep=' & ', end=' \\\\ \n')
        else:
            print(f"{name} {' '*(25-len(name))} | ", *[' '*(5-len(str(r))) + str(r) for r in ranks])

    if latex:
        print('\\hline \n\\end{tabular} ')


if __name__ == '__main__':
    all_data = get_all_data()
    math_ranking_evolution(all_data, latex=False)
    # math_ranking_evolution(all_data, latex=True)
