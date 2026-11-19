import numpy as np
from numpy.linalg import norm, pinv, svd

# ============================================================
# TRCG | Helmholtz–Hodge discreto v1.1 (torsion.py)
# Operador euclideo D, operador ponderado Fisher D_g
# y proyectores ortogonales P / P_g con diagnostico de rango
# ============================================================

BARY = np.ones(3) / 3.0


# ---------- Notas analiticas ----------
#
# PROPOSICION (algebra lineal finita):
# Sea D: R^m -> R^k una matriz real. Definimos:
# P = I - D^T (D D^T)^† D
# En aritmetica exacta se cumple:
# (i) P^2 = P (idempotencia / proyector)
# (ii) D P = 0 (im(P) contenido en ker(D))
# (iii) P^T = P (simetria / ortogonalidad euclidea)
# (iv) im(I - P) = im(D^T) (complemento de gradientes discretos)
#
# MODOS NULOS DE (D D^T):
# rank(D D^T) = rank(D). Si rank(D) < k, (D D^T) tiene nucleo no
# trivial y el uso de la pseudoinversa de Moore-Penrose es necesario.
# En esquemas discretos sobre mallas finitas suelen aparecer modos
# casi-nulos ligados a condiciones de borde y compatibilidad integral.
#
# BORDES:
# Interior: diferencias centrales de segundo orden.
# Frontera: diferencias one-sided de primer orden.
# Limite declarado: carta cartesiana (u, v) sobre el 2-simplex; no
# sustituye un elemento finito o esquema espectral en variedad curva.
#
# FISHER (D_g):
# En 2D, div_g V = (1 / rho) * d_a (rho * V^a) con rho = sqrt(det g).
# Definimos D_g = diag(1 / rho) @ D @ diag(rho, rho) sobre los bloques
# del campo vectorial.
# ============================================================


def e_basis():
    """Base ortonormal del plano tangente al 2-simplex."""
    e1 = np.array([1.0, -1.0, 0.0])
    e1 /= norm(e1)
    e2 = np.array([1.0, 1.0, -2.0])
    e2 /= norm(e2)
    return e1, e2


def from_uv(u, v):
    """Proyecta coordenadas (u, v) al espacio baricentrico."""
    e1, e2 = e_basis()
    return BARY + u * e1 + v * e2


def fisher_metric_uv(x):
    """Pullback de la metrica de Fisher g_ij = delta_ij / x_i a (u, v)."""
    e1, e2 = e_basis()
    x_safe = np.clip(np.asarray(x, dtype=float), 1e-12, None)
    G = np.diag(1.0 / x_safe)
    return np.array([
        [e1 @ G @ e1, e1 @ G @ e2],
        [e2 @ G @ e1, e2 @ G @ e2],
    ], dtype=float)


def rho_fisher(x):
    """Densidad escalar rho = sqrt(det g) en un punto baricentrico."""
    det_g = float(np.linalg.det(fisher_metric_uv(x)))
    return float(np.sqrt(max(det_g, 1e-18)))


def make_grid(n=15, half=0.20):
    """Genera malla uniforme n x n en [-half, half]^2."""
    xs = np.linspace(-half, half, n)
    ys = np.linspace(-half, half, n)
    U, V = np.meshgrid(xs, ys, indexing="ij")
    h = float(xs[1] - xs[0])
    return U, V, h, n


def discrete_div_operator(n, h):
    """
    Construye D: R^{2 n^2} -> R^{n^2} para campo empaquetado [Vu; Vv].
    Divergencia discreta: div V ≈ du Vu + dv Vv.
    """
    N = n * n
    D = np.zeros((N, 2 * N), dtype=float)

    def idx(i, j):
        return i * n + j

    for i in range(n):
        for j in range(n):
            row = idx(i, j)

            # Derivada parcial respecto a u sobre Vu
            if 0 < i < n - 1:
                D[row, idx(i + 1, j)] += 0.5 / h
                D[row, idx(i - 1, j)] -= 0.5 / h
            elif i == 0:
                D[row, idx(1, j)] += 1.0 / h
                D[row, idx(0, j)] -= 1.0 / h
            else:
                D[row, idx(i, j)] += 1.0 / h
                D[row, idx(i - 1, j)] -= 1.0 / h

            # Derivada parcial respecto a v sobre Vv
            off = N
            if 0 < j < n - 1:
                D[row, off + idx(i, j + 1)] += 0.5 / h
                D[row, off + idx(i, j - 1)] -= 0.5 / h
            elif j == 0:
                D[row, off + idx(i, 1)] += 1.0 / h
                D[row, off + idx(i, 0)] -= 1.0 / h
            else:
                D[row, off + idx(i, j)] += 1.0 / h
                D[row, off + idx(i, j - 1)] -= 1.0 / h

    return D


