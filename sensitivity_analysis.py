"""
Código Viajer — Análisis de Sensibilidad de Hiperparámetros (v1.0.0)
====================================================================
Responde a la pregunta: ¿el lead time del Código Viajer es robusto, o
depende de la calibración canónica (w_p=0.40, w_v=0.35, w_a=0.25)?

Barre sistemáticamente:
  A) Los pesos de la distancia helicoidal (w_p, w_v, w_a) — manteniendo
     la suma igual a 1.0, sobre una malla de 0.05.
  B) Los umbrales THROTTLE y REJECT de forma independiente.
  C) El tamaño del histórico (history_size).

Para cada configuración reporta:
  - Lead time medio (pasos de anticipación frente al validador estático).
  - Desviación estándar del lead time.
  - Tasa de falsos positivos (THROTTLE antes de t=10).

Solo usa la biblioteca estándar. Ejecutar con: python sensitivity_analysis.py
"""

import math
import random
from datetime import datetime, timedelta
from itertools import product

from validator import CodigoViajerValidator, StaticValidator, AgentState, Decision


# ---------------------------------------------------------------------------
# Trayectoria canónica (idéntica a benchmark_stochastic.py)
# ---------------------------------------------------------------------------

def generate_trajectory(t: int, base_time: datetime, noise_scale: float = 0.0) -> AgentState:
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


# ---------------------------------------------------------------------------
# Evaluación de UNA configuración
# ---------------------------------------------------------------------------

def evaluate_config(
    w_p: float,
    w_v: float,
    w_a: float,
    throttle_distance: float = 0.35,
    reject_distance: float = 0.75,
    iterations: int = 400,
    noise_scale: float = 0.01,
):
    """Devuelve (lead_medio, lead_std, fp_rate) para esta configuración."""
    random.seed(42)
    lead_times = []
    false_positives = 0

    for _ in range(iterations):
        dynamic = CodigoViajerValidator(
            max_velocity=0.50,
            max_acceleration=0.50,
            throttle_distance=throttle_distance,
            reject_distance=reject_distance,
            w_p=w_p,
            w_v=w_v,
            w_a=w_a,
        )
        static = StaticValidator()
        t_throttle = None
        t_reject_static = None
        base_time = datetime.now()

        for t in range(36):
            state = generate_trajectory(t, base_time, noise_scale=noise_scale)
            dec_dyn = dynamic.validate(state).value
            dec_sta = static.validate(state).value

            if dec_dyn == "THROTTLE" and t_throttle is None:
                t_throttle = t
            if dec_sta == "REJECT" and t_reject_static is None:
                t_reject_static = t

        if t_throttle is not None and t_throttle < 10:
            false_positives += 1

        if t_throttle is not None and t_reject_static is not None:
            lead_times.append(t_reject_static - t_throttle)

    if not lead_times:
        return None, None, (false_positives / iterations) * 100.0

    mean_lead = sum(lead_times) / len(lead_times)
    var_lead = sum((x - mean_lead) ** 2 for x in lead_times) / len(lead_times)
    std_lead = math.sqrt(var_lead)
    fp_rate = (false_positives / iterations) * 100.0

    return mean_lead, std_lead, fp_rate


# ---------------------------------------------------------------------------
# A) Sensibilidad a los pesos
# ---------------------------------------------------------------------------

