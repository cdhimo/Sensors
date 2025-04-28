# MA214 Assessed Coursework 2025

# Candidate Number: PUT YOUR CANDIDATE NUMBER HERE

from collections import deque
from math import sqrt

'''
Data Structures:
-----------------------
self.V (list of vertices):
- Stores all sensor objects. This list models the graph’s vertices and is used in Kruskal’s algorithm for 
Minimum Spanning Tree (MST) construction.

self.Adj (list of deques):
- Stores adjacency lists for each sensor. Each deque contains pairs (neighbor_sensor, distance), allowing efficient 
storage and lookup of neighboring connections during MST setup.

self.b (dictionary):
- Stores the backbone (the MST). Each sensor maps to a list of neighboring sensors with their corresponding edge weights. 
This allows for fast traversal when building communication chains.

Union-Find Structure (list):
- Used in Kruskal’s algorithm to efficiently check whether adding an edge would create a cycle. This ensures the backbone 
remains a valid tree (acyclic).

Algorithms:
-----------------------
Kruskal’s Algorithm (MSTKruskal):
- Constructs the communication backbone (MST) ensuring minimal total distance between all sensors. Sorts edges by weight 
and uses Union-Find to avoid cycles.

Breadth-First Search (BFS):
- Traverses the backbone to find the unique communication chain and communication distance between two sensors by following 
parent pointers.

Auxiliary Classes and Functions:
---------------------------------------
eucl_dist:
- Calculates the Euclidean distance between two sensors. Used when building the adjacency list, when sorting edges for 
Kruskal’s algorithm, and when computing distances during BFS traversal.

Class SensorStorage:
- Models the sensor network as a complete weighted graph. Stores the list of sensors (`self.V`) and adjacency lists (`self.Adj`).
- Contains the AdjList() function which uses a double for loop to connect all pairs of sensors with their Euclidean distances.

collect_edges, make_sets, find_set, union:
- Helper functions used to set up Kruskal’s algorithm. collect_edges gathers edges; make_sets initializes disjoint sets; 
find_set and union manage the Union-Find structure.

Class Backbone:
- Stores the MST as a dictionary mapping each sensor to its connected neighbors and edge weights.
- Used to efficiently perform BFS traversals to find communication chains.

build_chain function:
- Reconstructs the communication chain between two sensors by calling BFS first and then following parent pointers 
backward from the destination sensor to the source.

Class Sensor:
- Represents a sensor with (x, y) coordinates.
- Also stores properties (`id`, `color`, `d`, `pi`) needed for BFS and Kruskal’s algorithm.

Class SensorCollection:
- Organizes the entire sensor network.
- self.storage: Creates a SensorStorage object from a list of sensors.
- self.MST: Builds the MST using Kruskal’s algorithm.
- self.backbone: Stores the MST in a Backbone structure for fast traversal.

def communicate:
- Calls build_chain using the backbone and given sensors.
- Returns the chain (list of sensors) representing the communication path.

def cdist:
- Calls BFS on the backbone to traverse from one sensor to another.
- Returns the total communication distance from sensor1 to sensor2, stored in sensor1.d after traversal.

'''


def eucl_dist(sensor1, sensor2): # function calculates the euclidian distance, easy to use for future parts of the algorithm
    w = sqrt((sensor2.x - sensor1.x) ** 2 + (sensor2.y - sensor1.y) ** 2)
    return w

class SensorStorage:
    def __init__(self, sensor_list):
        self.n = len(sensor_list) # number of sensors
        self.V = [sensor for sensor in sensor_list] # Vertices
        self.Adj = [deque() for _ in range(self.n)] # adj list (connected edges)
        for i in range(self.n):
            self.V[i].id = i #keeps track of original sensor order
        self.AdjList()

    def AdjList(self):  # Adjacency list function to store each connected sensors returns the adj list
        for i in range(self.n):
            sensor1 = self.V[i]
            for j in range(i + 1, self.n):
                sensor2 = self.V[j]
                w = eucl_dist(sensor1, sensor2)  # calculates the euclidian distance between the two sensors
                self.Adj[i].append((sensor2, w))
                self.Adj[j].append((sensor1, w))
        return self.Adj


'''
Functions for the set-up of Kruskals
'''
def make_sets(n):
    return [i for i in range(0, n)]

