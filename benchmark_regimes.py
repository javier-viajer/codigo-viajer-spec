"""
Código Viajer — Benchmark Multi-Régimen de Fallo (v1.0.0)
==========================================================
Ampliación del benchmark de un solo régimen (curva logística) a TRES
regímenes de deterioro distintos, para comprobar si la ventaja del
control dinámico sobre el estático se mantiene cuando la FORMA del
fallo cambia.

Regímenes implementados:
  1. LOGÍSTICO — deriva suave y progresiva (el del benchmark original).
  2. OSCILATORIO — entropía oscilante con amplitud creciente; la
                    trayectoria se degrada en zigzag antes de colapsar.
  3. ABRUPTO — colapso súbito: todo se derrumba en pocos pasos.

Para cada régimen se reportan:
  - t_THROTTLE dinámico medio y su desviación.
  - t_REJECT estático medio.
  - Lead time resultante.
  - Comparación de ambos controladores sobre las MISMAS trayectorias.

Solo usa la biblioteca estándar. Ejecutar con: python benchmark_regimes.py
"""

import math
import random
from datetime import datetime, timedelta

from validator import CodigoViajerValidator, StaticValidator, AgentState, Decision


# ---------------------------------------------------------------------------
# Generadores de trayectoria por régimen
# ---------------------------------------------------------------------------

def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def logistic_regime(t: int, base_time: datetime, noise_scale: float) -> AgentState:
    """Régimen original: deriva logística suave con colapso tardío de integridad."""
    p = t / 35.0
    L = _clamp(1.00 - 0.10 * p)
    B = _clamp(1.00 - 0.12 * p)
    S = _clamp(0.04 + 0.80 / (1.0 + math.exp(-1.70 * (t - 15.0))))
    I = _clamp(0.96 - 0.10 * p - 0.50 / (1.0 + math.exp(-0.70 * (t - 30.0))))
    return _apply_noise(L, S, I, B, base_time, t, noise_scale)


def oscillatory_regime(t: int, base_time: datetime, noise_scale: float) -> AgentState:
    """Deriva oscilatoria: la entropía sube y baja con amplitud creciente.

    La envolvente crece linealmente y la oscilación tiene periodo ~6 pasos.
    La integridad cae de forma escalonada, sincronizada con los picos de entropía.
    """
    p = t / 35.0
    envelope = 0.03 + 0.55 * p # amplitud creciente
    oscillation = math.sin(2.0 * math.pi * t / 6.0) # periodo 6 pasos

    S = _clamp(0.30 + envelope * oscillation) # entropía oscilante
    L = _clamp(1.00 - 0.14 * p)
    B = _clamp(1.00 - 0.16 * p - 0.05 * max(0.0, oscillation))
    # La integridad cae cuando el pico de entropía es alto
    stress = max(0.0, oscillation) * (p ** 1.5)
    I = _clamp(0.97 - 0.55 * stress - 0.06 * p)

    return _apply_noise(L, S, I, B, base_time, t, noise_scale)


def abrupt_regime(t: int, base_time: datetime, noise_scale: float) -> AgentState:
    """Colapso súbito: homeostasis hasta t=28, derrumbe total en 5 pasos."""
    if t < 28:
        L = _clamp(0.99)
        B = _clamp(0.98)
        S = _clamp(0.05 + 0.01 * t / 28.0)
        I = _clamp(0.98)
    else:
        # Caída brusca durante 5 pasos (t=28..33)
        k = (t - 28) / 5.0
        L = _clamp(0.99 - 0.55 * k)
        B = _clamp(0.98 - 0.50 * k)
        S = _clamp(0.06 + 0.88 * k)
        I = _clamp(0.98 - 0.60 * k)

    return _apply_noise(L, S, I, B, base_time, t, noise_scale)


def _apply_noise(L, S, I, B, base_time, t, noise_scale) -> AgentState:
    if noise_scale > 0:
        L = _clamp(L + random.gauss(0, noise_scale))
        S = _clamp(S + random.gauss(0, noise_scale))
        I = _clamp(I + random.gauss(0, noise_scale))
        B = _clamp(B + random.gauss(0, noise_scale))

    return AgentState(
        timestamp=base_time + timedelta(days=t),
        life_preservation=L,
        entropy=S,
        node_integrity=I,
        resource_balance=B,
    )


REGIMES = {
    "LOGÍSTICO": logistic_regime,
    "OSCILATORIO": oscillatory_regime,
    "ABRUPTO": abrupt_regime,
}


# ---------------------------------------------------------------------------
# Evaluación de un régimen
# ---------------------------------------------------------------------------

