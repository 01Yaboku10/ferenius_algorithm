import math
import random
import heapq
import itertools
from linkedQFile import Linked_Q
from typing import Any,  Self
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import gui

class Node:
    def __init__(self, prefix: str | int, edges: dict[str, int] | None = None, xpos: int = 0, ypos: int = 0) -> None:
        self.prefix: str | int = prefix
        self.edges: dict[Self, int] = {}  # value is weight
        self._edges: dict[str, int] = edges if edges else {}
        self.visibility: int = 0
        self.xpos: int = xpos
        self.ypos: int = ypos

        self.distance = 0
        self.predecessor = None

        self.found = False

    def child_add(self, child: Self, weight: int = 0):
        self.edges[child] = weight

    def __str__(self) -> str:
        return f"{self.prefix}"
    
    def __repr__(self) -> str:
        return f"{self.prefix}"
    
    def __lt__(self, other):
        return self.distance < other.distance

class Graph():
    def __init__(self) -> None:
        self.root: Node | None = None
        self.nodes: dict[str, Node] = {}  # key is prefix

    def __contains__(self, value) -> bool:
        return value in self.nodes
    
    def node_add(self, key: str, edges: dict[str, int] | None = None, xpos: int = 0, ypos: int = 0):
        new_node: Node = Node(key, edges, xpos, ypos)
        self.nodes[key] = new_node
        if self.root is None:
            self.root = new_node

    def edge_add(self, from_node: str, to_node: str, weight: int = 0):
        if from_node not in self.nodes:
            self.node_add(from_node)
        if to_node not in self.nodes:
            self.node_add(to_node)
        self.nodes[from_node].child_add(self.nodes[to_node], weight)
    
    def add_children(self, c_weight: tuple[int, int] = (0, 0), weight_mode="d"):
        for node in self.nodes.values():
            for edge, weight in node._edges.items():
                child_node: Node = self.node_get(str(edge))
                if weight == 0:
                    a_edge = node.edges.get(edge)
                    if a_edge:
                        continue
                    if weight_mode == "d":
                        weight = math.sqrt((node.xpos-child_node.xpos)**2 + (node.ypos-child_node.ypos)**2)
                    else:
                        weight = random.randint(c_weight[0], c_weight[1])
                node.child_add(child_node, weight)
                child_node.child_add(node, weight)

    def node_get(self, key: str):
        node = self.nodes.get(key)
        if node is None: print(f"ERROR: Node with name '{key}' not found. Type:{type(key)}")
        return node
    
    def node_reset(self):
        for node in self.nodes.values():
            node.distance = math.inf
            node.predecessor = None
            node.visibility = 0

    def bfs(self, from_vert: Node, to_vert: Node):
        self.node_reset()
        queue: Linked_Q = Linked_Q()
        queue.enqueue(from_vert)
        while queue.size > 0:
            current_vert: Node = queue.dequeue()
            #print(current_vert)
            for nbr in current_vert.edges.keys():
                #print(nbr)
                if nbr.visibility == 0:  # Skip if already explored
                    nbr.visibility = 1
                    nbr.distance = current_vert.distance + 1
                    nbr.predecessor = current_vert
                    queue.enqueue(nbr)
                    if nbr == to_vert:
                        queue.size = 0
                        break
            current_vert.visibility = 2
        if to_vert.predecessor is None:  # Check if the Vertex was reached
            print(f"No Path could be found between '{from_vert.prefix}' to '{to_vert.prefix}'")
        else:
            return self.traverse(to_vert)

    def dijkstra(self, start: Node, target: Node, mode="d", record=False):
        self.node_reset()
        distances = {node: float("inf") for node in self.nodes.values()}
        distances[start] = 0
        previous_nodes = {node: None for node in self.nodes.values()}
        pq = [(0, start)] # (distance, node)
        best_dist = float("inf")

        frames = []
        visited = set()
        if mode == "7" and record:
            print(f"Creating search for... {target}")

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            # Skip if better path has already been found
            if current_dist > distances[current_node]:
                continue

            visited.add(current_node)
            
            if record:
                frames.append({
                    "current": current_node,
                    "visited": visited.copy(),
                    "distances": distances.copy()
                })

            for nbr, weight in current_node.edges.items():
                distance = current_dist + weight
                if distance < distances[nbr]:
                    distances[nbr] = distance
                    previous_nodes[nbr] = current_node
                    if mode == "7":
                        if current_dist <= best_dist:
                            if current_node == target:
                                if current_dist < best_dist:
                                    best_dist = current_dist
                            heapq.heappush(pq, (distance, nbr))
                    else:
                        heapq.heappush(pq, (distance, nbr))
        #return distances, previous_nodes
        if mode == "d":
            return (self.traverse_dji(previous_nodes, start, target), frames)
        elif mode == "7":
            return (self.traverse_dji(previous_nodes, start, target), frames)
        else:
            return (self.traverse_dji(previous_nodes, start, target), frames)
    
    def ferenius(self, start: Node, targets: list[Node], version: int = 1):
        def sweep(nodes, start, axis):
            if axis == "x":
                get_primary = lambda n: n.xpos
                get_secondary = lambda n: n.ypos
            else:
                get_primary = lambda n: n.ypos
                get_secondary = lambda n: n.xpos

            remaining = [n for n in nodes if n != start]
            start_value = get_primary(start)

            if version == 3 or version == 6 or version == 7:
                # Get forward direction
                furthest_p = max(remaining, key=get_primary)
                furthest_n = min(remaining, key=get_primary)
                dist_p = distance(start, furthest_p)
                dist_n = distance(start, furthest_n)

            # Split nodes relative to start
            forward = []
            backward = []
            if version == 3 or version == 6 or version == 7 and dist_n < dist_p:
                for n in remaining:
                    if get_primary(n) <= start_value:
                        forward.append(n)
                    else:
                        backward.append(n)
            else:
                for n in remaining:
                    if get_primary(n) >= start_value:
                        forward.append(n)
                    else:
                        backward.append(n)

            # Sort outward from start
            forward.sort(key=get_primary)
            backward.sort(key=get_primary, reverse=True)

            # Within each side, sort by secondary axis
            forward.sort(key=get_secondary)
            backward.sort(key=get_secondary)

            return [start] + forward + backward
        def two_opt(route):

            best = route[:]
            n = len(best)
            improved = True
            iters = 0

            while improved:
                improved = False

                for i in range(1, n - 2):  # keep start fixed
                    for j in range(i + 1, n - 1):

                        if j - i == 1:
                            continue  # skip adjacent edges

                        a, b = best[i - 1], best[i]
                        c, d = best[j], best[j + 1]

                        delta = (
                            distance(a, c) + distance(b, d)
                            - distance(a, b) - distance(c, d)
                        )

                        iters += 1

                        if delta < 0:
                            best[i:j+1] = reversed(best[i:j+1])
                            improved = True
                            break

                    if improved:
                        break
                if iters > 1000000:
                    break

            return best
        def path_length(order):
            return sum(distance(order[i], order[i+1]) for i in range(len(order) - 1))
        def distance(a, b):
            return math.hypot(a.xpos - b.xpos, a.ypos - b.ypos)
        start = targets[0]

        order_x = sweep(targets, start, "x")
        order_y = sweep(targets, start, "y")

        if version == 1:
            result = min([order_x, order_y], key=path_length)
            sec_result = two_opt(result)

            return sec_result, "x" if result == order_x else "y"
        else:
            return two_opt(order_x), two_opt(order_y)
    
    def dials(self, start: Node, target: Node):
        pass

    def traverse(self, vertex: Node):
        path = []
        weight = 0
        current_vert = vertex
        while current_vert:  # Stops when None
            path.append(current_vert)
            previous_vert = current_vert
            current_vert = current_vert.predecessor
            if current_vert is None:
                break
            weight += previous_vert.edges[current_vert]
        return(path, weight)
    
    def traverse_dji(self, previous_nodes, start, target):
        path = []
        current = target
        distance = 0

        while current is not None:
            path.append(current)
            prev = previous_nodes[current]
            if prev:
                distance += current.edges[prev]
            current = prev

        path.reverse()

        # If start is not first, no path exists
        if path[0] != start:
            print(f"OBS! No path exists between {start} and {target}")
            return None

        return path, distance

    def create_route(self, nodes: list[Node], version=1, record=False):
        route = []
        target_nodes = Linked_Q()
        distance = 0
        for node in nodes:
            target_nodes.enqueue(node)
        while target_nodes.size > 1:
            start = target_nodes.dequeue()
            end = target_nodes.peek()
            dji_out, frames = self.dijkstra(start, end, f"{version}", record=False)
            local_route, dist = dji_out
            if record:
                gui.update_dji(self, frames)

            if version != "brute":
                # If a target node is found along the route, remove it from the visit list
                new_local = []
                new_dist = dist
                for i, n in enumerate(local_route):
                    new_local.append(n)
                    if n in nodes:
                        n.found = True
                    if n in nodes and n != start and n != end:
                        target_nodes.remove(n)

                    # Check nbrs if version 4, and add a shortcut to the nbr if it's on the visit list
                    # and remove the nbr from the visit list.
                    if version == 4:
                        for nbr, weight in n.edges.items():
                            if nbr in nodes and nbr != start and nbr != end and not nbr.found:
                                try:
                                    if nbr == local_route[i+1] or nbr == local_route[i-1]:
                                        continue
                                    nbr.found = True
                                    new_local.append(nbr)
                                    new_local.append(n)
                                    new_dist += weight*2
                                    target_nodes.remove(nbr)
                                except IndexError:
                                    continue
            else:
                new_local = local_route
                new_dist = dist

            route += new_local
            distance += new_dist
        for node in route:
            node.found = False
        
        return route, distance
    
    def nn(self, start: Node, targets: list[Node]):
        def find_nn(graph: Graph, _start: Node, _targets):
            graph.node_reset()
            distances = {node: float("inf") for node in graph.nodes.values()}
            distances[_start] = 0
            previous_nodes = {node: None for node in graph.nodes.values()}
            pq = [(0, _start)] # (distance, node)

            while pq:
                current_dist, current_node = heapq.heappop(pq)

                # Skip if better path has already been found
                if current_dist > distances[current_node]:
                    continue

                for nbr, weight in current_node.edges.items():
                    if current_node in _targets and current_node != _start:
                        target = current_node
                        return self.traverse_dji(previous_nodes, _start, target)
                    distance = current_dist + weight
                    if distance < distances[nbr]:
                        distances[nbr] = distance
                        previous_nodes[nbr] = current_node
                        heapq.heappush(pq, (distance, nbr))
        
        targets_left = targets[1:]
        route = []
        dist = 0
        _starting = start
        while targets_left:
            nearst_nbr, nbr_dist = find_nn(self, _starting, targets_left)
            route += nearst_nbr
            dist += nbr_dist
            _starting = nearst_nbr[-1]
            targets_left.remove(nearst_nbr[-1])
        return route, dist

    def brute(self, start: Node, targets: list[Node]):
        """'Targets' cannot contain 'start'"""
        target_perms: list[tuple[Node]] = list(itertools.permutations(targets))
        target_dist = {perm: None for perm in target_perms}
        for perm in tqdm(target_perms, desc="Evaluating permutations..."):
            target_nodes = [start] + [node for node in perm]
            target_dist[perm] = self.create_route(target_nodes, "brute")
        lowest = math.inf
        fastest_route = None
        fastest_perm = None
        for perm, (route, distance) in tqdm(target_dist.items(), desc="Getting fastest permutation..."):
            if distance < lowest:
                fastest_route = route
                lowest = distance
                fastest_perm = perm
        return fastest_route, lowest, fastest_perm
    
    def multi_brute(self, start: Node, targets: list[Node]):
        perms = itertools.permutations(targets[:-1])

        args = ((self, start, perm) for perm in perms)

        best_distance = math.inf
        best_route = None
        best_perm = None

        with Pool(cpu_count()) as pool:
            results = pool.imap_unordered(evaluate_perm, args, chunksize=1000)
            for perm, route, distance in tqdm(results, desc="Evaluating permutations"):
                if distance < best_distance:
                    best_distance = distance
                    best_route = route
                    best_perm = perm

        return best_route, best_distance, best_perm
    
    def sep_two_opt(self, start: Node, targets: list[Node]):
        def distance(a, b):
            return math.hypot(a.xpos - b.xpos, a.ypos - b.ypos)
        route = targets[:-1]
        #route.insert(0, start)
        best = route[:]
        n = len(best)
        improved = True
        iters = 0

        while improved:
            improved = False

            for i in range(1, n - 2):  # keep start fixed
                for j in range(i + 1, n - 1):

                    if j - i == 1:
                        continue  # skip adjacent edges

                    a, b = best[i - 1], best[i]
                    c, d = best[j], best[j + 1]

                    delta = (
                        distance(a, c) + distance(b, d)
                        - distance(a, b) - distance(c, d)
                    )

                    iters += 1

                    if delta < 0:
                        best[i:j+1] = reversed(best[i:j+1])
                        improved = True
                        break

                if improved:
                    break
            if iters > 1000000:
                break

        return best
def evaluate_perm(args):
    solver, start, perm = args
    target_nodes = [start] + list(perm)
    route, distance = solver.create_route(target_nodes, "brute")
    return perm, route, distance