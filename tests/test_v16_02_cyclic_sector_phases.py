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

# Reference azimuthal angles per sector k in {0..3}
phi_sector_base = sectors * (np.pi / 2.0)

# Upper triangle indices for the 276 unique undirected edges (i < l)
iu, ju = np.triu_indices(N, k=1)
stratum_masks = [strata == (j + 1) for j in range(NUM_STRATA)]
sector_masks = [sectors == k for k in range(NUM_SECTORS)]


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


def sector_apical_drive(sym_mat):
    """Normalized per-sector parabolic/stratum drive chi_k."""
    row_sums = np.sum(sym_mat, axis=1)
    drives = np.zeros(NUM_SECTORS)
    for k in range(NUM_SECTORS):
        mask_k = sector_masks[k]
        drives[k] = np.sum(g_vec[mask_k] * row_sums[mask_k])
    mean_d = np.mean(drives)
    return (drives - mean_d) / (mean_d + 1e-12)


def step_cyclic(R_mat, theta_vec, gamma, kappa, coup_strength, asym_bias=0.25):
    """One discrete step of (R, theta_0..theta_3) with cyclic sector coupling."""
    v = dominant_eigenvector(R_mat)
    gv = g_vec * v
    base_edge = (gv[iu] * gv[ju]) ** gamma

    th_node = theta_vec[sectors]
    if kappa != 0.0:
        phase_kernel = np.exp(
            kappa * (np.cos(4.0 * (phi_sector_base[iu] - th_node[iu])) +
                     np.cos(4.0 * (phi_sector_base[ju] - th_node[ju])))
        )
        edge_weights = base_edge * phase_kernel
    else:
        edge_weights = base_edge

    denom = np.sum(edge_weights)
    n_edge = C0 * (edge_weights / denom) if denom > 0.0 else np.full_like(edge_weights, C0 / len(edge_weights))

    N_mat = np.zeros((N, N))
    N_mat[iu, ju] = n_edge
    N_mat[ju, iu] = n_edge

    R_next = (1.0 - MU) * R_mat + MU * N_mat

    chi = sector_apical_drive(R_next)
    theta_next = np.zeros(NUM_SECTORS)
    for k in range(NUM_SECTORS):
        k_fwd = (k + 1) % NUM_SECTORS
        k_bwd = (k - 1) % NUM_SECTORS
        fwd_term = (1.0 + asym_bias) * np.sin(theta_vec[k_fwd] - theta_vec[k] + chi[k])
        bwd_term = (1.0 - asym_bias) * np.sin(theta_vec[k_bwd] - theta_vec[k] - chi[k])
        theta_next[k] = theta_vec[k] + coup_strength * (fwd_term + bwd_term)

    p_next = stratum_masses(R_next) / C0
    return R_next, theta_next, theta_next - theta_vec, p_next


def make_initial_state(seed=2026, eps=1e-2):
    rng = np.random.default_rng(seed)
    pert = 1.0 + eps * rng.standard_normal(len(iu))
    pert = np.clip(pert, 1e-3, None)
    edges = C0 * pert / np.sum(pert)
    R_mat = np.zeros((N, N))
    R_mat[iu, ju] = edges
    R_mat[ju, iu] = edges
    theta_vec = 0.1 * rng.standard_normal(NUM_SECTORS)
    return R_mat, theta_vec


def jacobian_280(R_mat, theta_vec, gamma, kappa, coup_strength, eps_fd=1e-6):
    """Central finite-difference Jacobian on (276 unique edges, theta_0..theta_3)."""
    def pack(M, th):
        return np.concatenate([M[iu, ju], th])

    def unpack(vec):
        e = vec[:-NUM_SECTORS]
        th = vec[-NUM_SECTORS:]
        M = np.zeros((N, N))
        M[iu, ju] = e
        M[ju, iu] = e
        return M, th

    z0 = pack(R_mat, theta_vec)
    dim = len(z0)
    J = np.zeros((dim, dim))
    for idx in range(dim):
        dz = np.zeros(dim)
        dz[idx] = eps_fd
        mp, thp, *_ = step_cyclic(*unpack(z0 + dz), gamma=gamma, kappa=kappa, coup_strength=coup_strength)
        mm, thm, *_ = step_cyclic(*unpack(z0 - dz), gamma=gamma, kappa=kappa, coup_strength=coup_strength)
        J[:, idx] = (pack(mp, thp) - pack(mm, thm)) / (2.0 * eps_fd)
    return J


def run_cyclic_probe(gamma=1.5, kappa=0.5, warmup=300, window=80):
    print(f"=== Cyclic Sector Phases (theta_0..3) Probe: gamma={gamma}, kappa={kappa} ===")
    for coup_strength in [0.0, 0.1, 0.25, 0.5, 1.0]:
        R_mat, theta_vec = make_initial_state(seed=2026, eps=1e-2)
        dth_win, p_win = [], []

        for t in range(warmup + window):
            R_mat, theta_vec, dth_vec, p_next = step_cyclic(
                R_mat, theta_vec, gamma=gamma, kappa=kappa, coup_strength=coup_strength
            )
            if t >= warmup:
                dth_win.append(np.mean(dth_vec))
                p_win.append(p_next)

        p_arr = np.array(p_win)
        axial_span = float(np.max(np.abs(p_arr[-1] - p_arr[0])))
        mean_dth = float(np.mean(dth_win))
        omega_apical = float(p_arr[-1, -1])

        J = jacobian_280(R_mat, theta_vec, gamma=gamma, kappa=kappa, coup_strength=coup_strength)
        eigs = np.linalg.eigvals(J)
        complex_eigs = [ev for ev in eigs if abs(ev.imag) > 1e-6]
        if complex_eigs:
            dom_c = max(complex_eigs, key=abs)
            mod_c = float(abs(dom_c))
            ang_c = float(abs(np.angle(dom_c)))
            n_c = len(complex_eigs)
        else:
            mod_c, ang_c, n_c = 0.0, 0.0, 0

        print(
            f"coup={coup_strength:4.2f} | Omega={omega_apical:.4f} | mean_dth={mean_dth:+.2e} | "
            f"|eig_C|={mod_c:.5f}, arg={ang_c:.4f}, n_C={n_c} | max|dp|={axial_span:.2e}"
        )


if __name__ == "__main__":
    run_cyclic_probe(gamma=1.5, kappa=0.5, warmup=300, window=80)
