from numpy import log

import matplotlib.pyplot as plt


triax_n = lambda d_p: d_p*3

def critical_state_intercept(e0, lmbda, kappa, p_0):
    return e0 + (lmbda - kappa) * log(p_0 / 2) + kappa * log(p_0)

def plot(x, y, title):
    plt.plot(x, y)
    plt.xlabel("$\epsilon_1$")
    plt.ylabel("$q$")
    plt.title(title)
    plt.show()
