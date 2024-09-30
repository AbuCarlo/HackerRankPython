class Graph:
    def __init__(self, order):
        self.adjacency = [None] * order

    def connect(self, u, v):
        if self.adjacency[u] is None:
            self.adjacency[u] = set()
        if self.adjacency[v] is None:
            self.adjacency[v] = set()
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        
    def find_all_distances(self, source):
        import collections
        queue = collections.deque()
        distances = {}
        visited = set()
        distances[source] = 0
        queue.append(source)
        while queue:
            u = queue.popleft()
            if u in visited:
                continue
            if self.adjacency[u] is None:
                continue
            for v in self.adjacency[u]:
                if v in visited:
                    continue
                queue.append(v)
                alt = distances[u] + 1
                if v not in distances:
                    distances[v] = alt
                elif alt < distances[v]:
                    distances[v] = alt
                
            visited.add(u)
            
        reaches = [distances.get(v, None) for v in range(len(self.adjacency)) if v != source]
        answer = [r * 6 if r is not None else -1 for r in reaches]
        print(*answer)
        

import sys
sys.stdin = open("shortest-reach-inputs/sample.txt", "r")

t = int(input())

for i in range(t):
    n,m = [int(value) for value in input().split()]
    graph = Graph(n)
    for i in range(m):
        x,y = [int(x) for x in input().split()]
        graph.connect(x-1,y-1) 
    s = int(input())
    graph.find_all_distances(s-1)
