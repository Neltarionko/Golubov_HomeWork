import random
import numpy as np
from rrt import *


class RRT_connect(RRT): 
    def get_tree(self,tree):
        self.rrt_tree = tree   
        
               
    def check_connect(self,point):
        '''Проверка наличия сязи между двумя деревьями

        return: точку соединения, 0 при отсутствии таковой
        '''
        for tree_point in self.rrt_tree.all_point:
            if ((point[0]-tree_point[0])**2 + (point[1]-tree_point[1])**2) <= self.end_area**2:
                if self.find_collision(point,tree_point) != 1:
                    return tree_point
        return 0
        
    def make_tree(self):
        '''Создает деревья от начала и конца пути, после их соденинения возвращает путь

        return: путь между начальной и конечной
        '''
        point = (random.randint(0,self.map.shape[0]),random.randint(0,self.map.shape[1]))
        nearest_point = self.find_nearest_point(point)
        point = self.check_growth_factor(point,nearest_point)
        if self.find_collision(point,nearest_point):
            self.rrt_tree.make_tree()
        else:
            self.all_point.append(point)
            self.tree[point] = nearest_point
            check_connect = self.check_connect(point)
            if check_connect == 0:
                self.rrt_tree.make_tree()
            else:
                path1 = self.find_path(self.all_point[-1])
                path2 = self.rrt_tree.find_path(check_connect)
                self.path = np.array(list(reversed(path1)) + path2)
                self.rrt_tree.path = np.array(list(reversed(path1)) + path2)
        return self.path
            
            
