import numpy as np

N = 24
NUM_STRATA = 6
NUM_SECTORS = 4
C0 = 1.0
MU = 0.2
GAMMA_C = N / (N - 2.0) # 12/11 ≈ 1.090909

node_idx = np.arange(N)
sectors = node_idx // NUM_STRATA # 0..3
strata = (node_idx % NUM_STRATA) + 1 # 1..6

# Parabolic geometry: H = 10.0, z_j = j -> g_j = (1 - z_j/H)^(-1/2)
H = 10.0
z_strata = strata.astype(float)
g_vec = 1.0 / np.sqrt(1.0 - z_strata / H)

# Upper triangle indices for the 276 unique undirected edges (i < l)
iu, ju = np.triu_indices(N, k=1)
stratum_masks = [strata == (j + 1) for j in range(NUM_STRATA)]


def dominant_eigenvector(R_mat):
    """Non-negative dominant eigenvector v with ||v||_2 = 1."""
    _, vecs = np.linalg.eigh(R_mat)
    v = np.abs(vecs[:, -1])
    norm = np.linalg.norm(v)
    return v / norm if norm > 0.0 else np.full(N, 1.0 / np.sqrt(N))


def stratum_masses(sym_mat):
    """Single-edge convention: 0.5 * sum_{i in S_j} sum_{l != i} sym_mat[i,l]."""
    row_sums = np.sum(sym_mat, axis=1)
    return np.array([0.5 * np.sum(row_sums[mask]) for mask in stratum_masks])


def step_baseline(R_mat, gamma):
    """One baseline step on (R) with parabolic weights g_j and exponent gamma."""
    v = dominant_eigenvector(R_mat)
    gv = g_vec * v
    edge_weights = (gv[iu] * gv[ju]) ** gamma
    denom = np.sum(edge_weights)
    n_edge = C0 * (edge_weights / denom) if denom > 0.0 else np.full_like(edge_weights, C0 / len(edge_weights))

    N_mat = np.zeros((N, N))
    N_mat[iu, ju] = n_edge
    N_mat[ju, iu] = n_edge

    R_next = (1.0 - MU) * R_mat + MU * N_mat
    p_next = stratum_masses(R_next) / C0
    return R_next, p_next


def make_initial_state(seed=2026, eps=1e-2):
    rng = np.random.default_rng(seed)
    pert = 1.0 + eps * rng.standard_normal(len(iu))
    pert = np.clip(pert, 1e-3, None)
    edges = C0 * pert / np.sum(pert)
    R_mat = np.zeros((N, N))
    R_mat[iu, ju] = edges
    R_mat[ju, iu] = edges
    return R_mat


def run_baseline_checks(steps=300):
    print(f"=== TRCG v1.6 Baseline Checks (N={N}, edges={len(iu)}, gamma_c={GAMMA_C:.6f}) ===")
    for gamma in [0.8, 1.0, GAMMA_C, 1.5]:
        R_mat = make_initial_state(seed=2026, eps=1e-2)
        total_mass_err = 0.0
        for _ in range(steps):
            R_mat, p_next = step_baseline(R_mat, gamma=gamma)
            total_mass = float(np.sum(R_mat[iu, ju]))
            total_mass_err = max(total_mass_err, abs(total_mass - C0))
        omega_apical = float(p_next[-1])
        print(
            f"gamma={gamma:8.5f} | max|sum(R)-C0|={total_mass_err:.2e} | "
            f"Omega_apical={omega_apical:.6f} | p_strata={np.round(p_next, 4)}"
        )


if __name__ == "__main__":
    run_baseline_checks(steps=300)
