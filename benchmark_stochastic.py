"""
Código Viajer — Benchmark Estocástico de Monte Carlo (v1.1.6)
=============================================================
Evaluación cuantitativa alineada con CASE_STUDY.md y
compatible con la interfaz y unidades canónicas de validator.py.

Correcciones respecto a v1.1.5:
- Eliminado código inalcanzable en generate_trajectory.
- Corregida la indentación.
- El validador estático ahora usa StaticValidator (umbrales en las 4 dimensiones),
  no solo los mismos invariantes duros del validador dinámico.
"""

import math
import random
from datetime import datetime, timedelta
from typing import Dict
from validator import CodigoViajerValidator, StaticValidator, AgentState, Decision


def generate_trajectory(
    t: int, base_time: datetime, noise_scale: float = 0.0
) -> AgentState:
    """Genera un estado sintético en el paso t de una trayectoria de 35 pasos.

    La trayectoria tiene tres fases:
      1. Armonía (t ≈ 0–10)
      2. Deriva progresiva (t ≈ 10–30) — subida logística de entropía
      3. Colapso constitucional (t ≈ 30–35) — caída de integridad
    """
    p = t / 35.0

    L = max(0.0, min(1.0, 1.00 - 0.10 * p))
    B = max(0.0, min(1.0, 1.00 - 0.12 * p))
    S = max(0.0, min(1.0, 0.04 + 0.80 / (1.0 + math.exp(-1.70 * (t - 15.0)))))
    I = max(
        0.0,
        min(1.0, 0.96 - 0.10 * p - 0.50 / (1.0 + math.exp(-0.70 * (t - 30.0)))),
    )

    if noise_scale > 0:
        L = max(0.0, min(1.0, L + random.gauss(0, noise_scale)))
        S = max(0.0, min(1.0, S + random.gauss(0, noise_scale)))
        I = max(0.0, min(1.0, I + random.gauss(0, noise_scale)))
        B = max(0.0, min(1.0, B + random.gauss(0, noise_scale)))

    return AgentState(
        timestamp=base_time + timedelta(days=t),
        life_preservation=L,
        entropy=S,
        node_integrity=I,
        resource_balance=B,
    )


def run_single_simulation(noise_scale: float = 0.01) -> Dict:
    """Ejecuta una trayectoria y compara Código Viajer con validador estático."""
    dynamic = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    static = StaticValidator()
    t_throttle = None
    t_reject_dynamic = None
    t_reject_static = None
    base_time = datetime.now()

    for t in range(36):
        state = generate_trajectory(t, base_time, noise_scale=noise_scale)

        dec_dyn = dynamic.validate(state).value
        dec_sta = static.validate(state).value

        if dec_dyn == "THROTTLE" and t_throttle is None:
            t_throttle = t
        if dec_dyn == "REJECT" and t_reject_dynamic is None:
            t_reject_dynamic = t
        if dec_sta == "REJECT" and t_reject_static is None:
            t_reject_static = t

    return {
        "t_throttle": t_throttle,
        "t_reject_dynamic": t_reject_dynamic,
        "t_reject_static": t_reject_static,
    }


def run_monte_carlo(iterations: int = 1000):
    """Ejecuta N simulaciones y devuelve lead time medio, std y tasa de FP."""
    random.seed(42)
    lead_times = []
    false_positives = 0

    for _ in range(iterations):
        res = run_single_simulation(noise_scale=0.01)

        if res["t_throttle"] is not None and res["t_throttle"] < 10:
            false_positives += 1

        if res["t_throttle"] is not None and res["t_reject_static"] is not None:
            lead_time = res["t_reject_static"] - res["t_throttle"]
            lead_times.append(lead_time)

    mean_lead = sum(lead_times) / len(lead_times) if lead_times else 0.0
    var_lead = (
        sum((x - mean_lead) ** 2 for x in lead_times) / len(lead_times)
        if lead_times
        else 0.0
    )
    std_lead = math.sqrt(var_lead)
    fp_rate = (false_positives / iterations) * 100.0

    return mean_lead, std_lead, fp_rate


def print_single_run_table():
    """Imprime la tabla de trayectoria determinista (sin ruido)."""
    random.seed(42)
    validator = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    steps = 36
    base_time = datetime.now()

    print("=" * 75)
    print(" CÓDIGO VIAJER — VERIFICACIÓN DE TRAYECTORIA DETERMINISTA (v1.1.6)")
    print("=" * 75)
    print(f"{'Paso (t)':<10}{'L':<8}{'S':<8}{'I':<8}{'B':<8}{'Dh':<10}{'Decisión':<12}")
    print("-" * 75)

    for t in range(steps):
        state = generate_trajectory(t, base_time, noise_scale=0.0)
        decision = validator.validate(state)
        dec = decision.value
        dh_val = validator.last_d_h

        print(
            f"{t:<10}"
            f"{state.life_preservation:<8.2f}"
            f"{state.entropy:<8.2f}"
            f"{state.node_integrity:<8.2f}"
            f"{state.resource_balance:<8.2f}"
            f"{dh_val:<10.3f}"
            f"{dec:<12}"
        )


if __name__ == "__main__":
    print_single_run_table()
    print("\nEjecutando Simulación de Monte Carlo (1,000 iteraciones)...")
    mean_lead, std_lead, fp_rate = run_monte_carlo(1000)
    print("-" * 75)
    print(f"Lead Time Medio (Anticipación): {mean_lead:.1f} ± {std_lead:.1f} pasos")
    print(f"Tasa de Falsos Positivos (t < 10): {fp_rate:.2f}%")
    print("=" * 75)


    
  
       



    
   



       




   

          

        
       
