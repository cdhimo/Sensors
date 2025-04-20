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
    def __init__(self,Sensors):
        self.n = len(Sensors)
        self.V = [sensor for sensor in Sensors]
        self.Adj = [deque() for _ in range(self.n)]

    def add_adj(self):
        x_coord = {}
        y_coord = {}
        for idx, sensor in enumerate(self.V):
            x_coord[sensor.x] = idx
            y_coord[sensor.y] = idx




# Implement the class Sensor here. (See Task 1.)
class Sensor:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({str(self.x)},{str(self.y)})"

        
class SensorCollection:
    
    def __init__(self,sensor_list):
        pass


                
    def communicate(self,sensor1,sensor2):
        # Add your implementation here. (See Task 2.)
        pass

    def cdist(self,sensor1,sensor2):
        # Add your implementation here. (See Task 2.)
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
