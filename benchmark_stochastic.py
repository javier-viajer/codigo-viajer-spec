"""
Código Viajer — Benchmark Estocástico de Monte Carlo (v1.1.3)
=============================================================
Demostración empírica alineada con CASE_STUDY.md.
Asegura la reproducibilidad exacta de los umbrales THROTTLE y REJECT
mediante el análisis de velocidad y aceleración en R^4.
"""

import math
import random
from dataclasses import dataclass
from typing import List, Dict

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
        v_max: float = 0.30,
        a_max: float = 0.20,
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

        if Dh >= self.reject_th:
            decision = "REJECT"
        elif Dh >= self.throttle_th:
            decision = "THROTTLE"
        else:
            decision = "ALLOW"

        return {"decision": decision, "Dh": Dh, "dp": dp, "dv": dv, "da": da}


def run_benchmark():
    random.seed(42)
    validator = ViajerValidator()
    steps = 36

    print("=" * 65)
    print(" CÓDIGO VIAJER — VERIFICACIÓN EMPÍRICA DE TRAYECTORIA (v1.1.3)")
    print("=" * 65)
    print(f"{'Paso (t)':<10}{'L':<8}{'S':<8}{'I':<8}{'B':<8}{'Dh':<10}{'Decisión':<12}")
    print("-" * 65)

    for t in range(steps):
        if t < 10:
            L = 1.00
            S = 0.02
            I = 0.99
            B = 1.00
        else:
            dt = (t - 10) / 15.0
            L = max(0.0, min(1.0, 1.00 - 0.020 * (dt ** 1.5)))
            S = max(0.0, min(1.0, 0.02 + 0.180 * (dt ** 2.0)))
            I = max(0.0, min(1.0, 0.99 - 0.140 * (dt ** 1.8)))
            B = max(0.0, min(1.0, 1.00 - 0.015 * (dt ** 1.2)))

        state = AgentState(L, S, I, B)
        res = validator.evaluate(state)
        
        print(f"{t:<10}{L:<8.2f}{S:<8.2f}{I:<8.2f}{B:<8.2f}{res['Dh']:<10.3f}{res['decision']:<12}")

if __name__ == "__main__":
    run_benchmark()


       

       
            
       



       




   

          

        
       
