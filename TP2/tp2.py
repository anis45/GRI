import numpy as np
import collections

import sys, os, psutil

def mem() :
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss / 1000000, "Mb", file=sys.stderr)

def read_edges(fname, m_estim, delim='\t') :
    edg = np.zeros((m_estim, 2), dtype='int32')
    count = 0
    with open(fname) as fp: 
        while count < m_estim : 
            line = fp.readline()   
            if not line: break
            if line[0] == '#': continue
            su, sv = line.split(delim)
            edg[count][0] = int(su)
            edg[count][1] = int(sv)
            count += 1
    return edg[:count,:]


class Graph:

    # Natural code but python is so slow (few minutes for big graphs).
    # We could use numpy functions to go faster, but it becomes cryptic.
    def __init__(self, edg, symmetrize=False) :
        self.m = len(edg)
        # the maximum vertex number is n - 1, hence:
        self.n = edg.max() + 1
        # compute degrees:
        deg = np.zeros(self.n, dtype='int32')
        for i in range(len(edg)) :
            deg[edg[i, 0]] += 1
            if symmetrize : deg[edg[i, 1]] += 1
        # offset[u] will be the position of the first neighbor of u in adj
        self.offset = np.zeros(self.n + 1, dtype='int32')
        for u in range(self.n) :
            self.offset[u+1] = self.offset[u] + deg[u]
            deg[u] = 0 # re-use it as index of N(u)
        # all adjacency lists concatenated:
        self.adj = np.zeros(self.offset[self.n], dtype='int32')
        for i in range(len(edg)) :
            u = edg[i,0] ; v = edg[i,1]
            self.adj[self.offset[u] + deg[u]] = v ; deg[u] += 1
            if symmetrize :
                self.adj[self.offset[v] + deg[v]] = u ; deg[v] += 1

    def neighbors(self, u) :
        return self.adj[self.offset[u]:self.offset[u+1]]
    
    def nodes(self) :
        return range(0, self.n)

    def reverse(self) :
        pass
        

class Traversal:

    infinity = -1

    def __init__(self, n) :
        self.queue = collections.deque()
        self.dist = np.full((n), self.infinity)
        self.pere = np.full((n), self.infinity)

    def clear(self) :
        self.queue.clear()
        self.dist.fill(self.infinity)
        self.pere.fill(self.infinity)

    def bfs(self, g, src) :
        assert g.n <= len(self.dist)
        self.clear();
        # start from src:
        self.dist[src] = 0
        self.pere[src] = -1
        self.queue.append(src)
        #
        while self.queue : # not empty
            u = self.queue.popleft()
            du = self.dist[u]
           # if du > 3 : break # !!!!
            for v in g.neighbors(u) :
                if self.dist[v] == self.infinity :
                	self.pere[v] = u 
                	self.dist[v] = du + 1
                	self.queue.append(v)

def double_BFS(trav, src):
	trav.clear()
	trav.bfs(g, src)
	v = np.argmax(trav.dist)
	print("v=", v)
	trav.clear()
	trav.bfs(g, v)
	d = np.amax(trav.dist)
	w = np.argmax(trav.dist)
	print("w=", w)
	print("diam>=", d)

	return (w, d)

def double_double_BFS(trav, src):
    w, diam = double_BFS(trav, src)
    if diam % 2 == 0:#distance paire
        m =  my_path[diam/2]
        dist, d = double_BFS(trav, m)
        print ("diam>=",d)
    else:
    	i = 0
    	m1 = w
    	while i != (diam/2):
    		m1 = trav.pere[m1]
    		i += 1
    	m2 = trav.pere[m1]
    	print("diam>=",m1,m2)

def heuristique(trav, src):
	mydict = dict()
	sumdist = np.full(len(trav.dist), 0)
	m = src
	for i in range(4):
		trav.bfs(g, m)
		v = np.argmax(trav.dist)
		mydict[m] = trav.dist[v]
		sumdist = np.add(sumdist, trav.dist)
		m = np.argmax(sumdist)
	all_values = mydict.values()
	max_value = max(all_values)
	print("diam>=", max_value)

def connectedComponents(g,u):
    l = []
    visited = np.full(g.n,False)
    queue = collections.deque()
    queue.append(src)
    while queue : 
            u = queue.popleft()
            l.append(u)
            for v in g.neighbors(u) :
                if visited[v] == False :
                    queue.append(v)
                    visited[v]= True
    return l

def rec_sweep( trav,g, eccsup, diamlow, u,b):
    
    if eccsup[u] <= diamlow:
        return diamlow
    trav.bfs(g,u)
    m = np.amax(trav.dist)
    if(m>diamlow):
        diamlow = m
    for key in b :
        b[key] = trav.dist[key] + m
        if b[key] < eccsup[key] :
            eccsup[key] = b[key]
    u = max(eccsup, key=eccsup.get)
    return rec_sweep(trav,g,eccsup,diamlow,u,b)

def TakesKosters(g,trav,src):
    l = connectedComponents(g,src)
    b ={}
    eccsup = {}
    for i in l:
        b[i] = 0
        eccsup[i] = 99999
    print("diam=",rec_sweep(trav,g,eccsup,0,src,b))









if __name__ == "__main__":
    fname = sys.argv[2]
    m_estim = int(sys.argv[3])#nbr aretes
    src = int(sys.argv[4])
    edg = read_edges(fname, m_estim)
    g = Graph(edg, symmetrize=True)
    trav = Traversal(g.n)
    heuristique(trav,src)
    double_BFS(trav, src)
    #double_double_BFS(trav, src)
    TakesKosters(g,trav,src)
