# Песня Евгений

import numpy as np
import sympy as smp
import matplotlib.pyplot as plt

x_sym = smp.Symbol('x')
functions_sym = [smp.sin(x_sym**2), smp.cos(smp.sin(x_sym)), smp.exp(smp.cos(smp.sin(x_sym))),
    smp.log(x_sym + 3), smp.sqrt(x_sym + 3)]
functions = [smp.lambdify(x_sym, f) for f in functions_sym]

# antiderivatives_analytical_sym = [smp.integrate(f,(x_sym, 0, x_sym)) for f in functions_sym]
# smp.pprint(functions_sym, use_unicode=False)
# smp.pprint(float(antiderivatives_analytical_sym, use_unicode=False)

class AntiderivativeNum:
    
    def __init__(self, function, left_border, blocks_num):
        self.function = function
        self.left_border = left_border
        self.blocks_num = blocks_num
        self.coefficients = None

    def __call__(self, x):
        grid = self.__make_grid(x)
        h = (x - self.left_border) / self.blocks_num
        antiderivative = self.coefficients @ self.function(grid) * h
        return antiderivative

    def __make_grid(self, x):
        return np.linspace(self.left_border, x, self.blocks_num + 1)


class AntiderivativeRightRect(AntiderivativeNum):

    def __init__(self, function, left_border, blocks_num):
        AntiderivativeNum.__init__(self, function, left_border, blocks_num)
        self.coefficients = np.array([0] + [1] * blocks_num)

class AntiderivativeLeftRect(AntiderivativeNum):

    def __init__(self, function, left_border, blocks_num):
        AntiderivativeNum.__init__(self, function, left_border, blocks_num)
        self.coefficients = np.array([1] * blocks_num + [0])

class AntiderivativeMidRect(AntiderivativeLeftRect):

    def __make_grid(self, x):
        return np.linspace(self.left_border, x, self.blocks_num + 1) + \
            (x - self.left_border) / self.blocks_num

class AntiderivativeTrapezium(AntiderivativeNum):

    def __init__(self, function, left_border, blocks_num):
        AntiderivativeNum.__init__(self, function, left_border, blocks_num)
        self.coefficients = np.array([1 / 2] + [1] * (blocks_num - 1) + [1 / 2])

class AntiderivativeSimpson(AntiderivativeNum):

    def __init__(self, function, left_border, blocks_num):
        if (blocks_num % 2 == 0):
            AntiderivativeNum.__init__(self, function, left_border, blocks_num)
            self.coefficients = np.array([1 / 3] + [4 / 3, 2 / 3] * (int(blocks_num / 2) - 1) \
                + [4, 1 / 3])
        else:
            raise ValueError("In Simpson's rule blocks_num must be even.")



classes = [AntiderivativeRightRect, AntiderivativeLeftRect,
    AntiderivativeMidRect, AntiderivativeTrapezium, AntiderivativeSimpson]

x = np.linspace(0, 2, 51)
N = [2**(i + 1) for i in range(15)]

##############

antiderivatives_analytical = [[float(smp.integrate(f, (x_sym, 0, x_right))) for x_right in x]
    for f in functions_sym]
antiderivatives_num = [AntiderivativeRightRect(f, 0, 100) for f in functions]

for f in antiderivatives_num:
    plt.plot(x, f(x), 'b')

for f in functions_sym:
    plt.plot(x, antiderivatives_analytical[functions_sym.index(f)], 'g')

plt.show()

##############

for fun, fun_sym in zip(functions, functions_sym):
    antiderivative_analytical = antiderivatives_analytical[functions.index(fun)]
    fig, axs = plt.subplots(2, 3)
    fig.suptitle(fun_sym)

    for Antiderivative in classes:
        for n in N:
            antiderivative_num = Antiderivative(fun, 0, n)
            f = np.fabs(antiderivative_num(x) - antiderivative_analytical)
            i = classes.index(Antiderivative)
            axs[int(i / 3), int(i % 3)].set_title(Antiderivative.__name__)
            axs[int(i / 3), int(i % 3)].loglog(x, f)

    for ax in axs.flat:
        ax.label_outer()
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()