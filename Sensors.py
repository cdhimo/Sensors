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
    w = sqrt((sensor2.x - sensor1.x) ** 2 + (sensor2.y - sensor1.y) ** 2) #formula for euclidian distance
    return w

class SensorStorage:
    def __init__(self, sensor_list):
        # stores number of sensors
        self.n = len(sensor_list)
        # list of all sensor objects (vertices in the graph)
        self.V = [sensor for sensor in sensor_list]
        # Initialize an adjacency list: one deque per sensor to store (neighbor, distance) pairs
        self.Adj = [deque() for _ in range(self.n)]

        # Assign a unique ID to each sensor (needed for graph algorithms like Kruskal's and BFS)
        for i in range(self.n):
            self.V[i].id = i
        # Build the adjacency list by connecting all pairs of sensors with Euclidean distance
        self.AdjList()

    def AdjList(self):
        """
        Constructs the adjacency list for the complete sensor graph.
        Each sensor is connected to every other sensor, and the edge weight is the Euclidean distance between them.
        """
        # Adjacency list function to store each connected sensors returns the adj list
        for i in range(self.n):
            sensor1 = self.V[i]
            for j in range(i + 1, self.n):
                sensor2 = self.V[j]
                # Calculate the Euclidean distance between sensor1 and sensor2
                w = eucl_dist(sensor1, sensor2)
                # Add the connection to both sensors' adjacency lists (undirected graph)
                self.Adj[i].append((sensor2, w))
                self.Adj[j].append((sensor1, w))
        # Return the completed adjacency list
        return self.Adj


'''
Functions for the set-up of Kruskals
'''
#makes singletons for each set
def make_sets(n):
    return [i for i in range(0, n)]

# Finds the set that vertex v is an element of
# each set is represented by u.id for some vertex u in it
def find_set(S, v):
    i = v.id
    while S[i] != i:
        i = S[i]
    return i

# Unites the sets that includes u and v by linking representative
# of one of the sets to the representative of the other
def union(S, u, v):
    urep = find_set(S, u)
    vrep = find_set(S, v)
    S[vrep] = urep

# Collect edges of input graph G into a list
# Entry (u,v,w) corresponds to an edge (u,v) with weight w
def collect_edges(G):
    edges = []
    for u in G.V:
        for v, w in G.Adj[u.id]:
            # in order to avoid duplicating edges
            if u.id < v.id:
                edges.append((u, v, w))
    return edges

def MSTKruskal(G):
    A = [] # List to store the edges of the MST

    # Initialize the Union-Find structure: initially, each sensor is its own set
    S = make_sets(len(G.V))

    # Collect all edges from the graph
    E = collect_edges(G)

    # Sort the edges by ascending weight (smallest distance first)
    E.sort(key=lambda tup: tup[2])

    # Process edges in order of increasing weight
    for u, v, w in E:
        # If u and v are in different sets (no cycle would be formed)
        if find_set(S, u) != find_set(S, v):
            A.append((u, v, w)) # Add edge to MST
            union(S, u, v) # Merge the sets of u and v
    # Return the list of MST edges
    return A


'''
Backbone Structure using Hashmap
'''
class Backbone:
    def __init__(self, MST):
        self.b = {} #creates an empty dictionary
        for u, v, w in MST:
            #ensures u is in the dictionary
            if u not in self.b:
                self.b[u] = []
            #ensures v is in the dictionary
            if v not in self.b:
                self.b[v] = []
            # Add the edge in both directions (since the MST is undirected)
            self.b[u].append((v, w))
            self.b[v].append((u, w))

'''
Breadth First Search implemented with backbone structure
'''

def BFS(backbone,s):
    # Reset all sensors' colors and parent pointers
    for u in backbone.b:
        u.color = "white" # White = unvisited
        u.pi = None       # No parent yet
    s.color = "gray" # grey = discovered
    s.d = 0 # distance from itself is zero
    s.pi = None #no parent
    Q = deque() #initialize a deque
    Q.append(s) #append s
    while Q:
        u = Q.popleft() # Visit the next sensor in the queue

        # Explore all neighbors of u in the backbone
        for v in backbone.b[u]:
            v = v[0] # Extract the neighbor sensor (v, w) → v
            if v.color == "white":
                v.color = "gray" # Mark as discovered
                v.d = u.d + eucl_dist(u, v)  # Update distance (add edge weight)
                v.pi = u # Set parent to u
                Q.append(v) # Enqueue v for further exploration
        # Mark u as fully explored
        u.color = "black"

'''
Function to display communication chain used in def communicate
'''

def build_chain(backbone,sensor1,sensor2,chain):
    BFS(backbone, sensor2) #finds a path to sensor 2
    end = sensor2
    start = sensor1
    while start != end: #iterate through unitl reaching sensor 2
        chain.append(start) #add each sensor that connects the start to the end
        start = start.pi # move onto the next
    chain.append(start) #append sensor 2
    return chain #return full chian


# Implement the class Sensor here. (See Task 1.)
class Sensor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None  # ID is needed for Kruskals algorithm - id is set during the sensor storage portion
        self.color = None # .color,.d,.pi are all needed for BFS
        self.d = None
        self.pi = None

    def __repr__(self):
        #use f string to return the sensor in designated format
        return f"({str(self.x)},{str(self.y)})"


class SensorCollection:

    def __init__(self, sensor_list):
        '''

        SensorStorage:
        Building the adjacency list takes O(n^2) time. This is because a double for-loop iterates through each pair of
        sensors exactly once to compute the Euclidean distance between them.

        Kruskal's Algorithm:
        Running Kruskal’s algorithm takes O(n^2 log n) time. Kruskal sorts all edges (O(E log E)), and since the graph is
        complete (every sensor can connect to every other sensor), we have E ≈ n² edges, leading to O(n² log n) complexity.

        Backbone Construction:
        Building the backbone takes O(n) time. We simply insert each MST edge into a dictionary where the number of
        sensors (nodes) is proportional to n

        Running time: O(n^2 log n)
        '''
        self.storage = SensorStorage(sensor_list) #builds complete sensor graph
        self.MST = MSTKruskal(self.storage) #runs kruskals to create MST
        self.backbone = Backbone(self.MST) #forms the backbone from MST

    def communicate(self, sensor1, sensor2):
        '''
        - The build_chain function internally runs BFS.
        - BFS on the backbone (a tree with n-1 edges) takes O(n) time because n + (n-1) = 2n = O(n).
        - Traversing the parent pointers to build the chain also takes at most O(n) time.

        Overall, the running time of communicate() is O(n).
        '''
        self.chain = [] #initializes and empty list
        build_chain(self.backbone,sensor1,sensor2,self.chain) #runs the build chain function using designated backbone and sensors
        return self.chain



    def cdist(self, sensor1, sensor2):
        '''
        BFS = O(n)
        accessing .d take O(1)

        Overall, the running time of cdist is O(n)
        '''
        BFS(self.backbone, sensor2) #runs BFS to populate distances from Sensor 2

        # Return the communication distance to Sensor 1
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