def discrete_div_operator_fisher(n, h, U, V):
    """
    Construye D_g = diag(1/rho) @ D @ diag(rho, rho)
    con rho_k = sqrt(det g(x(u_k, v_k))).
    """
    N = n * n
    rho = np.zeros(N, dtype=float)

    for i in range(n):
        for j in range(n):
            p = from_uv(U[i, j], V[i, j])
            p = np.clip(p, 1e-10, None)
            p = p / np.sum(p)
            rho[i * n + j] = rho_fisher(p)

    D = discrete_div_operator(n, h)
    W = np.concatenate([rho, rho])
    Dg = np.diag(1.0 / (rho + 1e-15)) @ D @ np.diag(W)
    return Dg, rho


def build_projector(Dop, rcond=1e-10):
    """
    Construye P = I - D^T (D D^T)^† D y devuelve diagnostico espectral
    de D D^T (rango efectivo y modos nulos).
    """
    DDT = Dop @ Dop.T
    s = svd(DDT, compute_uv=False)
    smax = float(s.max()) if s.size else 0.0
    smin = float(s.min()) if s.size else 0.0
    tol = smax * rcond if smax > 0.0 else rcond
    rank = int(np.sum(s > tol))
    null_modes = int(DDT.shape[0] - rank)

    P = np.eye(Dop.shape[1], dtype=float) - Dop.T @ pinv(DDT, rcond=rcond) @ Dop

    info = {
        "shape_D": Dop.shape,
        "shape_DDT": DDT.shape,
        "rank_DDT": rank,
        "null_modes_DDT": null_modes,
        "s_max": smax,
        "s_min": smin,
        "s_min_over_s_max": float(smin / smax) if smax > 0.0 else np.nan,
        "rcond": rcond,
    }
    return P, info


def pack(Vu, Vv):
    """Empaqueta componentes (Vu, Vv) en un vector columna."""
    return np.concatenate([Vu.ravel(), Vv.ravel()])


def rms(a):
    """Raiz de la media cuadratica."""
    arr = np.asarray(a, dtype=float)
    return float(np.sqrt(np.mean(arr ** 2)))


def algebraic_checks(Dop, P):
    """Verifica numéricamente las identidades del proyector."""
    return {
        "idempotencia ||P^2-P||/||P||": norm(P @ P - P) / (norm(P) + 1e-15),
        "nucleo ||D P||/||D||": norm(Dop @ P) / (norm(Dop) + 1e-15),
        "simetria ||P-P.T||/||P||": norm(P - P.T) / (norm(P) + 1e-15),
    }


def sample_mixed(U, V):
    """Campo de prueba con componentes rotacionales, radiales y oscilatorias."""
    Vu = -V + 0.4 * U + 0.05 * np.sin(6.0 * U)
    Vv = U + 0.4 * V + 0.05 * np.cos(6.0 * V)
    return Vu, Vv


if __name__ == "__main__":
    n = 15
    U, V, h, n = make_grid(n=n, half=0.20)

    D = discrete_div_operator(n, h)
    Dg, rho = discrete_div_operator_fisher(n, h, U, V)

    P, infoE = build_projector(D)
    Pg, infoF = build_projector(Dg)

    print("=" * 64)
    print("TRCG | Helmholtz-Hodge v1.1 (D euclideo + D_g Fisher)")
    print("=" * 64)
    print(f"Malla {n}x{n} | h={h:.6f} | nodos={n*n}")
    print()

    print("[A] Diagnostico DD^T (euclideo)")
    for k, v in infoE.items():
        print(f" {k}: {v}")
    print("[A] Checks algebraicos P_eucl")
    for k, v in algebraic_checks(D, P).items():
        












    
           






     

   

