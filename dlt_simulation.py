"""Dynamic Location Theory (DLT) resonance simulation prototype.

Run example:
    python dlt_simulation.py --num-objects 200 --steps 1000 --animate
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree


@dataclass
class DLTParams:
    """Simulation parameters for DLT dynamics."""

    num_objects: int = 200
    dimensions: int = 2
    dt: float = 0.03
    steps: int = 800
    omega_min: float = 0.0
    omega_max: float = 2.5
    coupling: float = 1.0
    interaction_radius: float = 1.25
    omega_bandwidth: float = 0.8
    drift_speed: float = 0.2
    phase_noise: float = 0.03
    position_noise: float = 0.01
    t_res_noise: float = 0.01
    temporal_coupling: float = 0.8
    world_size: float = 8.0
    coherence_window: int = 200


@dataclass
class DLTState:
    """State vectors for objects in the DLT simulation."""

    x: np.ndarray
    phi: np.ndarray
    omega: np.ndarray
    t_res: np.ndarray


@dataclass
class DLTLog:
    """Optional trajectory and metric logging."""

    trajectory: Optional[np.ndarray]
    coherence: np.ndarray


def initialize_state(params: DLTParams, seed: Optional[int] = None) -> DLTState:
    rng = np.random.default_rng(seed)
    x = rng.uniform(-params.world_size / 2, params.world_size / 2, size=(params.num_objects, params.dimensions))
    phi = rng.uniform(0.0, 2.0 * np.pi, size=params.num_objects)

    if np.isclose(params.omega_min, params.omega_max):
        omega = np.full(params.num_objects, params.omega_min, dtype=float)
    else:
        omega = rng.uniform(params.omega_min, params.omega_max, size=params.num_objects)

    t_res = np.zeros(params.num_objects, dtype=float)
    return DLTState(x=x, phi=phi, omega=omega, t_res=t_res)


def _neighbor_pairs(x: np.ndarray, interaction_radius: float) -> np.ndarray:
    tree = cKDTree(x)
    pairs = tree.query_pairs(r=interaction_radius, output_type="ndarray")
    if pairs.size == 0:
        return np.empty((0, 2), dtype=int)
    return pairs


def compute_global_coherence(phi: np.ndarray, omega: np.ndarray) -> float:
    phase_sync = np.abs(np.mean(np.exp(1j * phi)))
    omega_std = np.std(omega)
    freq_alignment = 1.0 / (1.0 + omega_std)
    return float(phase_sync * freq_alignment)


def update_state(
    state: DLTState,
    params: DLTParams,
    rng: np.random.Generator,
) -> tuple[DLTState, float]:
    n = state.x.shape[0]
    dims = state.x.shape[1]

    pairs = _neighbor_pairs(state.x, params.interaction_radius)

    phase_coupling = np.zeros(n, dtype=float)
    temporal_shift = np.zeros(n, dtype=float)
    pull = np.zeros((n, dims), dtype=float)

    if len(pairs) > 0:
        i_idx = pairs[:, 0]
        j_idx = pairs[:, 1]

        dx = state.x[j_idx] - state.x[i_idx]
        dist = np.linalg.norm(dx, axis=1) + 1e-9
        phase_diff = state.phi[j_idx] - state.phi[i_idx]
        omega_diff = np.abs(state.omega[j_idx] - state.omega[i_idx])

        resonance_weight = np.exp(-omega_diff / max(params.omega_bandwidth, 1e-9))
        spatial_weight = np.exp(-(dist**2) / (2.0 * params.interaction_radius**2))
        weight = resonance_weight * spatial_weight

        sin_term = np.sin(phase_diff)
        cos_term = np.cos(phase_diff)

        np.add.at(phase_coupling, i_idx, weight * sin_term)
        np.add.at(phase_coupling, j_idx, -weight * sin_term)

        temporal_pair = weight * cos_term
        np.add.at(temporal_shift, i_idx, temporal_pair)
        np.add.at(temporal_shift, j_idx, temporal_pair)

        direction = dx / dist[:, None]
        pull_term = (weight * sin_term)[:, None] * direction
        np.add.at(pull, i_idx, pull_term)
        np.add.at(pull, j_idx, -pull_term)

    neighbor_count = np.maximum(1.0, np.bincount(pairs.ravel(), minlength=n).astype(float) if len(pairs) > 0 else np.ones(n))

    dphi = state.omega + params.coupling * (phase_coupling / neighbor_count)
    dphi += rng.normal(0.0, params.phase_noise, size=n)
    phi_new = (state.phi + params.dt * dphi) % (2.0 * np.pi)

    drift = params.drift_speed * np.stack([np.cos(state.phi), np.sin(state.phi)], axis=1)
    if dims > 2:
        pad = np.zeros((n, dims - 2))
        drift = np.concatenate([drift, pad], axis=1)

    x_new = state.x + params.dt * (drift + params.coupling * pull / neighbor_count[:, None])
    x_new += rng.normal(0.0, params.position_noise, size=x_new.shape)

    t_res_new = state.t_res + params.dt * (
        1.0 + params.temporal_coupling * temporal_shift / neighbor_count
    )
    t_res_new += rng.normal(0.0, params.t_res_noise, size=n)

    coherence = compute_global_coherence(phi_new, state.omega)
    return DLTState(x=x_new, phi=phi_new, omega=state.omega, t_res=t_res_new), coherence


def run_simulation(
    params: DLTParams,
    seed: Optional[int] = None,
    log_trajectory: bool = False,
) -> tuple[DLTState, DLTLog]:
    rng = np.random.default_rng(seed)
    state = initialize_state(params, seed=seed)

    trajectory = None
    if log_trajectory:
        trajectory = np.zeros((params.steps, params.num_objects, params.dimensions), dtype=float)

    coherence_values = np.zeros(params.steps, dtype=float)

    for step in range(params.steps):
        state, coherence = update_state(state, params, rng)
        coherence_values[step] = coherence
        if trajectory is not None:
            trajectory[step] = state.x

    return state, DLTLog(trajectory=trajectory, coherence=coherence_values)


def animate_simulation(
    params: DLTParams,
    seed: Optional[int] = None,
    interval_ms: int = 25,
    save_path: Optional[Path] = None,
) -> None:
    rng = np.random.default_rng(seed)
    state = initialize_state(params, seed=seed)

    fig, (ax_space, ax_coh) = plt.subplots(1, 2, figsize=(12, 5))

    xlim = (-params.world_size, params.world_size)
    ylim = (-params.world_size, params.world_size)

    coherence_series: list[float] = []
    coherence_line, = ax_coh.plot([], [], color="tab:blue", lw=2)
    ax_coh.set_title("Global resonance coherence")
    ax_coh.set_xlabel("Step")
    ax_coh.set_ylabel("Coherence")
    ax_coh.set_ylim(0.0, 1.05)

    scatter = ax_space.scatter(
        state.x[:, 0],
        state.x[:, 1],
        c=state.omega,
        s=22,
        cmap="viridis",
        alpha=0.85,
        edgecolor="none",
    )
    cbar = fig.colorbar(scatter, ax=ax_space)
    cbar.set_label("Resonance frequency ω")
    ax_space.set_title("DLT spatial re-localization")
    ax_space.set_xlim(*xlim)
    ax_space.set_ylim(*ylim)
    ax_space.set_xlabel("x")
    ax_space.set_ylabel("y")

    def _frame(step: int):
        nonlocal state
        state, coherence = update_state(state, params, rng)

        coherence_series.append(coherence)
        if len(coherence_series) > params.coherence_window:
            coherence_series.pop(0)

        scatter.set_offsets(state.x[:, :2])
        scatter.set_sizes(10 + 35 * np.clip((state.t_res - np.min(state.t_res)) / (np.ptp(state.t_res) + 1e-9), 0.0, 1.0))

        x_vals = np.arange(len(coherence_series))
        coherence_line.set_data(x_vals, coherence_series)
        ax_coh.set_xlim(0, max(params.coherence_window, len(coherence_series)))

        ax_space.set_title(f"DLT re-localization (step={step}, coherence={coherence:.3f})")
        return scatter, coherence_line

    anim = FuncAnimation(fig, _frame, frames=params.steps, interval=interval_ms, blit=False)

    if save_path is not None:
        anim.save(save_path, dpi=120)
    else:
        plt.tight_layout()
        plt.show()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dynamic Location Theory (DLT) simulation prototype")
    parser.add_argument("--num-objects", type=int, default=200)
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--omega-min", type=float, default=0.0)
    parser.add_argument("--omega-max", type=float, default=2.5)
    parser.add_argument("--coupling", type=float, default=1.0)
    parser.add_argument("--noise", type=float, default=0.03, help="Phase noise amplitude")
    parser.add_argument("--position-noise", type=float, default=0.01)
    parser.add_argument("--speed", type=float, default=0.2, help="Drift speed")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--animate", action="store_true", help="Run live animation")
    parser.add_argument("--log-trajectories", action="store_true", help="Store trajectory data")
    parser.add_argument("--save-log", type=Path, default=None, help="Path to save npz log")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    params = DLTParams(
        num_objects=args.num_objects,
        steps=args.steps,
        omega_min=args.omega_min,
        omega_max=args.omega_max,
        coupling=args.coupling,
        phase_noise=args.noise,
        position_noise=args.position_noise,
        drift_speed=args.speed,
    )

    if args.animate:
        animate_simulation(params, seed=args.seed)
        return

    _, log = run_simulation(params, seed=args.seed, log_trajectory=args.log_trajectories)
    print(
        f"Done. Final coherence={log.coherence[-1]:.4f}; "
        f"mean coherence={np.mean(log.coherence):.4f}"
    )

    if args.save_log is not None:
        save_data = {"coherence": log.coherence}
        if log.trajectory is not None:
            save_data["trajectory"] = log.trajectory
        np.savez(args.save_log, **save_data)
        print(f"Saved log to {args.save_log}")


if __name__ == "__main__":
    main()
