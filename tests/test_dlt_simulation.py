import numpy as np

from dlt_simulation import DLTParams, initialize_state, run_simulation, update_state


def test_identical_frequencies_initialization():
    params = DLTParams(num_objects=10, omega_min=1.2, omega_max=1.2)
    state = initialize_state(params, seed=1)
    assert np.allclose(state.omega, 1.2)


def test_update_state_shapes_and_finiteness():
    params = DLTParams(num_objects=50, steps=3)
    state = initialize_state(params, seed=2)
    rng = np.random.default_rng(3)

    new_state, coherence = update_state(state, params, rng)

    assert new_state.x.shape == state.x.shape
    assert new_state.phi.shape == state.phi.shape
    assert new_state.t_res.shape == state.t_res.shape
    assert np.isfinite(new_state.x).all()
    assert np.isfinite(new_state.phi).all()
    assert np.isfinite(new_state.t_res).all()
    assert 0.0 <= coherence <= 1.0


def test_large_object_count_runs():
    params = DLTParams(num_objects=1200, steps=5, interaction_radius=0.25)
    final_state, log = run_simulation(params, seed=4, log_trajectory=False)

    assert final_state.x.shape == (1200, 2)
    assert log.coherence.shape == (5,)
    assert np.isfinite(log.coherence).all()
