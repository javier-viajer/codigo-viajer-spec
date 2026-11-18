"""
=============================================================================
[Nombre del Módulo] — TRCG v1.2.0
STATUS: Nivel II (operativo y auditable / prototipo analítico)
SUPUESTO: [Ej: Campo prototipo no lineal / optimización convexa de momentos]
NO AFIRMA: [Ej: No es ley universal de la gravedad ni teorema físico cerrado]
-----------------------------------------------------------------------------
[Resto del docstring y código...]
"""

```text
TRCG — Auditoría Helmholtz–Hodge discreta v1.1
(Euclídea + Fisher ponderada D_g)

Respuesta al panel de 4º Factor:
1) Se mantiene P = I - D^T (DD^T)^† D
2) Se añaden: análisis de rango/modos nulos, bordes, y D_g
3) Las pruebas numéricas NO sustituyen la demostración; se separan
   PROPOSICIÓN ANALÍTICA vs VERIFICACIÓN NUMÉRICA
4) Límite declarado: malla cartesiana en el plano (u,v) del 2-símplex;
   bordes con diferencias one-sided; geometría Fisher aproximada por
   densidades ρ = √det g en nodos interiores

Dependencia: numpy
```

```python
import numpy as np
from numpy.linalg import norm, pinv, matrix_rank, svd

# ============================================================
# TRCG | Helmholtz–Hodge discreto v1.1
# D (euclídeo) y D_g (Fisher ponderado)
# ============================================================

BARY = np.ones(3) / 3.0


# ---------- Notas analíticas (no son “pruebas por print”) ----------
#
# PROPOSICIÓN (álgebra lineal finita):
# Sea D: R^m -> R^k una matriz real. Definimos
# P = I - D^T (D D^T)^† D
# Entonces, en aritmética exacta:
# (i) P^2 = P (proyector)
# (ii) D P = 0 (im P ⊂ ker D)
# (iii) P^T = P (ortogonal w.r.t. producto euclídeo)
# (iv) im(I-P) = im(D^T) (complemento de gradientes discretos)
# Demostración: identidades estándar de la pseudoinversa de Moore-Penrose
# sobre el operador A = D, usando A A^† A = A y (A A^†)^T = A A^†.
# Las pruebas numéricas solo controlan el error de redondeo / rcond.
#
# MODOS NULOS DE (DD^T):
# rank(DD^T) = rank(D). Si rank(D) < k, (DD^T) tiene núcleo no trivial
# y la † es obligatoria. En mallas con condiciones tipo Neumann discretas
# suele aparecer al menos un modo casi-nulo asociado a compatibilidad
# integral de la divergencia.
#
# BORDES:
# Interior: diferencias centrales.
# Borde: one-sided de primer orden. Esto define un operador concreto y
# auditable; no pretende ser todavía un elemento finito ni un esquema
# espectral en el simplex curvo.
#
# FISHER:
# En 2D, div_g V = (1/ρ) ∂_a (ρ V^a) con ρ = √det g.
# Por tanto D_g := diag(1/ρ) D diag(ρ,ρ) sobre los dos bloques del campo.
# ============================================================


def e_basis():
    e1 = np.array([1.0, -1.0, 0.0]); e1 /= norm(e1)
    e2 = np.array([1.0, 1.0, -2.0]); e2 /= norm(e2)
    return e1, e2


def from_uv(u, v):
    e1, e2 = e_basis()
    return BARY + u * e1 + v * e2


def fisher_metric_uv(x):
    """Pullback de g_ij = δ_ij / x_i al plano tangente (e1, e2)."""
    e1, e2 = e_basis()
    G = np.diag(1.0 / np.clip(np.asarray(x, float), 1e-12, None))
    return np.array([
        [e1 @ G @ e1, e1 @ G @ e2],
        [e2 @ G @ e1, e2 @ G @ e2],
    ])


def rho_fisher(x):
    return float(np.sqrt(max(np.linalg.det(fisher_metric_uv(x)), 1e-18)))


def make_grid(n=15, half=0.20):
    xs = np.linspace(-half, half, n)
    ys = np.linspace(-half, half, n)
    U, V = np.meshgrid(xs, ys, indexing="ij")
    h = xs[1] - xs[0]
    return U, V, h, n


def discrete_div_operator(n, h):
    """
    D: R^{2n^2} -> R^{n^2}
    Campo empaquetado [Vu; Vv]
    div ≈ ∂u Vu + ∂v Vv
    """
    N = n * n
    D = np.zeros((N, 2 * N))

    def idx(i, j):
        return i * n + j

    for i in range(n):
        for j in range(n):
            row = idx(i, j)
            # ∂u Vu
            if 0 < i < n - 1:
                D[row, idx(i + 1, j)] += 0.5 / h
                D[row, idx(i - 1, j)] -= 0.5 / h
            elif i == 0:
                D[row, idx(1, j)] += 1.0 / h
                D[row, idx(0, j)] -= 1.0 / h
            else:
                D[row, idx(i, j)] += 1.0 / h
                D[row, idx(i - 1, j)] -= 1.0 / h
            # ∂v Vv
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
    D_g = diag(1/ρ) D diag(ρ, ρ)
    con ρ_i = √det g(x(u_i,v_i))
    """
    N = n * n
    rho = np.zeros(N)
    for i in range(n):
        for j in range(n):
            p = from_uv(U[i, j], V[i, j])
            p = np.clip(p, 1e-10, None)
            p = p / p.sum()
            rho[i * n + j] = rho_fisher(p)
    D = discrete_div_operator(n, h)
    W = np.concatenate([rho, rho])
    Dg = np.diag(1.0 / (rho + 1e-15)) @ D @ np.diag(W)
    return Dg, rho


def build_projector(Dop, rcond=1e-10):
    """
    P = I - D^T (DD^T)^† D
    + diagnóstico de espectro de DD^T
    """
    DDT = Dop @ Dop.T
    s = svd(DDT, compute_uv=False)
    smax = float(s.max()) if s.size else 0.0
    tol = smax * rcond if smax > 0 else rcond
    rank = int(np.sum(s > tol))
    null_modes = DDT.shape[0] - rank
    P = np.eye(Dop.shape[1]) - Dop.T @ pinv(DDT, rcond=rcond) @ Dop
    info = {
        "shape_D": Dop.shape,
        "shape_DDT": DDT.shape,
        "rank_DDT": rank,
        "null_modes_DDT": null_modes,
        "s_max": smax,
        "s_min": float(s.min()) if s.size else 0.0,
        "s_min_over_s_max": float(s.min() / smax) if smax > 0 else np.nan,
        "rcond": rcond,
    }
    return P, info


def pack(Vu, Vv):
    return np.concatenate([Vu.ravel(), Vv.ravel()])


def rms(a):
    a = np.asarray(a)
    return float(np.sqrt(np.mean(a ** 2)))


def algebraic_checks(Dop, P):
    return {
        "idempotencia ||P²-P||/||P||": norm(P @ P - P) / (norm(P) + 1e-15),
        "nucleo ||D P||/||D||": norm(Dop @ P) / (norm(Dop) + 1e-15),
        "simetria ||P-P.T||/||P||": norm(P - P.T) / (norm(P) + 1e-15),
    }


def sample_mixed(U, V):
    Vu = -V + 0.4 * U + 0.05 * np.sin(6 * U)
    Vv = U + 0.4 * V + 0.05 * np.cos(6 * V)
    return Vu, Vv


if __name__ == "__main__":
    n = 15
    U, V, h, n = make_grid(n=n, half=0.20)

    D = discrete_div_operator(n, h)
    Dg, rho = discrete_div_operator_fisher(n, h, U, V)

    P, infoE = build_projector(D)
    Pg, infoF = build_projector(Dg)

    print("=" * 64)
    print("TRCG | Helmholtz–Hodge v1.1 (D euclídeo + D_g Fisher)")
    print("=" * 64)
    print(f"Malla {n}x{n} | h={h:.6f} | nodos={n*n}")
    print()

    print("[A] Diagnóstico DD^T (euclídeo)")
    for k, v in infoE.items():
        print(f" {k}: {v}")
    print("[A] Checks algebraicos P_eucl")
    for k, v in algebraic_checks(D, P).items():
        print(f" {k}: {v:.3e}")
    print()

    print("[B] Diagnóstico DD^T (Fisher D_g)")
    for k, v in infoF.items():
        print(f" {k}: {v}")
    print("[B] Checks algebraicos P_fisher")
    for k, v in algebraic_checks(Dg, Pg).items():
        print(f" {k}: {v:.3e}")
    print()

    Vu, Vv = sample_mixed(U, V)
    v = pack(Vu, Vv)

    print("[C] Residuos de divergencia (campo mixto)")
    print(f" ||D v||_rms = {rms(D @ v):.3e}")
    print(f" ||D (P v)||_rms = {rms(D @ (P @ v)):.3e}")
    print(f" ||D_g v||_rms = {rms(Dg @ v):.3e}")
    print(f" ||D_g (P_g v)||_rms = {rms(Dg @ (Pg @ v)):.3e}")
    print()
    print("[D] No equivalencia de geometrías")
    print(f" ||D_g (P v)||_rms = {rms(Dg @ (P @ v)):.3e} # eucl-solenoidal ≠ Fisher-solenoidal")
    print(f" ||D (P_g v)||_rms = {rms(D @ (Pg @ v)):.3e}")
    print()
    print("Límites declarados:")
    print(" - Proposición algebraica de P: analítica (Moore-Penrose).")
    print(" - Números: solo verificación de redondeo/rcond/discretización.")
    print(" - Bordes: one-sided; dominio = carta (u,v), no FEM curvo completo.")
    print(" - D_g: aproximación nodal ρ=√det g; siguiente paso = validar torsión TRCG con P_g.")
    print("=" * 64)
```
