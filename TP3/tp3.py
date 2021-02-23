from TP1 import *
from queue import PriorityQueue
import time



class degres :
	def __init__(self,g):
		self.marked = np.full((g.n), True)
		self.deg = np.zeros(g.n, dtype='int32')
		self.fin = 0
		for v in range(g.n):
			self.deg[v] = len(g.neighbors(v))

	def mark(self,sommet,pq):
		self.marked[sommet]=False
		self.fin += 1
		for v in g.neighbors(sommet):
			if self.marked[v]: 
				self.deg[v]= self.deg[v]-1
				pq.put((self.deg[v],v))


def nb_triangle(graph,voisins_sommet, sommet):
	compte = 0
	voisins = graph.neighbors(sommet)
	voisins_sommet[voisins] = True
	
	for v in voisins:
		
		#if not vertex_visited[v]:
		for v_2 in graph.neighbors(v):
				
				#if not vertex_visited[v_2]:
			if voisins_sommet[v_2]:
				compte += 1	

	#vertex_visited[sommet] = True
	voisins_sommet[voisins] = False
	
	return int(compte/2)

def clust(g, voisins_sommet,):
	clust_local = 0
	nbr_triangles = 0
	nv = 0
	for v in range(g.n):

		deg = len(g.neighbors(v))
		for i in range(1,deg):
			nv +=i
		if deg == 1 or deg == 0:
			continue
		else:
			nb_tr = nb_triangle(g, voisins_sommet,v)
			nbr_triangles += nb_tr 
			clust_local += (2 * nb_tr ) / (deg * (deg - 1))
	

	print(format(clust_local/g.n, '.5f'))
	print(format(nbr_triangles/nv, '.5f'))

	return clust_local/g.n

def k_coeur(g):
	deg_objet = degres(g)
	q = PriorityQueue()
	b = True
	res = 0
	res2 = 0
	for v in range(g.n):
		q.put((deg_objet.deg[v],v))
	for k in range(1,g.n):
		res2 = 0
		while(1):
			if (q.qsize() == 0):
				b = False
				break
			nb_vs,sommet = q.get()
			if deg_objet.marked[sommet] == True:
				if (nb_vs <= k ):
					res2 += 1
					deg_objet.mark(sommet,q)
					if(deg_objet.fin == len(deg_objet.marked)):                       ### pour eviter "if (not (True in deg_objet.marked))"
						b = False
						res = k
						break
				else:
					q.put((nb_vs,sommet))
					break
		if (not (b)):
			break

	print(k,res2)
		# 	deg,sommet = q.get()
		# 	print(sommet,deg)
		# 	print("size",q.qsize())
		# 	if deg < k:
		# 		if deg_objetc.marked[sommet]==True:
		# 			deg_objetc.mark(sommet)
		# 	else :
		# 		print("test",q.qsize())
		# 		b = False
		# b = True
		# if not np.any(deg_objetc.marked) :
		# 	print (k)
		# 	return k
	return k

if __name__ == "__main__":
	
	algo = sys.argv[1]
	filename = sys.argv[2]
	nb_arc = int(sys.argv[3])
	if (len(sys.argv) == 5):
		sommet = int(sys.argv[4])

	edg = read_edges(filename, nb_arc)
	g = Graph(edg, symmetrize=True)
	voisins_sommet = np.zeros(g.n, dtype = bool)
	
	if algo == "triangles":
		print(nb_triangle(g,voisins_sommet,sommet))

	elif algo == "clust":
		print(clus(g,voisins_sommet))

	elif algo == "k-coeur":
		k_coeur(g)

	else:
		print("algo inconnu")
	# #tableau numpy de taille nbr_sommets True ==> voisin de sommet
	# voisins_sommet = np.zeros(g.n, dtype = bool)
	# vertex_visited = np.full((g.n),False)
	# par_tri = np.full((g.n),0)
	# #k_coeur(g)

	# #on passe ce tableau à notre fonction
	
	# #print(nb_triangle(g,voisins_sommet, sommet))
	# start_time = time.time()
	# clust(g, voisins_sommet)
	# print("--- %s seconds ---" % (time.time() - start_time))

	# ## algorithme k_coeur



