"""Damped harmonic oscillator — the model kernel.

The equation of motion is

    x'' + 2 zeta omega x' + omega^2 x = 0,

with `zeta` the damping ratio and `omega` the natural angular frequency. The
qualitative behaviour is set entirely by `zeta`:

    zeta < 1   underdamped   (decaying oscillation, overshoot)
    zeta = 1   critical      (fastest non-oscillatory return)
    zeta > 1   overdamped    (slow non-oscillatory return)

This is the whole point of the sample: the same kernel produces three very
different regimes purely from configuration.
"""

from __future__ import annotations

import numpy as np


def _deriv(state: np.ndarray, omega: float, zeta: float) -> np.ndarray:
    x, v = state
    return np.array([v, -2.0 * zeta * omega * v - omega**2 * x])


def simulate(
    omega: float = 1.0,
    zeta: float = 0.2,
    x0: float = 1.0,
    v0: float = 0.0,
    t_max: float = 30.0,
    dt: float = 0.01,
    ic_jitter: float = 0.05,
    seed: int = 0,
) -> dict:
    """Integrate the oscillator with RK4 and return a results dict.

    `seed` perturbs the initial state by `ic_jitter` (Gaussian), so different
    seeds are genuinely different runs while staying near the same regime — this
    is what makes the `runs/..._seedN/` convention meaningful.

    Returns a dict of plain arrays/scalars: ``t``, ``x``, ``v``, plus the
    ``omega`` and ``zeta`` used.
    """
    rng = np.random.default_rng(seed)
    x0 = x0 + ic_jitter * rng.standard_normal()
    v0 = v0 + ic_jitter * rng.standard_normal()

    n = int(round(t_max / dt))
    t = np.linspace(0.0, n * dt, n + 1)
    traj = np.empty((n + 1, 2))
    traj[0] = (x0, v0)
    for i in range(n):
        s = traj[i]
        k1 = _deriv(s, omega, zeta)
        k2 = _deriv(s + 0.5 * dt * k1, omega, zeta)
        k3 = _deriv(s + 0.5 * dt * k2, omega, zeta)
        k4 = _deriv(s + dt * k3, omega, zeta)
        traj[i + 1] = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    return {"t": t, "x": traj[:, 0], "v": traj[:, 1], "omega": omega, "zeta": zeta}


def metrics(res: dict, settle_frac: float = 0.05) -> dict:
    """Headline numbers for the run's ``metrics.json``.

    - ``overshoot``: largest excursion past zero on the opposite side of x0
      (0 for a non-oscillatory response).
    - ``settling_time``: last time |x| leaves the +/- settle_frac*|x0| band.
    - ``final_abs_x``: |x| at the end of the horizon.
    """
    t, x = res["t"], res["x"]
    x0 = x[0]
    band = settle_frac * abs(x0)

    overshoot = max(0.0, -np.min(x * np.sign(x0)) / abs(x0)) if x0 != 0 else 0.0

    outside = np.where(np.abs(x) > band)[0]
    settling_time = float(t[outside[-1]]) if outside.size else 0.0

    return {
        "overshoot": float(overshoot),
        "settling_time": settling_time,
        "final_abs_x": float(abs(x[-1])),
    }
