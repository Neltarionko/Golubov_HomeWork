import random
import numpy as np


class RRT():
    def __init__(self,start: tuple,end: tuple,map: np.array):
        self.start = start  # Точка начала пути
        self.end = end  # Точка конца пути
        self.map = map
        self.all_point = [start]  # Массив из точек, входящих в дерево
        self.tree = {}  # Словарь дерева вида Точка_начала_отрезка:Точка_конца_отрезка
    
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
        path = [self.end]
        while path[-1] != self.start:
            path.append(self.tree[path[-1]])
        return path
        
    
    def make_tree(self,step: int):
        '''Создание дерева

        step: Максимальное количество измерений для RRT
        '''
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
print(rrt.make_tree(100000))
