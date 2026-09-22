"""
Código Viajer — Benchmark Estocástico de Monte Carlo (v1.1.4)
=============================================================
Evaluación cuantitativa alineada con CASE_STUDY.md y compatible 
con la interfaz canónica de validator.py.
"""

import math
import random
from datetime import datetime, timedelta
from typing import Dict, List
from validator import CodigoViajerValidator, AgentState

def generate_trajectory(t: int, base_time: datetime, noise_scale: float = 0.01) -> AgentState:
    """
    Genera la trayectoria helicoidal con deriva exponencial tras t >= 10,
    añadiendo ruido blanco gaussiano para simular la estocasticidad real.
    """
    if t < 10:
        L = 1.00
        S = 0.02
        I = 0.99
        B = 1.00
    else:
        dt = (t - 10) / 12.0
        L = max(0.0, min(1.0, 1.00 - 0.08 * (dt ** 2.2)))
        S = max(0.0, min(1.0, 0.02 + 0.85 * (dt ** 2.5)))
        I = max(0.0, min(1.0, 0.99 - 0.70 * (dt ** 2.0)))
        B = max(0.0, min(1.0, 1.00 - 0.15 * (dt ** 1.5)))

    if noise_scale > 0:
        L = max(0.0, min(1.0, L + random.gauss(0, noise_scale)))
        S = max(0.0, min(1.0, S + random.gauss(0, noise_scale)))
        I = max(0.0, min(1.0, I + random.gauss(0, noise_scale)))
        B = max(0.0, min(1.0, B + random.gauss(0, noise_scale)))

    current_timestamp = base_time + timedelta(seconds=t)

    return AgentState(
        timestamp=current_timestamp,
        life_preservation=L,
        entropy=S,
        node_integrity=I,
        resource_balance=B
    )


def run_single_simulation(noise_scale: float = 0.01) -> Dict:
    validator = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    t_throttle = None
    t_reject_dynamic = None
    t_reject_static = None
    base_time = datetime.now()

    for t in range(36):
        state = generate_trajectory(t, base_time, noise_scale=noise_scale)
        res = validator.validate(state)
        
        # Extracción segura de la decisión desde el objeto Decision o Diccionario
        dec = getattr(res, "decision", res.get("decision") if isinstance(res, dict) else str(res))

        if dec == "THROTTLE" and t_throttle is None:
            t_throttle = t
        if dec == "REJECT" and t_reject_dynamic is None:
            t_reject_dynamic = t

        if (state.node_integrity < 0.50 or state.life_preservation < 0.50) and t_reject_static is None:
            t_reject_static = t

    return {
        "t_throttle": t_throttle,
        "t_reject_dynamic": t_reject_dynamic,
        "t_reject_static": t_reject_static,
    }


def run_monte_carlo(iterations: int = 1000):
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
    var_lead = sum((x - mean_lead) ** 2 for x in lead_times) / len(lead_times) if lead_times else 0.0
    std_lead = math.sqrt(var_lead)
    fp_rate = (false_positives / iterations) * 100.0

    return mean_lead, std_lead, fp_rate


def print_single_run_table():
    random.seed(42)
    validator = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    steps = 36
    base_time = datetime.now()

    print("=" * 70)
    print(" CÓDIGO VIAJER — VERIFICACIÓN DE TRAYECTORIA DETERMINISTA (v1.1.4)")
    print("=" * 70)
    print(f"{'Paso (t)':<10}{'L':<8}{'S':<8}{'I':<8}{'B':<8}{'Dh':<10}{'Decisión':<12}")
    print("-" * 70)

    for t in range(steps):
        state = generate_trajectory(t, base_time, noise_scale=0.0)
        res = validator.validate(state)
        
        dec = getattr(res, "decision", res.get("decision") if isinstance(res, dict) else str(res))
        dh_val = getattr(res, "helical_distance", getattr(res, "Dh", res.get("Dh", 0.0) if isinstance(res, dict) else 0.0))

        print(f"{t:<10}{state.life_preservation:<8.2f}{state.entropy:<8.2f}{state.node_integrity:<8.2f}{state.resource_balance:<8.2f}{dh_val:<10.3f}{dec:<12}")


if __name__ == "__main__":
    print_single_run_table()
    print("\nEjecutando Simulación de Monte Carlo (1,000 iteraciones)...")
    mean_lead, std_lead, fp_rate = run_monte_carlo(1000)
    print("-" * 70)
    print(f"Lead Time Medio (Anticipación): {mean_lead:.1f} ± {std_lead:.1f} pasos")
    print(f"Tasa de Falsos Positivos (t < 10): {fp_rate:.2f}%")
    print("=" * 70)

       
            
       



       




   

          

        
       
