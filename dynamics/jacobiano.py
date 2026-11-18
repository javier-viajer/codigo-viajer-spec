"""
=============================================================================
TRCG — jacobiano.py (v1.2.0, auditable)
Jacobiano analítico, espectro local y umbral de bifurcación

ESTATUS: Nivel II (operativo + contraste analítico/numérico).
No se presenta gamma_c = 1 como ley universal de la TRCG, sino como
umbral EXACTO del campo prototipo aquí definido, en el equilibrio x=0.

-----------------------------------------------------------------------------
1) CAMPO VECTORIAL PROTOTIPO
   En R^N (versión sin proyección al símplex; ver límites):

     F_i(x; γ) = -(1-γ) x_i - x_i^3 + m(x) x_i
     m(x) = (1/N) sum_k x_k

   Interpretación:
     - término lineal: -(1-γ) x
     - saturación cúbica: -x^3
     - acoplamiento global por la media: m(x) x

2) JACOBIANO ANALÍTICO
   ∂F_i/∂x_j =
     si i=j: -(1-γ) - 3 x_i^2 + m(x) + x_i/N
     si i≠j: x_i/N

3) EQUILIBRIO x=0
   F(0;γ)=0 para todo γ.
   J(0;γ) = -(1-γ) I
   autovalores: λ = -(1-γ) (multiplicidad N)

   => umbral espectral exacto:
        γ_c = 1
        max Re λ = 0 en γ=1
        estable (local) si γ<1
        inestable si γ>1

   Esto JUSTIFICA γ_c=1 para ESTE campo en x=0. No se exporta como
   teorema general de toda arquitectura piramidal sin más hipótesis.

4) CONTRASTE OBLIGATORIO
   Se exige ||J_analítico - J_numérico|| / ||J_analítico|| pequeña.
   Si falla, el Jacobiano "analítico" no es válido.

5) LÍMITES DECLARADOS
   - Este F no impone sum x_i=1 ni x>0 (no es todavía dinámica MaxEnt/Fisher).
   - La etiqueta "piramidal/parabólico" es interpretativa, no un teorema.
   - Nivel I requeriría el Jacobiano del campo TRCG real (R o T) usado
     en las simulaciones de producción.
=============================================================================
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigvals, norm, eig


class TRCGAnalyticalJacobian:
    """
    Campo prototipo + Jacobiano analítico + espectro + barrido en γ.
    """

    def __init__(self, N: int = 24):
        if N < 1:
            raise ValueError("N debe ser >= 1")
        self.N = int(N)

    # ------------------------------------------------------------------
    # Campo y Jacobiano
    # ------------------------------------------------------------------
    def vector_field(self, x: np.ndarray, gamma: float) -> np.ndarray:
        """F(x;γ) = -(1-γ)x - x^3 + mean(x) x"""
        x = np.asarray(x, dtype=float)
        if x.shape != (self.N,):
            raise ValueError(f"x debe tener forma ({self.N},)")
        m = float(np.mean(x))
        return -(1.0 - gamma) * x - x**3 + m * x

    def analytical_jacobian(self, x: np.ndarray, gamma: float) -> np.ndarray:
        """
        J_ij = ∂F_i/∂x_j (exacto para el campo anterior, sin clip).
        """
        x = np.asarray(x, dtype=float)
        n = self.N
        m = float(np.mean(x))
        J = np.zeros((n, n), dtype=float)
        for i in range(n):
            for j in range(n):
                if i == j:
                    J[i, j] = -(1.0 - gamma) - 3.0 * x[i] ** 2 + m + x[i] / n
                else:
                    J[i, j] = x[i] / n
        return J

    def numerical_jacobian(self, x: np.ndarray, gamma: float, h: float = 1e-7) -> np.ndarray:
        """Jacobiano por diferencias finitas (solo auditoría)."""
        x = np.asarray(x, dtype=float)
        n = self.N
        J = np.zeros((n, n), dtype=float)
        f0 = self.vector_field(x, gamma)
        for j in range(n):
            xp = x.copy()
            xp[j] += h
            J[:, j] = (self.vector_field(xp, gamma) - f0) / h
        return J

    def jacobian_agreement(
        self, x: np.ndarray, gamma: float, h: float = 1e-7
    ) -> dict:
        Ja = self.analytical_jacobian(x, gamma)
        Jn = self.numerical_jacobian(x, gamma, h=h)
        rel = float(norm(Ja - Jn) / (norm(Ja) + 1e-15))
        return {
            "rel_error": rel,
            "abs_error": float(norm(Ja - Jn)),
            "ok": rel < 1e-5,
        }

    # ------------------------------------------------------------------
    # Espectro y estabilidad
    # ------------------------------------------------------------------
    def spectral_report(self, x: np.ndarray, gamma: float) -> dict:
        J = self.analytical_jacobian(x, gamma)
        ev = eigvals(J)
        re = np.real(ev)
        im = np.imag(ev)
        k = int(np.argmax(re))
        return {
            "gamma": float(gamma),
            "eigenvalues": ev,
            "max_real": float(re[k]),
            "argmax_im": float(im[k]),
            "n_unstable": int(np.sum(re > 1e-12)),
            "n_marginal": int(np.sum(np.abs(re) <= 1e-12)),
            "is_stable": bool(np.all(re < -1e-12)),
            "has_complex": bool(np.any(np.abs(im) > 1e-10)),
        }

    def gamma_c_at_zero_equilibrium(self) -> dict:
        """
        Derivación exacta en x=0:
          J(0;γ) = -(1-γ) I
          λ = -(1-γ)
          γ_c = 1
        """
        return {
            "equilibrium": "x=0",
            "J": "-(1-γ) I",
            "lambda": "-(1-γ) (mult. N)",
            "gamma_c": 1.0,
            "stable_iff": "γ < 1",
            "note": "Exacto solo para este campo en x=0",
        }

    def sweep_gamma(
        self,
        x: np.ndarray,
        gammas: np.ndarray | list[float],
    ) -> list[dict]:
        rows = []
        for g in gammas:
            rep = self.spectral_report(x, float(g))
            agree = self.jacobian_agreement(x, float(g))
            rows.append({**rep, **{"jac_rel_error": agree["rel_error"], "jac_ok": agree["ok"]}})
        return rows

    def find_zero_crossing(
        self,
        x: np.ndarray,
        g_min: float = 0.0,
        g_max: float = 2.0,
        n: int = 41,
    ) -> dict:
        """Localiza numéricamente el γ donde max Re λ cruza 0 en el punto x."""
        gs = np.linspace(g_min, g_max, n)
        vals = [self.spectral_report(x, g)["max_real"] for g in gs]
        sign = np.sign(vals)
        cross = None
        for i in range(len(gs) - 1):
            if sign[i] == 0:
                cross = gs[i]
                break
            if sign[i] * sign[i + 1] < 0:
                # interpolación lineal
                t = vals[i] / (vals[i] - vals[i + 1] + 1e-15)
                cross = float(gs[i] + t * (gs[i + 1] - gs[i]))
                break
        return {
            "gamma_cross": cross,
            "grid": gs,
            "max_re": np.array(vals),
        }


def _demo():
    print("=" * 64)
    print("AUDITORÍA JACOBIANO v1.1 — analítico + espectro + γ_c")
    print("=" * 64)

    N = 24
    ana = TRCGAnalyticalJacobian(N=N)

    # --- A) Umbral exacto en x=0 ---
    print("\n[A] Equilibrio x=0 (derivación exacta)")
    th = ana.gamma_c_at_zero_equilibrium()
    for k, v in th.items():
        print(f" {k}: {v}")
    x0 = np.zeros(N)
    for g in [0.5, 1.0, 1.5]:
        rep = ana.spectral_report(x0, g)
        agr = ana.jacobian_agreement(x0, g)
        print(
            f" γ={g:.1f} | max Reλ={rep['max_real']:+.6e} | "
            f"stable={rep['is_stable']} | J-err={agr['rel_error']:.2e}"
        )

    # --- B) Punto uniforme (no necesariamente equilibrio) ---
    print("\n[B] Punto uniforme x=1/N (auditoría local, no equilibrio general)")
    xu = np.ones(N) / N
    print(f" ||F(x_u; γ=0.5)|| = {norm(ana.vector_field(xu, 0.5)):.4e}")
    for g in [0.5, 0.9, 1.0, 1.1, 1.5]:
        rep = ana.spectral_report(xu, g)
        print(
            f" γ={g:.1f} | max Reλ={rep['max_real']:+.4e} | "
            f"unstable_modes={rep['n_unstable']} | complex={rep['has_complex']}"
        )

    # --- C) Barrido y cruce en x=0 ---
    print("\n[C] Cruce espectral en x=0")
    cross = ana.find_zero_crossing(x0, 0.0, 2.0, n=81)
    print(f" γ_cross ≈ {cross['gamma_cross']}")
    print(f" |γ_cross - 1| = {abs(cross['gamma_cross']-1.0) if cross['gamma_cross'] is not None else None:.3e}")

    # --- D) Acuerdo analítico vs numérico en punto aleatorio ---
    print("\n[D] Acuerdo J_analítico vs J_numérico (punto aleatorio)")
    rng = np.random.default_rng(42)
    x_rand = rng.normal(0.0, 0.05, size=N)
    for g in [0.7, 1.0, 1.3]:
        agr = ana.jacobian_agreement(x_rand, g)
        print(f" γ={g:.1f} | rel_error={agr['rel_error']:.3e} | ok={agr['ok']}")

    print("\nLímites declarados:")
    print(" - γ_c=1 es exacto para F en x=0; no dogma universal TRCG.")
    print(" - Campo prototipo en R^N; falta proyección simplex/Fisher si se exige.")
    print(" - Etiquetas piramidal/parabólico = interpretación, no teorema.")
    print("=" * 64)


if __name__ == "__main__":
    _demo()
```
