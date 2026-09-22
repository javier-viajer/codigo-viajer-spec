"""
Código Viajer — Informe de Simulación y Benchmark en Consola (v1.2.0)
=====================================================================
Genera un informe completo en texto plano con tres secciones:
  1. Tabla de trayectoria en R^4 (determinista, 36 pasos).
  2. Evolución de Dh con indicadores visuales de umbrales.
  3. Distribución del Lead Time (Monte Carlo real, 1000 iteraciones).

Sin dependencia de matplotlib. Ejecutar con: python generate_report.py
"""

import math
import random
from datetime import datetime, timedelta
from collections import Counter

from validator import CodigoViajerValidator, StaticValidator, AgentState, Decision


# ---------------------------------------------------------------------------
# Funciones de trayectoria (reproducen las de benchmark_stochastic.py)
# ---------------------------------------------------------------------------

def generate_trajectory(
    t: int, base_time: datetime, noise_scale: float = 0.0
) -> AgentState:
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


def run_single_simulation(noise_scale: float = 0.01) -> dict:
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
    random.seed(42)
    lead_times = []
    false_positives = 0

    for _ in range(iterations):
        res = run_single_simulation(noise_scale=0.01)

        if res["t_throttle"] is not None and res["t_throttle"] < 10:
            false_positives += 1

        if res["t_throttle"] is not None and res["t_reject_static"] is not None:
            lead_times.append(res["t_reject_static"] - res["t_throttle"])

    mean_lead = sum(lead_times) / len(lead_times) if lead_times else 0.0
    var_lead = (
        sum((x - mean_lead) ** 2 for x in lead_times) / len(lead_times)
        if lead_times
        else 0.0
    )
    std_lead = math.sqrt(var_lead)
    fp_rate = (false_positives / iterations) * 100.0

    return mean_lead, std_lead, fp_rate, lead_times


# ---------------------------------------------------------------------------
# SECCIÓN 1: Tabla de trayectoria determinista
# ---------------------------------------------------------------------------

def bar(value: float, width: int = 20, filled: str = "█", empty: str = "░") -> str:
    """Barra ASCII proporcional para un valor en [0, 1]."""
    n = int(round(value * width))
    return filled * n + empty * (width - n)


def print_trajectory_table():
    random.seed(42)
    validator = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    steps = 36
    base_time = datetime.now()

    print()
    print("=" * 100)
    print(" SECCIÓN 1 — TRAYECTORIA DETERMINISTA EN ℝ⁴".center(100))
    print("=" * 100)
    print()
    print(
        f"{'t':>3} │ {'L':>6} {'S':>6} {'I':>6} {'B':>6} │ "
        f"{' D_h':>21} │ {'Decisión':<10} │ {'Evolución L S I B'}"
    )
    print("—" * 100)

    for t in range(steps):
        state = generate_trajectory(t, base_time, noise_scale=0.0)
        decision = validator.validate(state)
        dec = decision.value
        dh_val = validator.last_d_h

        # Barra combinada de las 4 dimensiones (cada una ocupa 5 chars)
        bars = (
            f"{bar(state.life_preservation, 5, 'L', '·')}"
            f"{bar(state.entropy, 5, 'S', '·')}"
            f"{bar(state.node_integrity, 5, 'I', '·')}"
            f"{bar(state.resource_balance, 5, 'B', '·')}"
        )

        # Indicador visual de decisión
        if dec == "ALLOW":
            marker = "✓"
        elif dec == "THROTTLE":
            marker = "⚠"
        else:
            marker = "✗"

        print(
            f"{t:>3} │ {state.life_preservation:6.3f} {state.entropy:6.3f} "
            f"{state.node_integrity:6.3f} {state.resource_balance:6.3f} │ "
            f"{bar(dh_val, 20)} {dh_val:.3f} │ "
            f"{marker} {dec:<8} │ {bars}"
        )

    print()


# ---------------------------------------------------------------------------
# SECCIÓN 2: Evolución de Dh con umbrales
# ---------------------------------------------------------------------------

