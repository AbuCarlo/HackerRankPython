# No machine should be able to reach another machine.
# This turns out to be a shortest-paths problem:
# we need to determine the shortest paths from a 
# given machine to every other, and eliminate the 
# the lowest-cost edge on each path. If a machine
# is connected to two other machines, let's say, 
# it won't suffice to eliminate an edge shared 
# by both the respective paths, since those two 
# machines would still be connected to each other.

from collections import defaultdict
import heapq
import sys
import time


class Graph:
    def __init__(self, cities):
        self.order = max(max([e[0] for e in cities]), max([e[1] for e in cities])) + 1
        self.adjacency = defaultdict(lambda: {})
        for (u, v, cost) in cities:
            self.connect(u, v, cost)

    def connect(self, u, v, cost):
        self.adjacency[u][v] = cost
        self.adjacency[v][u] = cost
        
    def disconnect(self, u, v):
        del self.adjacency[v][u]
        del self.adjacency[u][v]
        
    def find_shortest_paths(self, source, targets):
        queue = []
        distances = defaultdict(lambda: sys.maxsize)
        previous = {}
        visited = set()

        found = []
        
        distances[source] = 0
        heapq.heappush(queue, (0, source))

        while queue:
            d, u = heapq.heappop(queue)
            if u in targets:
                found.append(u)
                # A path from source can't go through a city
                # to another city; the first part of the path
                # will be broken.
                visited.add(u)
                continue
            for v in self.adjacency[u]:
                if v in visited:
                    continue
                alt = d + self.adjacency[u][v]
                if distances[v] > alt:
                    distances[v] = alt
                    previous[v] = u
                heapq.heappush(queue, (distances[v], v))
                
            visited.add(u)

        paths = []
        for target in found:
            v = target
            path = []
            while v != source:
                path.append(v)
                v = previous[v]
            path.append(source)
            path.reverse()
            paths.append(path)
            
        return paths
    
def minTime(roads, machines) -> int:
    graph = Graph(roads)
    result = 0
    # It's not clear that this is an optimization.
    edges_removed = 0
    targets = set(machines)
    for machine in machines:
        targets.remove(machine)
        paths = graph.find_shortest_paths(machine, targets)
        cheapest_edges = set()
        for path in paths:
            # What is the lowest-cost edge on this path?
            edges = [(path[i - 1], path[i]) for i in range(1, len(path))]
            cheapest = min(edges, key = lambda e: graph.adjacency[e[0]][e[1]])
            cheapest_edges.add(cheapest if cheapest[0] < cheapest[1] else (cheapest[1], cheapest[0]))
        costs = [graph.adjacency[u][v] for u, v in cheapest_edges]
        result += sum(costs)
        edges_removed += len(cheapest_edges)
        if edges_removed == len(machines) - 1:
            break
        for u, v in cheapest_edges:
            graph.disconnect(u, v)
            
    return result

def load(file):
    with open(file, "r") as f:
        first_multiple_input = f.readline().rstrip().split()
        n = int(first_multiple_input[0])
        k = int(first_multiple_input[1])

        roads = []

        for _ in range(n - 1):
            line = f.readline()
            roads.append(list(map(int, line.rstrip().split())))

        machines = []

        for _ in range(k):
            line = f.readline()
            machines_item = int(line.strip())
            machines.append(machines_item)
            
        return roads, machines

# Sample 0 / Test Case 0
result0 = minTime([[2, 1, 8], [1, 0, 5], [2, 4, 5], [1, 3, 4]], [2, 4, 0])
# Sample 1
result1 = minTime([[0, 1, 4], [1, 2, 3], [1, 3, 7], [0, 4, 2]], [2, 3, 4])
# Sample 2
result2 = minTime([[0, 3, 3], [1, 4, 4], [1, 3, 4], [0, 2, 5]], [1, 3, 4])

print(result0, result1, result2)
# 6: 492394728
# 5: 28453895 @ 4s
# 8: 3105329 @ 210s
benchmark_graph, benchmark_machines = load('interviews/graphs/matrix-inputs/input05.txt')

time_start = time.perf_counter()
result = minTime(benchmark_graph, benchmark_machines)
time_end = time.perf_counter()
time_duration = time_end - time_start
print(f'Took {time_duration:.3f} seconds for result {result}')
