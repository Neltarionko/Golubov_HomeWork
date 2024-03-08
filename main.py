import numpy as np 
import matplotlib.pyplot as plt
from rrt import *
from rrt_connect import *
'''
map = np.loadtxt("map.txt", dtype=float)
map = np.rot90(map)
map = map[70:240,25:240]
np.savetxt("map2.txt", map, fmt="%d")
plt.imshow(map, cmap='Greys')
plt.show()
'''

rrt_mod = 1

if rrt_mod == 0:
    start = (150,50)
    end = (20,150)
    end_area = 2
    growth_factor = 20
    map = np.loadtxt("map2.txt", dtype=float)
    rrt = RRT(start,end,map,end_area,growth_factor)
    path = rrt.make_tree(100000)
    plt.imshow(map, cmap='Greys')
    rrt.print_all_tree()
    plt.plot(start[1],start[0],"bo")
    plt.plot(end[1],end[0],"go")
    plt.plot(path[0:path.shape[0],1],path[0:path.shape[0],0],"b",ms = 3)
    plt.show()
elif rrt_mod == 1:
    start = (150,50)
    end = (20,150)
    end_area = 30
    growth_factor = 20
    map = np.loadtxt("map2.txt", dtype=float)
    rrt1 = RRT_connect(start,end,map,end_area,growth_factor)
    rrt2 = RRT_connect(end,start,map,end_area,growth_factor)
    rrt1.get_tree(rrt2)
    rrt2.get_tree(rrt1)
    path = rrt1.make_tree()
    plt.imshow(map, cmap='Greys')
    rrt1.print_all_tree()
    rrt2.print_all_tree()
    plt.plot(start[1],start[0],"bo")
    plt.plot(end[1],end[0],"go")
    plt.plot(path[0:path.shape[0],1],path[0:path.shape[0],0],color="#7cb3e3b0")
    plt.show()