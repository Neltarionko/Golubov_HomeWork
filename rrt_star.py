from rrt import *

class RRT_star(RRT):    
    
    def path_len(self,tree_point):
        '''Измеряет длину пути от начала до указанной точки

        return: измеренная длина пути
        '''
        path_len = 0
        temp_point = tree_point
        while temp_point != self.start:
            father_point = self.tree[temp_point] 
            path_len += ((temp_point[0]-father_point[0])**2 + (temp_point[1]-father_point[1])**2)**0.5
            temp_point = father_point
        return path_len
    
    def near_goal(self,point):
        '''Оптимизирует путь от начала до точек в области
        При наличии более короткого пути перестраивает ребра графа
        '''
        for tree_point in self.all_point:
            if ((point[0]-tree_point[0])**2 + (point[1]-tree_point[1])**2) <= self.growth_factor**2:
                old_path_len = self.path_len(tree_point)
                new_path_len = self.path_len(point) + ((point[0]-tree_point[0])**2 + (point[1]-tree_point[1])**2)**0.5
                if new_path_len < old_path_len and not self.find_collision(point,tree_point ):
                    del self.tree[tree_point]
                    self.tree[tree_point] = point
        
    
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
                self.near_goal(point)
                if self.check_end_area(point):
                    return np.array(self.find_path(self.all_point[-1]))