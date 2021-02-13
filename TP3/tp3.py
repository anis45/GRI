 #TP3

from TP1 import *


def nb_triangle(graph,voisins_sommet):
	compte = 0
	#voisin = graph.neighbors(sommet)
	for s, yes_or_no in enumerate(voisins_sommet):
		if yes_or_no:
			for v_2 in graph.neighbors(s):
				if voisins_sommet[v_2]:
					compte += 1
	compte = int(compte/2)
	return compte

if __name__ == "__main__":
	triangle = sys.argv[1]
	filename = sys.argv[2]
	nb_arc = int(sys.argv[3])

	sommet = int(sys.argv[4])
	edg = read_edges(filename, nb_arc)
	g = Graph(edg, symmetrize=True)
	#tableau numpy de taille nbr_sommets True ==> voisin de sommet
	voisins_sommet = np.zeros(g.n, dtype = bool)
	voisins = g.neighbors(sommet)
	voisins_sommet[voisins] = True

	#on passe ce tableau à notre fonction
	
	print(nb_triangle(g,voisins_sommet))
    