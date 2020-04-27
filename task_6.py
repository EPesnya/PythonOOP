# Песня Евгений

import numpy as np
import matplotlib.pyplot as plt
from abc import ABC
import second as sec


class AbstractExplicitRKmethod(ABC):
    
    def __init__(
            self, f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            ):

        self.a = None
        self.b = None
        self.c = None

        self.f = f
        self.u_0 = u_0
        
        self.dt = dt
        self.t_num_blocks = int((float(t_end) - float(t_start)) / self.dt)
        self.t_num_points = self.t_num_blocks + 1

        self.h = h
        self.x_num_blocks = int((float(x_right) - float(x_left)) / self.h)
        self.x_num_points = self.x_num_blocks + 1

        self.solution_array = np.zeros((self.t_num_points, self.x_num_points))
        self.time_array = np.linspace(t_start, t_end, self.t_num_points)
        self.space_array = np.linspace(x_left, x_right, self.x_num_points)
        
        self.t_start, self.t_end = float(t_start), float(t_end)
        self.x_left, self.x_right = float(x_left), float(x_right)

    def solve(self):
        self.solution_array[0] = self.u_0(self.space_array)

        for i in range(self.t_num_blocks):
            u_old = self.solution_array[i]                
            self.solution_array[i + 1] = u_old + self.dt * np.dot(self.b, self.k(u_old))

    def k(self, u_i):
        k = np.zeros((len(self.b), len(u_i)))
        k[0] = self.f(u_i)
        for i in range(len(k) - 1):
            k[i + 1] = self.f(u_i + self.dt * np.dot(self.a[i + 1, :], k))
        return k
    
    def plot_solution(self):
        plt.plot(
            self.space_array, +
            self.solution_array[-1], '-',
            linewidth=2, label=self.__class__.__name__
            )


class ExplicitEuler(AbstractExplicitRKmethod):

    def __init__(
            self, f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            ):
        super().__init__(
            f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            )
        self.a = np.array([0])
        self.b = np.array([1])

class Heun(AbstractExplicitRKmethod):

    def __init__(
            self, f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            ):
        super().__init__(
            f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            )
        self.a = np.array([
            [0, 0],
            [1, 0]
            ])
        self.b = np.array([1/2, 1/2])

class RK4(AbstractExplicitRKmethod):

    def __init__(
            self, f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            ):
        super().__init__(
            f, u_0, dt, t_start, t_end,
            h, x_left, x_right
            )
        self.a = np.array([
            [  0,   0,   0,   0],
            [1/2,   0,   0,   0],
            [  0, 1/2,   0,   0],
            [  0,   0,   1,   0]
            ])
        self.b = np.array([1/6, 1/3, 1/3, 1/6])


class VectorRightHandSide:
        
    def __init__(self, k, h, b_l, b_r):
        self._k = float(k)
        self._h = float(h)
        self._b_l = float(b_l)
        self._b_r = float(b_r)
    
    def __call__(self, u):
        size = len(u)
        A = np.zeros((size, size))
        F = np.zeros(size)
        F[0], F[-1] = self._b_l, self._b_r
        np.fill_diagonal(A, -2)
        np.fill_diagonal(A[1:], 1)
        np.fill_diagonal(A[:, 1:], 1)
        return (A @ u + F) * self._k / self._h**2




if __name__ == "__main__":
    
    methods_class = [ExplicitEuler, Heun, RK4]

    k = 0.1
    h = 1/25
    dt = h**2 / 200 / k

    rhs = VectorRightHandSide(k=k, h=h, b_l=0 , b_r=0)

    def f_0(x):
        ans = np.zeros(len(x))
        ans[0.4 <= x] = 1
        ans[0.6 < x] = 0
        return ans


    for method_class in methods_class:
        method = method_class(
            f=rhs, u_0=f_0, dt=dt, t_start=0, t_end=0.04,
            h=h, x_left=0, x_right=1
            )    
        method.solve()
        method.plot_solution()
    
    plt.grid('off')
    plt.legend()
    plt.show()