def print_dh_evolution():
    random.seed(42)
    validator = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    steps = 40
    base_time = datetime.now()

    dh_values = []

    for t in range(steps):
        if t >= 10:
            # Deriva acelerada (misma lógica que generate_plots original)
            dt = (t - 10) / 15.0
            L = max(0.0, min(1.0, 1.0 - 0.015 * (dt ** 1.5) + random.gauss(0, 0.01)))
            S = max(0.0, min(1.0, 0.02 + 0.15 * (dt ** 2.0) + abs(random.gauss(0, 0.01))))
            I = max(0.0, min(1.0, 0.99 - 0.12 * (dt ** 1.8) + random.gauss(0, 0.01)))
            B = max(0.0, min(1.0, 1.0 - 0.01 * (dt ** 1.2) + random.gauss(0, 0.01)))
        else:
            L = max(0.0, min(1.0, 1.0 + random.gauss(0, 0.005)))
            S = max(0.0, min(1.0, 0.02 + abs(random.gauss(0, 0.005))))
            I = max(0.0, min(1.0, 0.99 + random.gauss(0, 0.005)))
            B = max(0.0, min(1.0, 1.0 + random.gauss(0, 0.005)))

        state = AgentState(
            timestamp=base_time + timedelta(days=t),
            life_preservation=L,
            entropy=S,
            node_integrity=I,
            resource_balance=B,
        )
        validator.validate(state)
        dh_values.append(validator.last_d_h)

    print()
    print("=" * 100)
    print(" SECCIÓN 2 — EVOLUCIÓN DE D_h CON DERIVA ACELERADA (40 pasos)".center(100))
    print("=" * 100)
    print()
    print(f" {'t':>3} │ {'D_h':>6} │ {'Gráfico de D_h':>60} ← THROTTLE (0.35) ··· REJECT (0.75)")
    print(" " + "—" * 95)

    for t, dh in enumerate(dh_values):
        # Escala: 60 chars para [0, 1]
        pos = int(round(dh * 60))
        throttle_pos = int(round(0.35 * 60)) # 21
        reject_pos = int(round(0.75 * 60)) # 45

        # Construir la línea con marcas de umbral
        line = [" "] * 61
        for i in range(pos):
            line[i] = "▓"

        # Marcar el extremo
        if pos < 61:
            line[min(pos, 60)] = "●"

        # Poner umbrales como marcas verticales
        line[throttle_pos] = "╎" if pos != throttle_pos else "●"
        line[reject_pos] = "╎" if pos != reject_pos else "●"

        plot = "".join(line)

        if dh < 0.35:
            zone = "ALLOW "
        elif dh < 0.75:
            zone = "THROTTLE "
        else:
            zone = "REJECT "

        print(f" {t:>3} │ {dh:.3f} │ {plot} │ {zone}")

    print()
    print(" Leyenda: ▓ = D_h acumulada ╎ = umbral ● = valor actual de D_h")
    print()


# ---------------------------------------------------------------------------
# SECCIÓN 3: Distribución del Lead Time (Monte Carlo)
# ---------------------------------------------------------------------------

def print_lead_time_distribution():
    print()
    print("=" * 100)
    print(" SECCIÓN 3 — DISTRIBUCIÓN DEL LEAD TIME (Monte Carlo, 1000 iteraciones)".center(100))
    print("=" * 100)
    print()

    mean_lead, std_lead, fp_rate, lead_times = run_monte_carlo(1000)

    if not lead_times:
        print(" No se detectó lead time en ninguna simulación.")
        return

    # Histograma de frecuencias
    counter = Counter(lead_times)
    min_lt = min(lead_times)
    max_lt = max(lead_times)
    max_count = max(counter.values())

    # Escala: barra de hasta 50 chars para la frecuencia máxima
    def hist_bar(count: int) -> str:
        n = int(round(count / max_count * 50)) if max_count > 0 else 0
        return "█" * n

    print(f" {'Lead Time (pasos)':>20} │ {'Frecuencia':>10} │ Distribución")
    print(" " + "—" * 80)

    for lt in range(min_lt, max_lt + 1):
        count = counter.get(lt, 0)
        print(f" {lt:>20} │ {count:>10} │ {hist_bar(count)} {count}")

    print()
    print(f" Lead Time Medio: {mean_lead:.1f} ± {std_lead:.1f} pasos")
    print(f" Rango: [{min_lt}, {max_lt}] pasos")
    print(f" Tasa de Falsos Positivos (t < 10): {fp_rate:.2f}%")

    # Comparativa con los umbrales
    print()
    print(" ┌─────────────────────────────────────────────────────────────┐")
    print(f" │ Código Viajer THROTTLE ─── lead time ───► Static REJECT │")
    print(f" │ (t ≈ {mean_lead - std_lead:.0f}–{mean_lead + std_lead:.0f} pasos antes) │")
    print(" └─────────────────────────────────────────────────────────────┘")

    print()


# ---------------------------------------------------------------------------
# Resumen final
# ---------------------------------------------------------------------------

def print_summary():
    print()
    print("=" * 100)
    print(" RESUMEN DEL INFORME".center(100))
    print("=" * 100)
    print()

    mean_lead, std_lead, fp_rate, _ = run_monte_carlo(1000)

    print(f" Versión del validador: CodigoViajerValidator v1.1.3")
    print(f" Validador estático: StaticValidator (4 umbrales)")
    print(f" Iteraciones Monte Carlo: 1,000")
    print(f" Lead Time medio: {mean_lead:.1f} ± {std_lead:.1f} pasos")
    print(f" Falsos positivos (t < 10): {fp_rate:.2f}%")
    print()
    print(" El Código Viajer detecta la deriva de forma preventiva")
    print(" mediante la distancia helicoidal D_h, que incorpora posición,")
    print(" velocidad y aceleración en ℝ⁴. El validador estático solo")
    print(" reacciona cuando los umbrales individuales se cruzan.")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print()
    print("╔" + "═" * 98 + "╗")
    print("║" + " CÓDIGO VIAJER — INFORME DE ESTABILIDAD Y GOBERNANZA PREVENTIVA (v1.2.0) ".center(98) + "║")
    print("╚" + "═" * 98 + "╝")

    print_trajectory_table()
    print_dh_evolution()
    print_lead_time_distribution()
    print_summary()
