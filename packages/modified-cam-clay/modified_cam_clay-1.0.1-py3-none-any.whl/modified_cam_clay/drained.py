from numpy import append, arange, cumsum, roll, zeros
from .utils import triax_n


def drained(p_0:float, M:float, kappa:float, lmbda:float, e:float) -> tuple[float,float,str]:
    """Drained Triaxial Test

    Args:
        p_0 (float): Preconsolidation Pressure
        M (float): Slope of Critical State Line
        kappa (float): Unloading Slope
        lmbda (float): Loading Slope
        e (float): Void Ratio

    Returns:
        Tuple: axial strain, deviatoric stress, label
    """
    label = 'Drained'
    dp = 1
    dq = triax_n(dp)

    pf = 3 * p_0 / (3 - M)
    qf = 3 * M * p_0 / (3 - M)

    p = append([0], arange(p_0, pf, dp))

    q = append([0], arange(0, qf, dq))

    eta = append([0], q[1:] / p[1:])
    eta_n = roll(eta, 1)
    eta_n[0] = 0
    deta = eta - eta_n
    
    dev = (
        lmbda
        / (1 + e)
        * (dp / p + (1 - kappa / lmbda) * 2 * eta * deta / (M ** 2 + eta ** 2))
    )
    dev[0] = 0
    evk = cumsum(dev)

    de = (1 + e) * dev

    e = append([e], zeros((0, len(de) - 1)))

    for i in range(1, len(e)):
        e[i] = e[i - 1] - de[i]

    des = (
        (lmbda - kappa)
        / (1 + e)
        * (dp / p + 2 * eta * deta / (M ** 2 + eta ** 2))
        * (2 * eta / (M ** 2 - eta ** 2))
    )
    des[0] = 0
    es = cumsum(des)
    e1 = evk / 3 + es
    return e1, q, label
