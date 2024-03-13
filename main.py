import numpy as np 
import matplotlib.pyplot as plt
from rrt import *
from rrt_connect import *
from rrt_star import *

# Цвета для графиков
brown = "#4d3d27"
red = "#448c39"
'''
Выбор алгоритма RRT
0 - RRT
1 - RRT connect
2 - RRT*
'''
rrt_mod = 2

# Координаты начала и конца пути
start = (100,43)
end = (20,150)

# Радиус области для засчитывания попадания в конечную точку
end_area = 2

# Фактор роста быстрорастущего дерева
growth_factor = 20

map = np.loadtxt("map2.txt", dtype=float)

if rrt_mod == 0:
    rrt = RRT(start,end,map,end_area,growth_factor)
    path = rrt.make_tree(100000)
    plt.imshow(map, cmap='Greys')
    rrt.print_all_tree(brown)
    plt.plot(start[1],start[0],"bo")
    plt.plot(end[1],end[0],"go")
    plt.plot(path[0:path.shape[0],1],path[0:path.shape[0],0],"b",ms = 3)
    plt.show()
elif rrt_mod == 1:
    rrt1 = RRT_connect(start,end,map,end_area,growth_factor)
    rrt2 = RRT_connect(end,start,map,end_area,growth_factor)
    rrt1.get_tree(rrt2)
    rrt2.get_tree(rrt1)
    path = rrt1.make_tree()
    plt.imshow(map, cmap='Greys')
    rrt1.print_all_tree(brown)
    rrt2.print_all_tree(red)
    plt.plot(start[1],start[0],"bo")
    plt.plot(end[1],end[0],"go")
    plt.plot(path[0:path.shape[0],1],path[0:path.shape[0],0],color="#7cb3e3b0")
    plt.show()
elif rrt_mod == 2:
    rrt = RRT_star(start,end,map,end_area,growth_factor)
    path = rrt.make_tree(10000)
    plt.imshow(map, cmap='Greys')
    rrt.print_all_tree(brown)
    plt.plot(start[1],start[0],"bo")
    plt.plot(end[1],end[0],"go")
    plt.plot(path[0:path.shape[0],1],path[0:path.shape[0],0],"b",ms = 3)
    plt.show()