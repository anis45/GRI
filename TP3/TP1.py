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
        self.deg = np.zeros(self.n, dtype='int32')
        for i in range(len(edg)) :
            self.deg[edg[i, 0]] += 1
            if symmetrize : self.deg[edg[i, 1]] += 1
        # offset[u] will be the position of the first neighbor of u in adj
        self.offset = np.zeros(self.n + 1, dtype='int32')
        for u in range(self.n) :
            self.offset[u+1] = self.offset[u] + self.deg[u]
            self.deg[u] = 0 # re-use it as index of N(u)
        # all adjacency lists concatenated:
        self.adj = np.zeros(self.offset[self.n], dtype='int32')
        for i in range(len(edg)) :
            u = edg[i,0] ; v = edg[i,1]
            self.adj[self.offset[u] + self.deg[u]] = v ; self.deg[u] += 1
            if symmetrize :
                self.adj[self.offset[v] + self.deg[v]] = u ; self.deg[v] += 1

    def neighbors(self, u) :
        return self.adj[self.offset[u]:self.offset[u+1]]
    
    def nodes(self) :
        return range(0, self.n)

    def reverse(self) :
        pass
        

class Traversal:

    infinity = np.iinfo(np.int32).max

    def __init__(self, n) :
        self.queue = collections.deque()
        self.dist = np.full((n), self.infinity)

    def clear(self) :
        self.queue.clear()
        self.dist.fill(self.infinity)

    def bfs(self, g, src) :
        assert g.n <= len(self.dist)
        self.clear();
        # start from src:
        self.dist[src] = 0
        self.queue.append(src)
        #
        while self.queue : # not empty
            u = self.queue.popleft()
            du = self.dist[u]
            if du > 3 : break # !!!!
            for v in g.neighbors(u) :
                if self.dist[v] == self.infinity :
                    self.dist[v] = du + 1
                    self.queue.append(v)
        
    
if __name__ == "__main__":
    fname = sys.argv[1]
    m_estim = int(sys.argv[2])
    mem()
    edg = read_edges(fname, m_estim)
    mem()
    g = Graph(edg, symmetrize=True)
    print(f"n={g.n}")
    print(f"m={g.m}")
    mem()
    degmax = 0
    for u in g.nodes() :
        du = len(g.neighbors(u))
        if du > degmax :
            degmax = du
    print(f"degmax={degmax}")
    mem()
    trav = Traversal(g.n)
    src = int(sys.argv[3])
    dst = int(sys.argv[4])
    for i in range(1) : trav.bfs(g, src+i) # 10s per BFS on soc-pokec
    print(f"dist={trav.dist[dst]}")
    mem()
