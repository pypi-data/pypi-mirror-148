from numpy import append, log, sqrt, zeros, arange, exp, cumsum
from .utils import triax_n, critical_state_intercept

def undrained(p_0:float, M:float, kappa:float, lmbda:float, e0:float, nu:float ) -> tuple[float, float, str]:
    """Undrained test on Cam-Clay

    Args:
        p_0 (float): Preconsolidation Pressure
        M (float): Slope of Critical State Line
        kappa (float): Unloading Slope
        lmbda (float): Loading Slope
        e (float): Void Ratio
        nu (float): Poisson's ratio

    Returns:
        Tuple:axial strain, deviatoric stress, label
    """
    label = "Undrained"
    dp = 1
    dq = triax_n(dp)

    e_lmbda = critical_state_intercept(e0, lmbda, kappa, p_0)

    pf = exp((e_lmbda - e0) / lmbda)

    p = arange(p_0, pf - 1, -dp)

    pc = append([p_0], zeros((1, len(p) - 1)))

    for i in range(1, len(pc)):
        pc[i] = pc[i - 1] * (p[i - 1] / p[i]) ** (kappa / (lmbda - kappa))

    q = M * p * sqrt(pc / p - 1)
    eta = q / p

    deve = kappa / (1 + e0) * -dp / p
    deve[0] = 0

    devp = -deve
    
    desp = devp * 2 * eta / (M ** 2 - eta ** 2)
    G = 3 * (1 - 2 * nu) * (1 + e0) * p / (2 * (1 + nu) * kappa)
    dese = dq / (3 * G)

    des = dese + desp
    es = cumsum(des)
    e1 = es
    pu = p_0 + q / 3
    du = pu - p
    return e1, q, label
