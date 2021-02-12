 #TP3

from TP1 import *


def nb_triangle(graph,sommet):
	print()


if __name__ == "__main__":
	triangle = sys.argv[1]
	filename = sys.argv[2]
	nb_arc = sys.argv[3]
	sommet = sys.argv[4]
	edg = read_edges(fname, m_estim)
	g = Graph(edg, symmetrize=True)

    # fname = sys.argv[1]
    # m_estim = int(sys.argv[2])
    # mem()
    # edg = read_edges(fname, m_estim)
    # mem()
    # g = Graph(edg, symmetrize=True)
    # print(f"n={g.n}")
    # print(f"m={g.m}")
    # mem()
    # degmax = 0
    # for u in g.nodes() :
    #     du = len(g.neighbors(u))
    #     if du > degmax :
    #         degmax = du
    # print(f"degmax={degmax}")
    # mem()
    # trav = Traversal(g.n)
    # src = int(sys.argv[3])
    # dst = int(sys.argv[4])
    # for i in range(1) : trav.bfs(g, src+i) # 10s per BFS on soc-pokec
    # print(f"dist={trav.dist[dst]}")
    # mem()