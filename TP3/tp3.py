 #TP3

from TP1 import *


def nb_triangle(graph,voisins_sommet, sommet):
	compte = 0
	voisins = g.neighbors(sommet)
	voisins_sommet[voisins] = True
	#voisin = graph.neighbors(sommet)
	for s, yes_or_no in enumerate(voisins_sommet):
		if yes_or_no:
			for v_2 in graph.neighbors(s):
				if voisins_sommet[v_2]:
					compte += 1
	compte = int(compte/2)
	voisins_sommet[voisins] = False
	return compte

def clust(g, voisins_sommet):
	clust_local = 0
	nbr_triangles = 0
	for s in range(g.n):
		if g.deg[s] == 1 or g.deg[s] == 0:
			clust_local += 0
		else:
			nbr_triangles += nb_triangle(g, voisins_sommet, s)
			clust_local += (2 * nb_triangle(g, voisins_sommet, s)) / (g.deg[s] * (g.deg[s] - 1))
	print(format(clust_local/g.n, '.5f'))
	print(nbr_triangles / 3)
	return clust_local/g.n

if __name__ == "__main__":
	triangle = sys.argv[1]
	filename = sys.argv[2]
	nb_arc = int(sys.argv[3])

	#sommet = int(sys.argv[4])
	edg = read_edges(filename, nb_arc)
	g = Graph(edg, symmetrize=True)
	#tableau numpy de taille nbr_sommets True ==> voisin de sommet
	voisins_sommet = np.zeros(g.n, dtype = bool)
	

	#on passe ce tableau à notre fonction
	
	#print(nb_triangle(g,voisins_sommet, sommet))
	clust(g, voisins_sommet)
    