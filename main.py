import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys

class Graph():
    def __init__(self,map) -> None:
        self.map = map
        self.G = nx.Graph()
        self.all_poit = []
    
    def make_grapf(self,point = [(1,1),(2,2)]):
        if point in self.all_poit:
            return
        robot1 = point[0]
        robot2 = point[1]
        self.all_poit.append(point)
        for y1 in range(max(0,robot1[0]-1),min(self.map.shape[0],robot1[0]+2)):
            for x1 in range(max(0,robot1[1]-1),min(self.map.shape[1],robot1[1]+2)):
                if abs(y1-robot1[0]) + abs(x1-robot1[1]) == 2:
                    continue
                for y2 in range(max(0,robot2[0]-1),min(self.map.shape[0],robot2[0]+2)):
                    for x2 in range(max(0,robot2[1]-1),min(self.map.shape[1],robot2[1]+2)):
                        if abs(y2-robot2[0]) + abs(x2-robot2[1]) == 2:
                            continue

                        if x2 == x1 and y2 == y1:
                            continue
                        if (self.map[y1,x1] != 1) and (self.map[y2,x2] != 1):
                            self.G.add_edge(str([robot1,robot2]),str([(y1,x1),(y2,x2)]))
                            self.make_grapf([(y1,x1),(y2,x2)])
        return self.G

def plot_one_point(G,poit):
    G2 = nx.Graph()
    for n in G.neighbors(poit):
        G2.add_edge(poit,n)
    nx.draw_spring(G2, with_labels = True)
    plt.show()
    
def plot_all_grpah(G):
    nx.draw_shell(G, with_labels = True)
    plt.show()
    
def make_map():
    map = np.zeros((10,10))
    map[0,:] = 1
    map[-1,:] = 1
    map[:,-1] = 1
    map[:,0] = 1
    map[2,1] = 1
    map[2,4:8] = 1
    map[3,5:8] = 1
    map[4,7:8] = 1
    map[5,2:5] = 1
    map[5+2,6:8] = 1
    return map

map = make_map()
#plt.imshow(map, cmap='Greys')
#plt.show()
sys.setrecursionlimit(100000)

GR = Graph(map)
G = GR.make_grapf()
mod = 1
point = str([(1,2),(2,2)])
if mod == 0:
    plot_one_point(G,point)
else:
    plot_all_grpah(G)
