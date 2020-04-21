# Песня Евгений

import numpy as np
import matplotlib.pyplot as plt
from abc import ABC


class AbstractExplicitRKmethod(ABC):
    
    def __init__(self, f, u_0, num_blocks, t_start, t_end):
        self.a = None
        self.b = None
        self.c = None

        self.f = f
        self.u_0 = u_0
       
        self.num_blocks, self.num_points = num_blocks, num_blocks + 1
        self.dt = (float(t_end) - float(t_start))/self.num_blocks
        
        self.solution_array = np.zeros(self.num_points)
        self.time_array = np.linspace(t_start, t_end, self.num_points)
        
        self.t_start, self.t_end = float(t_start), float(t_end)  

    def solve(self):
        self.solution_array[0] = self.u_0

        for i in range(self.num_blocks):
            u_old = self.solution_array[i]                
            self.solution_array[i + 1] = u_old + self.dt * np.dot(self.b, self.k(u_old))

    def k(self, u_i):
        k = np.zeros(len(self.b))
        k[0] = self.f(u_i)
        for i in range(len(k) - 1):
            k[i + 1] = self.f(u_i + np.dot(self.a[i + 1, :], k))
        return k
    
    def plot_solution(self):
        plt.plot(self.time_array, self.solution_array, '-', linewidth=4)
        plt.grid('off')
        plt.title('Решение методом %s ' % self.__class__.__name__)
        plt.xlabel('Время')
        plt.ylabel('Популяция')
        plt.show()


class ExplicitEuler(AbstractExplicitRKmethod):

    def __init__(self, f, u_0, num_blocks, t_start, t_end):
        super().__init__(f, u_0, num_blocks, t_start, t_end)
        self.a = np.array([0])
        self.b = np.array([1])

class Heun(AbstractExplicitRKmethod):

    def __init__(self, f, u_0, num_blocks, t_start, t_end):
        super().__init__(f, u_0, num_blocks, t_start, t_end)
        self.a = np.array([
            [0, 0],
            [1, 0]
            ])
        self.b = np.array([1/2, 1/2])

class RK4(AbstractExplicitRKmethod):

    def __init__(self, f, u_0, num_blocks, t_start, t_end):
        super().__init__(f, u_0, num_blocks, t_start, t_end)
        self.a = np.array([
            [  0,   0,   0,   0],
            [1/2,   0,   0,   0],
            [  0, 1/2,   0,   0],
            [  0,   0,   1,   0]
            ])
        self.b = np.array([1/6, 1/3, 1/3, 1/6])

class ImplicitTrapezoidal:
    pass


class LogisticRightHandSide:
        
    def __init__(self, alpha, R):
        self._alpha = float(alpha)
        self._R = float(R)
    
    def __call__(self, u):
        return self._alpha * u * (1. - u/self._R)




if __name__ == "__main__":
    
    methods_class = [ExplicitEuler, Heun, RK4]
    rhs_1 = LogisticRightHandSide(alpha=0.2, R=100.)

    for method_class in methods_class:
        method = method_class(f=rhs_1, u_0=2., num_blocks=30, t_start=0., t_end=80.)    
        method.solve()
        method.plot_solution()