# Песня Евгений

import numpy as np
import sympy as smp
import matplotlib.pyplot as plt

x_sym = smp.Symbol('x')

functions_sym = [smp.sin(x_sym**2), smp.cos(smp.sin(x_sym)), smp.exp(smp.sin(smp.cos(x_sym))), \
    smp.log(x_sym + 3), smp.sqrt(x_sym + 3)]
functions = [smp.lambdify(x_sym, f) for f in functions_sym]

derivatives_analytical_sym = [smp.diff(f, x_sym) for f in functions_sym]
derivatives_analytical = [smp.lambdify(x_sym, f) for f in derivatives_analytical_sym] 

smp.pprint(functions_sym, use_unicode=False)
# smp.pprint(derivatives_analytical_sym, use_unicode=False)

class DerivativeNum:
    
    def __init__(self, f, h, coefficients):
        self.f = f
        self.h = h
        self.coefficients = coefficients

    def set_coefficients(self, coefficients):
        self.coefficients = coefficients

    def __call__(self, x):
        f, h, c = self.f, self.h, self.coefficients
        x_i = np.linspace(x - h * np.floor(len(c) / 2), x + h * np.floor(len(c) / 2), len(c))
        return c @ f(x_i) / h


x_0 = 5
h_0 = 0.05

coefficients_1 = [0, -1, 1]
coefficients_2 = [-1, 1, 0]
coefficients_3 = [-1/2, 0, 1/2]
coefficients_4 = [1/12, -2/3, 0, 2/3, -1/12]
coefficients_5 = [-1/60, 3/20, -3/4, 0, 3/4, -3/20, 1/60]

derivatives_num = []

for f in functions:
    derivatives_num.append(DerivativeNum(f, h_0, coefficients_3))

x_left, x_right = 0., 10.
num_points = 100
x_data = np.linspace(x_left, x_right, num_points)


fig, axs = plt.subplots(3, len(functions))

for i in range(len(functions)):
    axs[0, i].plot(x_data, functions[i](x_data))
    axs[0, i].set_title(functions_sym[i])
    axs[1, i].plot(x_data, derivatives_analytical[i](x_data))
    axs[1, i].set_title(derivatives_analytical_sym[i])
    axs[2, i].plot(x_data, derivatives_num[i](x_data))

axs[0, 0].set(ylabel = "Функции")
axs[1, 0].set(ylabel = "Аналит. произв.")
axs[2, 0].set(ylabel = "Числ. произв.")

for ax in fig.get_axes():
    ax.label_outer()

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()


steps = [2**(-n) for n in range(20)]
coef = [coefficients_1, coefficients_2, coefficients_3, coefficients_4, coefficients_5]
fig, axs = plt.subplots(2, 3)
fig.suptitle('Анализ сходимости')

for i in range(len(coef)):
    for f, dfdx in zip(functions, derivatives_analytical):
            errors = []
            
            for h in steps:
                dfdxNum = DerivativeNum(f, h, coef[i])
                error = np.fabs(dfdxNum(x_0) - dfdx(x_0))
                errors.append(error)

            axs[int(i / 3), int(i % 3)].set_title("coefficients {}".format(i + 1))
            axs[int(i / 3), int(i % 3)].loglog(steps, errors, '-o', linewidth=2, markersize=5)

for ax in axs.flat:
    ax.set(xlabel='Шаг сетки', ylabel='Погрешность')
for ax in axs.flat:
    ax.label_outer()

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()