def find_set(S, v):
    i = v.id
    while S[i] != i:
        i = S[i]
    return i

def union(S, u, v):
    urep = find_set(S, u)
    vrep = find_set(S, v)
    S[vrep] = urep

def collect_edges(G):
    edges = []
    for u in G.V:
        for v, w in G.Adj[u.id]:
            # in order to avoid duplicating edges
            if u.id < v.id:
                edges.append((u, v, w))
    return edges

def MSTKruskal(G):
    A = []
    S = make_sets(len(G.V))
    E = collect_edges(G)
    E.sort(key=lambda tup: tup[2])
    for u, v, w in E:
        if find_set(S, u) != find_set(S, v):
            A.append((u, v, w))
            union(S, u, v)
    return A


'''
Backbone Structure using Hashmap
'''
class Backbone:
    def __init__(self, MST):
        self.b = {}
        for u, v, w in MST:
            if u not in self.b:
                self.b[u] = []
            if v not in self.b:
                self.b[v] = []
            self.b[u].append((v, w))
            self.b[v].append((u, w))

'''
Breadth First Search implemented with backbone structure
'''

def BFS(backbone,s):
    # reset colors to white
    for u in backbone.b:
        u.color = "white"
        u.pi = None
    s.color = "gray"
    s.d = 0
    s.pi = None
    Q = deque()
    Q.append(s)
    while Q:
        u = Q.popleft()
        for v in backbone.b[u]:
            v = v[0]
            if v.color == "white":
                v.color = "gray"
                v.d = u.d + eucl_dist(u, v)
                v.pi = u
                Q.append(v)
        u.color = "black"

'''
Function to display communication chain used in def communicate
'''

def build_chain(backbone,sensor1,sensor2,chain):
    BFS(backbone, sensor2)
    end = sensor2
    start = sensor1
    while start != end:
        chain.append(start)
        start = start.pi
    chain.append(start)
    return chain


# Implement the class Sensor here. (See Task 1.)
class Sensor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None  # ID is needed for Kruskals algorithm - id is set during the sensor storage portion
        self.color = None
        self.d = None
        self.pi = None

    def __repr__(self):
        return f"({str(self.x)},{str(self.y)})"


class SensorCollection:

    def __init__(self, sensor_list):
        self.storage = SensorStorage(sensor_list)
        self.MST = MSTKruskal(self.storage)
        self.backbone = Backbone(self.MST)

    def communicate(self, sensor1, sensor2):
        self.chain = []
        build_chain(self.backbone,sensor1,sensor2,self.chain)
        return self.chain



    def cdist(self, sensor1, sensor2):
        BFS(self.backbone, sensor2)
        return sensor1.d


if __name__== '__main__':
    sensors = [Sensor(0,0),Sensor(0,1),Sensor(0,2),Sensor(1,0),Sensor(1,1),Sensor(1,2),Sensor(2,0),Sensor(2,1),Sensor(2,2)] 
    collection = SensorCollection(sensors)
    print( "Example 1:" )
    print( "==========" )
    print( "Sensors:" + str(sensors) )
    for i,j in [(0,8),(6,1),(7,8),(8,6)]:
        print( "From sensor number " + str(i) + " to sensor number " + str(j) + ":")
        print( "   " + str( collection.communicate(sensors[i],sensors[j]) ) )
        print( "   Distance : " + str( collection.cdist(sensors[i],sensors[j]) ) )
    print()

    sensors = [Sensor(0,0),Sensor(2,5),Sensor(1,0),Sensor(3.5,1)] 
    collection = SensorCollection(sensors)
    print( "Example 2:" )
    print( "==========" )
    print( "Sensors:" + str(sensors) )
    for i,j in [(0,3),(3,1),(2,3)]:
        print( "From sensor number " + str(i) + " to sensor number " + str(j) + ":")
        print( "   " + str( collection.communicate(sensors[i],sensors[j]) ) )
        print( "   Distance : " + str( collection.cdist(sensors[i],sensors[j]) ) )
    print()


'''
Answers to Task 3:
(a)
ADD YOUR ANSWER HERE.
(b)
ADD YOUR ANSWER HERE.
'''

'''
Resources (other than lecture resources) used:
LIST USED RESOURCES HERE.
'''






