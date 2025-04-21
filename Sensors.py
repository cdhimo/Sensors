# MA214 Assessed Coursework 2025
#
# Candidate Number: PUT YOUR CANDIDATE NUMBER HERE

from collections import deque
from math import inf
from math import sqrt


'''
Explain the design of your program here. (See Task 3.)
'''


# add other classes and functions you need here

class SensorStorage:
    def __init__(self,sensor_list):
        self.n = len(sensor_list)
        self.V = [sensor for sensor in sensor_list]
        self.Adj = [deque() for _ in range(self.n)]
        for i in range(self.n):
            self.V[i].id = i

    def AdjList(self):
        for i in range(self.n):
            sensor1 = self.V[i]
            for j in range(i+1,self.n):
                sensor2 = self.V[j]
                if sensor1.x == sensor2.x or sensor1.y == sensor2.y:
                    w = sqrt((sensor2.x - sensor1.x)**2 + (sensor2.y - sensor1.y)**2)
                    self.Adj[i].append((sensor2,w))
                    self.Adj[j].append((sensor1,w))
        return self.Adj


def swap(Q, i, j):
    Q[i], Q[j] = Q[j], Q[i]
    Q[i].pos = i
    Q[j].pos = j


def MinHeapify(Q, i):
    smallest = i
    l = 2 * i + 1
    r = 2 * i + 2
    for c in [l, r]:
        if c < len(Q) and Q[c].key < Q[smallest].key:
            smallest = c
    if smallest == i:
        return
    swap(Q, i, smallest)
    MinHeapify(Q, smallest)


def ExtractMin(Q):
    swap(Q, 0, len(Q) - 1)
    min = Q.pop()
    MinHeapify(Q, 0)
    return min

def DecreaseKey(Q, v, k):
    v.key = k
    i = v.pos
    while i > 0 and Q[(i - 1) // 2].key > Q[i].key:
        Q[(i - 1) // 2].pos = i
        Q[i].pos = (i - 1) // 2
        Q[(i - 1) // 2], Q[i] = Q[i], Q[(i - 1) // 2]
        i = (i - 1) // 2

def MSTPrim(S,r):
    Q = []
    for i in range(0,len(S.V)):
        u = S.V[i]
        u.key = inf
        u.pi = None
        Q.append(u)
        u.pos = i
        u.InQueue = True
    DecreaseKey(Q,r,0)
    while Q:
        u = ExtractMin(Q)
        u.InQueue = False
        for v,w in S.Adj[u.id]:
            print(v.key)
            if v.InQueue == True and w < v.key:
                v.pi = u
                DecreaseKey(Q,v,w)





class Backbone:
    def __init__(self,sensor_list):
        pass


# Implement the class Sensor here. (See Task 1.)
class Sensor:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.id = None # Everything below including ID is needed for prims algorithm - id is set during the sensor storage portion
        self.key = inf
        self.pi = None
        self.pos = inf
        self.inQueue = False
    def __repr__(self):
        return f"({str(self.x)},{str(self.y)})"

        
class SensorCollection:
    
    def __init__(self,sensor_list):
        self.storage = SensorStorage(sensor_list)



                
    def communicate(self,sensor1,sensor2):
        # Add your implementation here. (See Task 2.)
        pass

    def cdist(self,sensor1,sensor2):
        pass
    # Add other functions you need here.

sensors = [Sensor(0,0),Sensor(0,1),Sensor(0,2),Sensor(1,0),Sensor(1,1),Sensor(1,2),Sensor(2,0),Sensor(2,1),Sensor(2,2)]



'''
# Main block (for testing purposes only):
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
prac = SensorStorage(sensors)
MSTPrim(prac,sensors[0])


