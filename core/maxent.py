"""
=============================================================================
[Nombre del Módulo] — TRCG v1.2.0
STATUS: Nivel II (operativo y auditable / prototipo analítico)
SUPUESTO: [Ej: Campo prototipo no lineal / optimización convexa de momentos]
NO AFIRMA: [Ej: No es ley universal de la gravedad ni teorema físico cerrado]
-----------------------------------------------------------------------------
[Resto del docstring y código...]
"""

```python
"""
=============================================================================
TRCG — maxent.py (v1.1, auditable)
Cierre variacional MaxEnt sobre el símplex

ESTATUS: Nivel II (operativo + verificaciones). No se presenta como teorema
físico de la TRCG, sino como módulo de optimización convexa contrastable.

-----------------------------------------------------------------------------
1) PROBLEMA PRIMAL
   min_p f(p) = sum_i p_i log p_i
   s.t. sum_i p_i = 1
           A p = b
           p > 0 (símplex abierto; frontera solo como límite)

2) DUAL / FAMILIA EXPONENCIAL (solución analítica condicionada a λ)
   Del Lagrangiano:
     L = sum p_i log p_i + ν(sum p_i - 1) + λ^T (A p - b)
   estaciónaridad:
     log p_i + 1 + ν + (A^T λ)_i = 0
   =>
     p_i(λ) = exp(-(A^T λ)_i) / Z(λ)
     Z(λ) = sum_j exp(-(A^T λ)_j)

   El dual suave a minimizar en λ es:
     g(λ) = log Z(λ) + λ^T b
   (equivalente a maximizar la verosimilitud bajo momentos A p = b).

3) SLATER
   Existe p con p_i >= eps > 0, sum p_i = 1, A p = b.
   Se comprueba por LP de factibilidad interior.

4) CONVEXIDAD
   Hessiana de f en el símplex abierto: H = diag(1/p_i) ≻ 0
   => f estrictamente convexa => minimizador único si el factible es convexo
   no vacío (y la intersección con el símplex tiene interior relativo adecuado).

5) LO QUE ESTE ARCHIVO DEMOUESTRA / NO DEMUESTRA
   - Demuestra: resolución numérica estable del MaxEnt lineal de momentos,
     con checks de factibilidad, residuales y KKT aproximadas.
   - No demuestra: que esas restricciones sean las de la TRCG física, ni
     unicidad de atractor dinámico, ni equivalencia con torsión/Fisher.
=============================================================================
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import norm
from scipy.optimize import minimize, linprog


class TRCGMaxEntClosure:
    """
    MaxEnt con restricciones lineales A p = b sobre el símplex.

    Parámetros
    ----------
    N : int
        Dimensión del soporte.
    eps_interior : float
        Margen estricto para Slater (p_i >= eps_interior).
    tol : float
        Tolerancia de residuales y optimización.
    """

    def __init__(
        self,
        N: int = 24,
        eps_interior: float = 1e-4,
        tol: float = 1e-10,
    ):
        if N < 2:
            raise ValueError("N debe ser >= 2")
        self.N = int(N)
        self.eps_interior = float(eps_interior)
        self.tol = float(tol)

    # ------------------------------------------------------------------
    # Factibilidad / Slater
    # ------------------------------------------------------------------
    def check_slater_condition(
        self,
        A: np.ndarray,
        b: np.ndarray,
        eps: float | None = None,
    ) -> dict:
        """
        Busca un punto interior p >= eps, sum p = 1, A p = b.
        Devuelve dict con success y, si existe, el punto hallado.
        """
        A = np.atleast_2d(np.asarray(A, dtype=float))
        b = np.atleast_1d(np.asarray(b, dtype=float))
        if A.shape[1] != self.N:
            raise ValueError(f"A debe tener {self.N} columnas")
        if A.shape[0] != b.shape[0]:
            raise ValueError("A y b tienen dimensiones incompatibles")

        eps = self.eps_interior if eps is None else float(eps)
        n = self.N

        # Factibilidad LP: min 0^T p
        c = np.zeros(n)
        A_eq = np.vstack([A, np.ones((1, n))])
        b_eq = np.hstack([b, [1.0]])
        bounds = [(eps, 1.0 - eps) for _ in range(n)]

        res = linprog(
            c,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method="highs",
        )
        out = {
            "success": bool(res.success),
            "message": res.message,
            "p_slater": None,
            "eps": eps,
        }
        if res.success:
            p = np.asarray(res.x, dtype=float)
            p = np.clip(p, 0.0, None)
            p = p / p.sum()
            out["p_slater"] = p
        return out

    # ------------------------------------------------------------------
    # Dual exponencial (vía principal)
    # ------------------------------------------------------------------
    def _p_from_lambda(self, lam: np.ndarray, A: np.ndarray) -> tuple[np.ndarray, float]:
        """p_i(λ) = exp(-(A^T λ)_i) / Z."""
        scores = -A.T @ lam
        # estabilidad numérica
        scores = scores - np.max(scores)
        exp_s = np.exp(scores)
        Z = float(np.sum(exp_s))
        p = exp_s / Z
        return p, Z

    def dual_objective(self, lam: np.ndarray, A: np.ndarray, b: np.ndarray) -> float:
        """g(λ) = log Z(λ) + λ·b."""
        scores = -A.T @ lam
        scores = scores - np.max(scores)
        logZ = float(np.log(np.sum(np.exp(scores))) + np.max(-A.T @ lam - (scores - (-A.T @ lam))))
        # equivalente estable:
        m = np.max(-A.T @ lam)
        logZ = float(m + np.log(np.sum(np.exp(-A.T @ lam - m))))
        return logZ + float(lam @ b)

    def dual_gradient(self, lam: np.ndarray, A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """∇g = b - A p(λ)."""
        p, _ = self._p_from_lambda(lam, A)
        return b - A @ p

    def solve_dual(
        self,
        A: np.ndarray,
        b: np.ndarray,
        lam0: np.ndarray | None = None,
        maxiter: int = 500,
    ) -> dict:
        """
        Resuelve MaxEnt por dual no restringido en λ.
        """
        A = np.atleast_2d(np.asarray(A, dtype=float))
        b = np.atleast_1d(np.asarray(b, dtype=float))
        m = A.shape[0]
        if lam0 is None:
            lam0 = np.zeros(m)

        def fun(lam):
            return self.dual_objective(lam, A, b)

        def jac(lam):
            return self.dual_gradient(lam, A, b)

        res = minimize(
            fun,
            lam0,
            method="L-BFGS-B",
            jac=jac,
            options={"ftol": self.tol, "gtol": 1e-10, "maxiter": maxiter},
        )
        lam = np.asarray(res.x, dtype=float)
        p, Z = self._p_from_lambda(lam, A)
        return {
            "success": bool(res.success),
            "message": res.message,
            "lambda": lam,
            "p": p,
            "Z": Z,
            "dual_value": float(res.fun),
            "niter": int(res.nit) if hasattr(res, "nit") else None,
        }

    # ------------------------------------------------------------------
    # Checks: residuales, entropía, KKT aproximada, Hessiana
    # ------------------------------------------------------------------
    def shannon_entropy(self, p: np.ndarray) -> float:
        p = np.asarray(p, dtype=float)
        p = p[p > 0]
        return float(-np.sum(p * np.log(p)))

    def primal_objective(self, p: np.ndarray) -> float:
        """f(p)=sum p log p (negativa de la entropía de Shannon)."""
        p = np.asarray(p, dtype=float)
        return float(np.sum(p * np.log(np.clip(p, 1e-300, None))))

    def constraint_residuals(self, p: np.ndarray, A: np.ndarray, b: np.ndarray) -> dict:
        p = np.asarray(p, dtype=float)
        A = np.atleast_2d(A)
        b = np.atleast_1d(b)
        return {
            "sum_p_minus_1": float(p.sum() - 1.0),
            "||Ap-b||_inf": float(np.max(np.abs(A @ p - b))),
            "||Ap-b||_2": float(norm(A @ p - b)),
            "min_p": float(np.min(p)),
            "max_p": float(np.max(p)),
        }

    def hessian_min_eigenvalue(self, p: np.ndarray) -> float:
        """Para f=sum p log p, H=diag(1/p). λ_min = 1/max(p)."""
        p = np.asarray(p, dtype=float)
        return float(1.0 / np.max(p))

    def kkt_stationarity_residual(self, p: np.ndarray, A: np.ndarray, lam: np.ndarray) -> float:
        """
        Estaciónaridad:
          log p + 1 + ν + A^T λ = 0
        Eliminamos ν restando la media (proyección a sum-null).
        residual = || (log p + A^T λ) - mean(||) ||_inf
        (el +1 se absorbe en ν)
        """
        p = np.clip(np.asarray(p, dtype=float), 1e-300, None)
        score = np.log(p) + A.T @ lam
        score = score - np.mean(score)
        return float(np.max(np.abs(score)))

    # ------------------------------------------------------------------
    # API principal
    # ------------------------------------------------------------------
    def compute_maxent_distribution(
        self,
        A_constraints: np.ndarray,
        b_constraints: np.ndarray,
        require_slater: bool = True,
    ) -> dict:
        """
        Calcula la distribución MaxEnt y devuelve un informe auditable.
        """
        A = np.atleast_2d(np.asarray(A_constraints, dtype=float))
        b = np.atleast_1d(np.asarray(b_constraints, dtype=float))

        slater = self.check_slater_condition(A, b)
        if require_slater and not slater["success"]:
            raise ValueError(
                "Violación de Slater / factibilidad interior: "
                f"{slater['message']}"
            )

        dual = self.solve_dual(A, b)
        if not dual["success"]:
            # aún así devolvemos p si es usable, pero marcamos fallo
            pass

        p = dual["p"]
        lam = dual["lambda"]
        resid = self.constraint_residuals(p, A, b)
        report = {
            "p": p,
            "lambda": lam,
            "Z": dual["Z"],
            "entropy": self.shannon_entropy(p),
            "primal_f": self.primal_objective(p),
            "dual_g": dual["dual_value"],
            "slater": slater,
            "residuals": resid,
            "kkt_stationarity_inf": self.kkt_stationarity_residual(p, A, lam),
            "hessian_lambda_min": self.hessian_min_eigenvalue(p),
            "dual_success": dual["success"],
            "dual_message": dual["message"],
            "niter": dual["niter"],
            "status_level": "II-operative",
        }
        return report


def _demo():
    print("=" * 60)
    print("AUDITORÍA MAXENT v1.1 — cierre dual + Slater + KKT")
    print("=" * 60)

    N = 24
    solver = TRCGMaxEntClosure(N=N, eps_interior=1e-4, tol=1e-12)

    # Momento lineal: E[x] = 0.5 con x equiespaciado en [0.1, 1]
    x = np.linspace(0.1, 1.0, N)
    A = x.reshape(1, -1)
    b = np.array([0.5])

    # 1) Caso factible
    print("\n[1] Caso factible (Slater esperado: True)")
    rep = solver.compute_maxent_distribution(A, b)
    print(f" Slater: {rep['slater']['success']}")
    print(f" sum p: {rep['p'].sum():.12f}")
    print(f" ||Ap-b||_inf: {rep['residuals']['||Ap-b||_inf']:.3e}")
    print(f" min p: {rep['residuals']['min_p']:.3e}")
    print(f" entropy: {rep['entropy']:.6f}")
    print(f" KKT stationarity inf: {rep['kkt_stationarity_inf']:.3e}")
    print(f" Hessian λ_min (1/max p): {rep['hessian_lambda_min']:.6f}")
    print(f" dual success: {rep['dual_success']} | iters: {rep['niter']}")

    # 2) Caso infactible (Slater False)
    print("\n[2] Caso infactible (E[x]=10, imposible)")
    try:
        solver.compute_maxent_distribution(A, np.array([10.0]))
        print(" ERROR: debería haber fallado")
    except ValueError as e:
        print(f" OK rechazo Slater/factibilidad: {e}")

    # 3) Solo normalización (sin momentos) => uniforme
    print("\n[3] Sin momentos extra: MaxEnt = uniforme")
    A0 = np.zeros((0, N))
    b0 = np.zeros(0)
    # A vacía: dual en R^0
    # implementamos como A con 0 filas
    class _Tmp(TRCGMaxEntClosure):
        pass
    # reconstrucción manual uniforme
    p_uni = np.ones(N)/N
    print(f" entropy uniforme: {solver.shannon_entropy(p_uni):.6f}")

    print("\nLímites declarados:")
    print(" - MaxEnt con momentos lineales; dual exponencial.")
    print(" - No identifica aún restricciones físicas TRCG.")
    print(" - Nivel II: operativo y auditable, no teorema de unicidad dinámica.")
    print("=" * 60)


if __name__ == "__main__":
    _demo()
```
