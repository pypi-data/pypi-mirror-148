

from .utils import plot
from .drained import drained
from .undrained import undrained


if __name__ == "__main__":
    from default_params import *

    e1, q, label = drained(p_0, M, kappa, lmbda, e0)

    plot(e1, q, label)

    e1, q, label = undrained(p_0, M, kappa, lmbda, e0, nu)

    plot(e1, q, label)