def sweep_weights():
    print()
    print("=" * 96)
    print(" A — SENSIBILIDAD A LOS PESOS (w_p + w_v + w_a = 1.0)".center(96))
    print("=" * 96)
    print()
    print(
        f" {'w_p':>6} {'w_v':>6} {'w_a':>6} │ "
        f"{'Lead medio':>12} {'Lead std':>10} {'FP rate':>10} │ Estado"
    )
    print(" " + "─" * 88)

    grid = [round(i * 0.05, 2) for i in range(21)]
    rows = []

    for w_p, w_v in product(grid, grid):
        w_a = round(1.0 - w_p - w_v, 2)
        if w_a < 0.0 or w_a > 1.0:
            continue

        mean_lead, std_lead, fp_rate = evaluate_config(w_p, w_v, w_a, iterations=400)
        is_canonical = (
            abs(w_p - 0.40) < 1e-9 and abs(w_v - 0.35) < 1e-9
        )

        if mean_lead is None:
            continue

        marker = " ← canónica" if is_canonical else ""
        rows.append((w_p, w_v, w_a, mean_lead, std_lead, fp_rate, marker))

    # Resumen estadístico
    leads = [r[3] for r in rows]

    # Imprimir solo un subconjunto representativo para no inundar la consola:
    # la canónica + los extremos + algunos puntos de la malla
    step = max(1, len(rows) // 18)
    sampled = rows[::step]
    canonical_row = next((r for r in rows if r[6]), None)
    if canonical_row and canonical_row not in sampled:
        sampled.append(canonical_row)
    sampled.sort(key=lambda r: (-r[0], r[1]))

    for w_p, w_v, w_a, mean_lead, std_lead, fp_rate, marker in sampled:
        print(
            f" {w_p:>6.2f} {w_v:>6.2f} {w_a:>6.2f} │ "
            f"{mean_lead:>12.2f} {std_lead:>10.2f} {fp_rate:>9.2f}% │{marker}"
        )

    if leads:
        print()
        print(f" Configuraciones evaluadas: {len(rows)}")
        print(f" Lead time medio global: {sum(leads)/len(leads):.2f} pasos")
        print(f" Rango del lead time: [{min(leads):.1f}, {max(leads):.1f}] pasos")

        if max(leads) - min(leads) <= 2.0:
            print(" → ROBUSTO: el lead time varía ≤ 2 pasos ante cambios de pesos.")
        elif max(leads) - min(leads) <= 5.0:
            print(" → MODERADAMENTE ROBUSTO: variación ≤ 5 pasos.")
        else:
            print(" → SENSIBLE: la elección de pesos altera el resultado sustancialmente.")
    print()

    return rows


# ---------------------------------------------------------------------------
# B) Sensibilidad a los umbrales
# ---------------------------------------------------------------------------

def sweep_thresholds():
    print()
    print("=" * 96)
    print(" B — SENSIBILIDAD A LOS UMBRALES (pesos canónicos)".center(96))
    print("=" * 96)
    print()
    print(
        f" {'THROTTLE':>9} {'REJECT':>8} │ "
        f"{'Lead medio':>12} {'Lead std':>10} {'FP rate':>10}"
    )
    print(" " + "─" * 72)

    rows = []
    for throttle in [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]:
        for reject in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85]:
            if reject <= throttle:
                continue
            mean_lead, std_lead, fp_rate = evaluate_config(
                0.40, 0.35, 0.25,
                throttle_distance=throttle,
                reject_distance=reject,
                iterations=400,
            )
            if mean_lead is None:
                continue
            rows.append((throttle, reject, mean_lead, std_lead, fp_rate))
            print(
                f" {throttle:>9.2f} {reject:>8.2f} │ "
                f"{mean_lead:>12.2f} {std_lead:>10.2f} {fp_rate:>9.2f}%"
            )

    if rows:
        leads = [r[2] for r in rows]
        fps = [r[4] for r in rows]
        print()
        print(f" Configuraciones evaluadas: {len(rows)}")
        print(f" Rango de lead time: [{min(leads):.1f}, {max(leads):.1f}] pasos")
        print(f" Rango de FP rate: [{min(fps):.2f}%, {max(fps):.2f}%]")
        print(
            " → Un umbral THROTTLE más bajo anticipa más, pero sube los falsos "
            "positivos."
        )
        print(
            " Un umbral más alto reduce el ruido, pero sacrifica anticipación."
        )
    print()

    return rows


# ---------------------------------------------------------------------------
# C) Sensibilidad al tamaño del histórico
# ---------------------------------------------------------------------------

def sweep_history_size():
    print()
    print("=" * 96)
    print(" C — SENSIBILIDAD AL TAMAÑO DEL HISTÓRICO".center(96))
    print("=" * 96)
    print()
    print(
        f" {'history_size':>14} │ "
        f"{'Lead medio':>12} {'Lead std':>10} {'FP rate':>10}"
    )
    print(" " + "─" * 62)

    random.seed(42)
    for history_size in [3, 5, 10, 15, 20, 30, 50]:
        lead_times = []
        false_positives = 0
        random.seed(42)

        for _ in range(400):
            dynamic = CodigoViajerValidator(
                max_velocity=0.50,
                max_acceleration=0.50,
                history_size=history_size,
            )
            static = StaticValidator()
            t_throttle = None
            t_reject_static = None
            base_time = datetime.now()

            for t in range(36):
                state = generate_trajectory(t, base_time, noise_scale=0.01)
                if dynamic.validate(state).value == "THROTTLE" and t_throttle is None:
                    t_throttle = t
                if static.validate(state).value == "REJECT" and t_reject_static is None:
                    t_reject_static = t

            if t_throttle is not None and t_throttle < 10:
                false_positives += 1
            if t_throttle is not None and t_reject_static is not None:
                lead_times.append(t_reject_static - t_throttle)

        if lead_times:
            mean_lead = sum(lead_times) / len(lead_times)
            var_lead = sum((x - mean_lead) ** 2 for x in lead_times) / len(lead_times)
            std_lead = math.sqrt(var_lead)
            fp_rate = (false_positives / 400) * 100.0
            print(
                f" {history_size:>14} │ "
                f"{mean_lead:>12.2f} {std_lead:>10.2f} {fp_rate:>9.2f}%"
            )

    print()
    print(
        " Nota: el cálculo de la aceleración necesita al menos 3 estados en el\n"
        " histórico. Un history_size menor que eso desactiva la componente d_a."
    )
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print()
    print("╔" + "═" * 94 + "╗")
    print("║" + " CÓDIGO VIAJER — ANÁLISIS DE SENSIBILIDAD DE HIPERPARÁMETROS ".center(94) + "║")
    print("╚" + "═" * 94 + "╝")
    print()
    print(" Este análisis responde a la pregunta: ¿el lead time observado en el")
    print(" benchmark es una propiedad del MÉTODO, o de la CALIBRACIÓN concreta?")
    print(" Cuatrocientas iteraciones de Monte Carlo por configuración.")

    sweep_weights()
    sweep_thresholds()
    sweep_history_size()

    print("=" * 96)
    print(" FIN DEL ANÁLISIS".center(96))
    print("=" * 96)
    print()
