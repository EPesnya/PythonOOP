# Песня Евгений

import numpy as np
import sympy as smp
import second as sec

class CN:
    def __init__(self, h, n_dim, left, right):
        self.h = h
        self.n_dim = n_dim
        self.points = np.arange(left, right, h)

    def norm(self, f):
        result = np.amax(abs(f(self.points)))
        derivative_num = sec.DerivativeNum(f, self.h, [-1/2, 0, 1/2])
        temp = self.points
        for _ in range(self.n_dim):
            temp = np.amax(abs(derivative_num(temp)))
            result += temp
        return result

    def metrics(self, f1, f2):
        return np.sqrt(self.norm(lambda x: f1(x) - f2(x)))



if __name__ == "__main__":
    x_sym = smp.Symbol('x')

    functions_sym = [5 / (2 + 3 * x_sym ** 2), 2 / (5 + smp.cos(x_sym)),
                    (3 + 4 * x_sym ** 2) ** 1 / 3,
                    2 / smp.sqrt(smp.pi) * smp.exp(-x_sym ** 2)]
    functions = [smp.lambdify(x_sym, f) for f in functions_sym]

    h = 10e-3
    a = 0.
    b = 2.

    spaces = [CN(h, i, a, b) for i in range(3)]

    for i in range(3):
        for f, fs in zip(functions, functions_sym):
            print('The norm of the function ' + str(fs) +
                ' in C' + str(i) +
                ' space: ' + str(spaces[i].norm(f)))


    for i in range(3):
        j = 1
        for f, fs in zip(functions, functions_sym):
            for f1, fs1 in zip(functions[j:], functions_sym[j:]):
                res = spaces[i].metrics(f, f1)
                print('The distance between ' + str(fs) +
                    ' and ' + str(fs1) +
                    ' in C' + str(i) +
                    ' space: ' + str(res))
            j += 1