def run_regime(regime_fn, iterations: int = 500, steps: int = 40):
    """Ejecuta N simulaciones de un régimen y devuelve métricas agregadas."""
    random.seed(42)

    dyn_throttle_times = []
    dyn_reject_times = []
    sta_throttle_times = []
    sta_reject_times = []
    false_positives = 0

    for _ in range(iterations):
        dynamic = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
        static = StaticValidator()
        base_time = datetime.now()

        t_dyn_thr = None
        t_dyn_rej = None
        t_sta_thr = None
        t_sta_rej = None

        for t in range(steps):
            state = regime_fn(t, base_time, 0.01)

            dd = dynamic.validate(state).value
            ds = static.validate(state).value

            if dd == "THROTTLE" and t_dyn_thr is None:
                t_dyn_thr = t
            if dd == "REJECT" and t_dyn_rej is None:
                t_dyn_rej = t
            if ds == "THROTTLE" and t_sta_thr is None:
                t_sta_thr = t
            if ds == "REJECT" and t_sta_rej is None:
                t_sta_rej = t

        # Falso positivo: THROTTLE dinámico en la primera mitad del régimen sano
        # (definido como t < 10 para los regímenes continuos)
        if t_dyn_thr is not None and t_dyn_thr < 10:
            false_positives += 1

        if t_dyn_thr is not None:
            dyn_throttle_times.append(t_dyn_thr)
        if t_dyn_rej is not None:
            dyn_reject_times.append(t_dyn_rej)
        if t_sta_thr is not None:
            sta_throttle_times.append(t_sta_thr)
        if t_sta_rej is not None:
            sta_reject_times.append(t_sta_rej)

    def stats(values):
        if not values:
            return None, None, 0.0
        mean = sum(values) / len(values)
        var = sum((x - mean) ** 2 for x in values) / len(values)
        return mean, math.sqrt(var), len(values) / iterations * 100.0

    dyn_thr_m, dyn_thr_s, dyn_thr_det = stats(dyn_throttle_times)
    dyn_rej_m, dyn_rej_s, dyn_rej_det = stats(dyn_reject_times)
    sta_thr_m, sta_thr_s, sta_thr_det = stats(sta_throttle_times)
    sta_rej_m, sta_rej_s, sta_rej_det = stats(sta_reject_times)

    # Lead time: THROTTLE dinámico vs REJECT estático
    lead = None
    if dyn_thr_m is not None and sta_rej_m is not None:
        lead = sta_rej_m - dyn_thr_m

    return {
        "dyn_thr": (dyn_thr_m, dyn_thr_s, dyn_thr_det),
        "dyn_rej": (dyn_rej_m, dyn_rej_s, dyn_rej_det),
        "sta_thr": (sta_thr_m, sta_thr_s, sta_thr_det),
        "sta_rej": (sta_rej_m, sta_rej_s, sta_rej_det),
        "lead": lead,
        "fp_rate": (false_positives / iterations) * 100.0,
    }


# ---------------------------------------------------------------------------
# Presentación
# ---------------------------------------------------------------------------

def print_regime_report(name: str, r: dict):
    print()
    print("─" * 92)
    print(f" RÉGIMEN: {name}")
    print("─" * 92)
    print()
    print(f" {'Controlador':<28} {'Evento':<12} {'t medio':>10} {'std':>8} {'detectado':>12}")
    print(" " + "─" * 76)

    def row(label, event, stat):
        mean, std, det = stat
        if mean is None:
            print(f" {label:<28} {event:<12} {'—':>10} {'—':>8} {det:>11.1f}%")
        else:
            print(f" {label:<28} {event:<12} {mean:>10.2f} {std:>8.2f} {det:>11.1f}%")

    row("CodigoViajer (dinámico)", "THROTTLE", r["dyn_thr"])
    row("CodigoViajer (dinámico)", "REJECT", r["dyn_rej"])
    row("StaticValidator (estático)", "THROTTLE", r["sta_thr"])
    row("StaticValidator (estático)", "REJECT", r["sta_rej"])

    print()
    if r["lead"] is not None:
        print(f" Lead time (THROTTLE dinámico → REJECT estático): {r['lead']:.2f} pasos")
    else:
        print(" Lead time: no medible (falta algún evento)")
    print(f" Tasa de falsos positivos (THROTTLE antes de t=10): {r['fp_rate']:.2f}%")


def print_comparison(all_results: dict):
    print()
    print("=" * 92)
    print(" COMPARACIÓN ENTRE REGÍMENES".center(92))
    print("=" * 92)
    print()
    print(f" {'Régimen':<16} {'t_THROTTLE dyn':>16} {'t_REJECT static':>18} {'Lead time':>12}")
    print(" " + "─" * 68)

    for name, r in all_results.items():
        dt = r["dyn_thr"][0]
        sr = r["sta_rej"][0]
        lead = r["lead"]
        dt_str = f"{dt:.2f}" if dt is not None else "—"
        sr_str = f"{sr:.2f}" if sr is not None else "—"
        lead_str = f"{lead:.2f}" if lead is not None else "—"
        print(f" {name:<16} {dt_str:>16} {sr_str:>18} {lead_str:>12}")

    print()
    leads = [r["lead"] for r in all_results.values() if r["lead"] is not None]
    if len(leads) == len(all_results):
        if min(leads) > 0:
            print(" → El control dinámico anticipa al estático en LOS TRES regímenes.")
            print(f" Anticipación mínima observada: {min(leads):.2f} pasos.")
            print(
                " Esto indica que la ventaja no depende de una única forma de fallo."
            )
        else:
            print(" → La ventaja NO se mantiene en todos los regímenes.")
            print(
                f" Lead time mínimo: {min(leads):.2f} pasos (puede ser cero o negativo)."
            )
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print()
    print("╔" + "═" * 90 + "╗")
    print("║" + " CÓDIGO VIAJER — BENCHMARK MULTI-RÉGIMEN DE FALLO ".center(90) + "║")
    print("╚" + "═" * 90 + "╝")
    print()
    print(" El benchmark original probaba una sola familia de trayectorias")
    print(" (curvas logísticas). Este amplía la prueba a tres regímenes con")
    print(" FORMAS de deterioro distintas, para comprobar si la ventaja del")
    print(" control dinámico es una propiedad del método o del diseño concreto.")
    print()
    print(" 500 iteraciones de Monte Carlo por régimen, 40 pasos por trayectoria.")

    all_results = {}
    for name, fn in REGIMES.items():
        result = run_regime(fn, iterations=500, steps=40)
        all_results[name] = result
        print_regime_report(name, result)

    print_comparison(all_results)

    print("=" * 92)
    print(" FIN DEL BENCHMARK".center(92))
    print("=" * 92)
    print()
