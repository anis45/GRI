 #TP3

from TP1 import *


def nb_triangle(graph,sommet):
	compte = 0
	voisin = graph.neighbors(sommet)
	for v in voisin:
		for v_2 in graph.neighbors(v):
			if v_2 in voisin:
				compte += 1
	compte = int(compte/2)
	print(compte)
	return compte

if __name__ == "__main__":
	triangle = sys.argv[1]
	filename = sys.argv[2]
	nb_arc = int(sys.argv[3])
	sommet = int(sys.argv[4])
	edg = read_edges(filename, nb_arc)
	g = Graph(edg, symmetrize=True)
	nb_triangle(g,sommet)
    