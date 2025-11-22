# AVL Tree for City Zone Indexing
class ZoneNode:
    def __init__(self, zone_id, name, details):
        self.zone_id = zone_id
        self.name = name
        self.details = details
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, node):
        if not root:
            return node
        if node.zone_id < root.zone_id:
            root.left = self.insert(root.left, node)
        else:
            root.right = self.insert(root.right, node)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Rotations
        if balance > 1 and node.zone_id < root.left.zone_id:
            return self.right_rotate(root)
        if balance < -1 and node.zone_id > root.right.zone_id:
            return self.left_rotate(root)
        if balance > 1 and node.zone_id > root.left.zone_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and node.zone_id < root.right.zone_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(f"ZoneID: {root.zone_id}, Name: {root.name}, Details: {root.details}")
            self.inorder(root.right)

# Graph for Road Networks
import heapq

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    # Dijkstra Algorithm
    def dijkstra(self, start):
        dist = [float('inf')] * self.V
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self.graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    # Floyd-Warshall Algorithm
    def floyd_warshall(self):
        dist = [[float('inf')]*self.V for _ in range(self.V)]
        for u in range(self.V):
            dist[u][u] = 0
            for v, w in self.graph[u]:
                dist[u][v] = w
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    # Kruskal's MST
    def kruskal(self):
        parent = [i for i in range(self.V)]
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            parent[find(u)] = find(v)
        edges = []
        for u in range(self.V):
            for v, w in self.graph[u]:
                if u < v:
                    edges.append((w, u, v))
        edges.sort()
        mst = []
        for w, u, v in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, w))
        return mst

# Example Usage
if __name__ == "__main__":
    # AVL Tree for Zones
    avl = AVLTree()
    root_zone = None
    root_zone = avl.insert(root_zone, ZoneNode(1, "Residential Area", "North City"))
    root_zone = avl.insert(root_zone, ZoneNode(2, "Commercial Area", "Central City"))
    root_zone = avl.insert(root_zone, ZoneNode(3, "Industrial Zone", "South City"))
    print("City Zones (Inorder Traversal):")
    avl.inorder(root_zone)

    # Graph for Roads
    g = Graph(4)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 8)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 3, 1)
    print("\nDijkstra from Node 0:", g.dijkstra(0))
    print("Floyd-Warshall Distance Matrix:")
    for row in g.floyd_warshall():
        print(row)
    print("Minimum Spanning Tree (Kruskal):", g.kruskal())
