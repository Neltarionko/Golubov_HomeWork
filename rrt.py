import random
import numpy as np
import matplotlib.pyplot as plt
import math


class RRT():
    def __init__(self,start: tuple,end: tuple,map: np.array, end_area, growth_factor):
        self.start = start  # Точка начала пути
        self.end = end  # Точка конца пути
        self.map = map
        self.all_point = [start]  # Массив из точек, входящих в дерево
        self.tree = {}  # Словарь дерева вида Точка_начала_отрезка:Точка_конца_отрезка
        self.end_area = end_area
        self.growth_factor = growth_factor
    
    def find_nearest_point(self,point):
        '''Поиск ближайшей точки среди точек входящих в дерево

        point: Точка, расстояние до которой измеряется
        return: Ближайшая точка из имеющихся в дереве
        '''
        min = 9999
        best_point = (0,0)
        for tree_point in self.all_point:
            distance = ((tree_point[0]-point[0])**2 + (tree_point[1]-point[1])**2)**0.5
            if distance < min:
                best_point = tree_point
                min = distance
        return best_point
    
    def find_collision(self,point,nearest_point):
        '''Поиск пересечений прямой между указанными точками и препятствиями на карте

        point:: Точка начала отрезка
        nearest_point: Точка конца отрезка
        '''
        dx = point[1] - nearest_point[1]
        dy = point[0] - nearest_point[0]
        '''
        Так как функция вызывается для точки дерева пути и рандомной,
        то при их совпадении пересечений с препятствием нет
        '''
        if dx == 0 and dy == 0:
            return True
        
        if abs(dx) >= abs(dy):
            for x in range(point[1]-1,nearest_point[1],np.sign(nearest_point[1] - point[1])):
                y = (dy/dx)*(x - nearest_point[1]) + nearest_point[0]
                try:
                    if self.map[int(y),int(x)] == 1:
                        return True
                except:
                    continue
        else:
            for y in range(point[0]-1,nearest_point[0],np.sign(nearest_point[0] - point[0])):
                x = (dx/dy)*(y - nearest_point[0]) + nearest_point[1]
                try:
                    if self.map[int(y),int(x)] == 1:
                        return True
                except:
                    continue
        return False
    
    def find_path(self):
        '''Поиск пути в построенном дереве

        return: Массив точек дерева между начальной и конечной
        '''
        path = [self.all_point[-1]]
        while path[-1] != self.start:
            path.append(self.tree[path[-1]])
        return np.array(path)
    
    def check_end_area(self,point):
        return ((point[0]-self.end[0])**2 + (point[1]-self.end[1])**2) <= self.end_area**2
    
    def check_growth_factor(self,point,nearest_point):
        if ((point[0]-nearest_point[0])**2 + (point[1]-nearest_point[1])**2) >= self.growth_factor**2:
            dx = point[1]-nearest_point[1]
            dy = point[0]-nearest_point[0]
            angle = math.atan2(dy,dx)
            return (int(nearest_point[0] + self.growth_factor * math.sin(angle)), int(nearest_point[1] + self.growth_factor * math.cos(angle)))
        else:
            return point
        
    
    def make_tree(self,step: int):
        '''Создание дерева

        step: Максимальное количество измерений для RRT
        '''
        for  i in range(step):
            point = (random.randint(0,self.map.shape[0]),random.randint(0,self.map.shape[1]))
            nearest_point = self.find_nearest_point(point)
            point = self.check_growth_factor(point,nearest_point)
            if self.find_collision(point,nearest_point):
                continue
            else:
                self.all_point.append(point)
                self.tree[point] = nearest_point
                if self.check_end_area(point):
                    return self.find_path()
                
start = (11,11)
end = (150,150)
end_area = 10
growth_factor = 20
map = np.loadtxt("map.txt", dtype=float)
rrt = RRT(start,end,map,end_area,growth_factor)
path = rrt.make_tree(100000)
plt.imshow(map, cmap='Greys')
plt.plot(start[1],start[0],"bo")
plt.plot(end[1],end[0],"go")
plt.plot(path[0:path.shape[0],1],path[0:path.shape[0],0])
plt.show()