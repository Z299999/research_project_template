"""Plotting routines for the damped oscillator.

Each function has the shape ``fig_<name>(res, out_path, ...)``: it takes a
results dict from ``oscillator.simulate`` and writes one figure file. Plotting
never re-runs the simulation.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless: write files, never open a window
import matplotlib.pyplot as plt


def fig_trajectory(res: dict, out_path, title: str | None = None) -> None:
    """Displacement x(t) — the flagship figure."""
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.plot(res["t"], res["x"], lw=1.6, color="#1f77b4")
    ax.axhline(0.0, color="0.7", lw=0.8, zorder=0)
    ax.set_xlabel("time $t$")
    ax.set_ylabel("displacement $x(t)$")
    ax.set_title(title or fr"$\zeta={res['zeta']:.2f}$, $\omega={res['omega']:.2f}$")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def fig_phase(res: dict, out_path, title: str | None = None) -> None:
    """Phase portrait v vs x — the spiral/return to the origin."""
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    ax.plot(res["x"], res["v"], lw=1.2, color="#d62728")
    ax.plot([res["x"][0]], [res["v"][0]], "o", color="#d62728", ms=4)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$\\dot{x}$")
    ax.set_title(title or "phase portrait")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
