import networkx as nx, numpy as np, sys, time
from random import seed

def betweenness_centrality(c, n, m):
    bc, duration = 0.0, 0.0
    for i in range(c):
        graph = nx.barabasi_albert_graph(n, m)
        start = time.time()
        bc += np.mean(list(nx.betweenness_centrality(graph).values()))
        stop = time.time()
        duration += stop - start
    bc /= c
    duration /= c
    print('Betweenness Centrality:  {} ({}s/call)'.format(bc, duration))

def clustering_coefficient(c, n, m):
    cc, duration = 0.0, 0.0
    for i in range(c):
        graph = nx.barabasi_albert_graph(n, m)
        start = time.time()
        cc += nx.average_clustering(graph)
        stop = time.time()
        duration += stop - start
    cc /= c
    duration /= c
    print('Average Clustering Coefficient:  {} ({}s/call)'.format(cc, duration))

def main():
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    if len(sys.argv) > 3:
        seed(sys.argv[3])

    betweenness_centrality(5, n, m)
    clustering_coefficient(10, n, m)

if __name__ == '__main__':
    main()
