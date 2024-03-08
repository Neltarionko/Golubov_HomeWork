import random
import numpy as np
import math
import matplotlib.pyplot as plt


class RRT():
    def __init__(self,start: tuple,end: tuple,map: np.array):
        self.start = start
        self.end = end
        self.map = map
        self.all_point = [start]
        self.tree = {}
    
    def find_nearest_point(self,point):
        min = 9999
        best_point = (0,0)
        for tree_point in self.all_point:
            distance = ((tree_point[0]-point[0])**2 + (tree_point[1]-point[1])**2)**0.5
            if distance < min:
                best_point = tree_point
                min = distance
        return best_point
    
    def find_collision(self,point,nearest_point):
        
        dx = point[1] - nearest_point[1]
        dy = point[0] - nearest_point[0]
        if dx == 0 and dy == 0:
            return 1
        if abs(dx) >= abs(dy):
            for x in range(point[1]-1,nearest_point[1],np.sign(nearest_point[1] - point[1])):
                y = (dy/dx)*(x - nearest_point[1]) + nearest_point[0]
                try:
                    if self.map[int(y),int(x)] == 1:
                        return 1
                except:
                    continue
        else:
            for y in range(point[0]-1,nearest_point[0],np.sign(nearest_point[0] - point[0])):
                x = (dx/dy)*(y - nearest_point[0]) + nearest_point[1]
                try:
                    if self.map[int(y),int(x)] == 1:
                        return 1
                except:
                    continue
        return 0 
    
    def find_path(self):
        path = [self.end]
        while path[-1] != self.start:
            path.append(self.tree[path[-1]])
        return path
        
    
    def make_tree(self,step):
        for  i in range(step):
            point = (random.randint(0,self.map.shape[0]),random.randint(0,self.map.shape[1]))
            nearest_point = self.find_nearest_point(point)
            if self.find_collision(point,nearest_point):
                continue
            else:
                if point != self.end:
                    self.tree[point] = nearest_point
                    self.all_point.append(point)
                else:
                    self.tree[point] = nearest_point
                    return self.find_path()
                
            
            
rrt = RRT((11,11),(1,1),np.loadtxt("map.txt", dtype=float))
print(rrt.make_tree(10000000))
