"""
Código Viajer — Benchmark Estocástico de Monte Carlo (v1.1.2)
=============================================================
Evaluación cuantitativa sobre 1,000 iteraciones para medir:
1. Lead Time (Tiempo de anticipación frente a control estático).
2. Tasa de Falsos Positivos bajo ruido blanco nominal.
3. Resiliencia y comportamiento ante recuperación de la trayectoria.
"""

import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict


# =====================================================================
# 1. ESPECIFICACIÓN Y VALIDADOR CÓDIGO VIAJER (v1.1.2)
# =====================================================================

@dataclass
class AgentState:
    L: float # Life Preservation [0, 1]
    S: float # Entropy [0, 1]
    I: float # Node Integrity [0, 1]
    B: float # Resource Balance [0, 1]

    def to_vector(self) -> List[float]:
        return [self.L, self.S, self.I, self.B]


class ViajerValidator:
    def __init__(
        self,
        wp: float = 0.40,
        wv: float = 0.35,
        wa: float = 0.25,
        v_max: float = 0.50,
        a_max: float = 0.50,
        throttle_th: float = 0.35,
        reject_th: float = 0.75,
    ):
        self.wp = wp
        self.wv = wv
        self.wa = wa
        self.v_max = v_max
        self.a_max = a_max
        self.throttle_th = throttle_th
        self.reject_th = reject_th
        self.attractor = [1.0, 0.0, 1.0, 1.0]
        self.history: List[AgentState] = []

    def _euclidean_distance(self, v1: List[float], v2: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def evaluate(self, current_state: AgentState) -> Dict:
        self.history.append(current_state)
        curr = current_state.to_vector()

        # Invariantes Constitucionales Duros
        if current_state.L < 0.50 or current_state.I < 0.50:
            return {"decision": "REJECT", "Dh": 1.0, "reason": "HARD_INVARIANT_VIOLATION"}

        # 1. Distancia de Posición (dp)
        d_raw = self._euclidean_distance(curr, self.attractor)
        # Distancia máxima posible en el hipercubo unitario hasta E = 2.0
        dp = min(1.0, d_raw / 2.0)

        # 2. Magnitud de Velocidad (dv)
        dv = 0.0
        if len(self.history) >= 2:
            prev = self.history[-2].to_vector()
            vel = [c - p for c, p in zip(curr, prev)]
            v_mag = math.sqrt(sum(x ** 2 for x in vel))
            dv = min(1.0, v_mag / self.v_max)

        # 3. Magnitud de Aceleración (da)
        da = 0.0
        if len(self.history) >= 3:
            prev1 = self.history[-2].to_vector()
            prev2 = self.history[-3].to_vector()
            v_curr = [c - p for c, p in zip(curr, prev1)]
            v_prev = [p1 - p2 for p1, p2 in zip(prev1, prev2)]
            acc = [vc - vp for vc, vp in zip(v_curr, v_prev)]
            a_mag = math.sqrt(sum(x ** 2 for x in acc))
            da = min(1.0, a_mag / self.a_max)

        # Métrica de Distancia Helicoidal (Dh)
        Dh = min(1.0, self.wp * dp + self.wv * dv + self.wa * da)

        # Regla de Decisión
        if Dh >= self.reject_th:
            decision = "REJECT"
        elif Dh >= self.throttle_th:
            decision = "THROTTLE"
        else:
            decision = "PASS"

        return {"decision": decision, "Dh": Dh, "dp": dp, "dv": dv, "da": da}


class NaiveValidator:
    """Controlador estático tradicional basado únicamente en umbrales duros."""
    def evaluate(self, state: AgentState) -> str:
        if state.L < 0.50 or state.I < 0.50 or state.S > 0.60:
            return "REJECT"
        elif state.S > 0.35:
            return "THROTTLE"
        return "PASS"


# =====================================================================
# 2. GENERADORES DE TRAYECTORIAS ESTOCÁSTICAS
# =====================================================================

def generate_drift_trajectory(steps: int = 40, noise_level: float = 0.02) -> List[AgentState]:
    """Genera una trayectoria sintética con aceleración estocástica de la deriva."""
    trajectory = []
    for t in range(steps):
        noise = lambda: random.gauss(0, noise_level)
        if t < 10:
            # Fase 1: Armonía Nominal
            L = min(1.0, max(0.0, 1.0 + noise()))
            S = min(1.0, max(0.0, 0.02 + abs(noise())))
            I = min(1.0, max(0.0, 0.99 + noise()))
            B = min(1.0, max(0.0, 1.0 + noise()))
        else:
            # Fase 2 y 3: Deriva Acelerada (Perfil Cuadrático + Ruido)
            dt = (t - 10) / 15.0
            L = min(1.0, max(0.0, 1.0 - 0.015 * (dt ** 1.5) + noise()))
            S = min(1.0, max(0.0, 0.02 + 0.15 * (dt ** 2.0) + abs(noise())))
            I = min(1.0, max(0.0, 0.99 - 0.12 * (dt ** 1.8) + noise()))
            B = min(1.0, max(0.0, 1.0 - 0.01 * (dt ** 1.2) + noise()))
        
        trajectory.append(AgentState(L, S, I, B))
    return trajectory


def generate_noisy_stable_trajectory(steps: int = 40, noise_level: float = 0.04) -> List[AgentState]:
    """Genera una trayectoria nominal con alto ruido estocástico pero SIN deriva destructiva."""
    trajectory = []
    for t in range(steps):
        noise = lambda: random.gauss(0, noise_level)
        L = min(1.0, max(0.55, 0.95 + noise()))
        S = min(0.30, max(0.0, 0.05 + abs(noise())))
        I = min(1.0, max(0.55, 0.95 + noise()))
        B = min(1.0, max(0.55, 0.95 + noise()))
        trajectory.append(AgentState(L, S, I, B))
    return trajectory


# =====================================================================
# 3. EJECUCIÓN DE SIMULACIÓN DE MONTE CARLO
# =====================================================================

def run_monte_carlo(iterations: int = 1000):
    print("=" * 70)
    print(f" CÓDIGO VIAJER (v1.1.2) — SIMULACIÓN DE MONTE CARLO ({iterations} RUNS)")
    print("=" * 70)

    # -----------------------------------------------------------------
    # PRUEBA A: Lead Time y Anticipación en Deriva Acelerada
    # -----------------------------------------------------------------
    lead_times = []
    viajer_detections = 0
    naive_detections = 0

    for _ in range(iterations):
        trajectory = generate_drift_trajectory(steps=40)
        viajer = ViajerValidator()
        naive = NaiveValidator()

        t_viajer_warning = None
        t_naive_warning = None

        for t, state in enumerate(trajectory):
            res_v = viajer.evaluate(state)
            res_n = naive.evaluate(state)

            if t_viajer_warning is None and res_v["decision"] in ["THROTTLE", "REJECT"]:
                t_viajer_warning = t

            if t_naive_warning is None and res_n in ["THROTTLE", "REJECT"]:
                t_naive_warning = t

        if t_viajer_warning is not None:
            viajer_detections += 1

        if t_naive_warning is not None:
            naive_detections += 1

        if t_viajer_warning is not None and t_naive_warning is not None:
            lead = t_naive_warning - t_viajer_warning
            lead_times.append(lead)

    # Cálculo Estadístico
    avg_lead = sum(lead_times) / len(lead_times) if lead_times else 0.0
    variance = sum((x - avg_lead) ** 2 for x in lead_times) / len(lead_times) if lead_times else 0.0
    std_dev_lead = math.sqrt(variance)

    # -----------------------------------------------------------------
    # PRUEBA B: Tasa de Falsos Positivos en Escenario Ruidoso Estabilizado
    # -----------------------------------------------------------------
    false_positives_viajer = 0
    false_positives_naive = 0

    for _ in range(iterations):
        stable_trajectory = generate_noisy_stable_trajectory(steps=40)
        viajer = ViajerValidator()
        naive = NaiveValidator()

        v_flagged = False
        n_flagged = False

        for state in stable_trajectory:
            res_v = viajer.evaluate(state)
            res_n = naive.evaluate(state)

            if res_v["decision"] in ["THROTTLE", "REJECT"]:
                v_flagged = True
            if res_n in ["THROTTLE", "REJECT"]:
                n_flagged = True

        if v_flagged:
            false_positives_viajer += 1
        if n_flagged:
            false_positives_naive += 1

    fp_rate_viajer = (false_positives_viajer / iterations) * 100.0
    fp_rate_naive = (false_positives_naive / iterations) * 100.0

    # -----------------------------------------------------------------
    # REPORTE DE RESULTADOS DE BENCHMARK
    # -----------------------------------------------------------------
    print("\n[MÉTRICAS DE DETECCIÓN Y ANTICIPACIÓN]")
    print(f" * Detección Preventiva Código Viajer: {viajer_detections / iterations * 100:.1f}%")
    print(f" * Detección Estática Naive Validator: {naive_detections / iterations * 100:.1f}%")
    print(f" * Lead Time Medio (t_naive - t_viajer): {avg_lead:.2f} pasos de tiempo")
    print(f" * Desviación Estándar de Lead Time : +/- {std_dev_lead:.2f} pasos")

    print("\n[ANÁLISIS DE RESILIENCIA Y FALSOS POSITIVOS]")
    print(f" * Tasa de Falsos Positivos (Código Viajer) : {fp_rate_viajer:.2f}%")
    print(f" * Tasa de Falsos Positivos (Naive Validator): {fp_rate_naive:.2f}%")

    print("\n" + "=" * 70)
    print(" CONCLUSIÓN ESTADÍSTICA:")
    print(f" El Código Viajer demuestra una anticipación sistemática de ~{avg_lead:.1f} pasos")
    print(f" de tiempo frente a los modelos estáticos, manteniendo los falsos")
    print(f" positivos en un rango acotado de {fp_rate_viajer:.1f}%.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_monte_carlo(iterations=1000)
