"""
test_validator.py — Tests unitarios para el Código Viajer (v1.0.0)
==================================================================
Ejecutar con: python -m pytest test_validator.py -v
O simplemente: python test_validator.py
"""

import math
from datetime import datetime, timedelta
from validator import (
    CodigoViajerValidator,
    StaticValidator,
    AgentState,
    Decision,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_state(L=1.0, S=0.0, I=1.0, B=1.0, days=0):
    """Factory de AgentState con valores por defecto en el atractor."""
    return AgentState(
        timestamp=datetime(2026, 1, 1) + timedelta(days=days),
        life_preservation=L,
        entropy=S,
        node_integrity=I,
        resource_balance=B,
    )


# ---------------------------------------------------------------------------
# CodigoViajerValidator
# ---------------------------------------------------------------------------

def test_perfect_state_is_allowed():
    v = CodigoViajerValidator()
    assert v.validate(make_state()) == Decision.ALLOW


def test_life_below_05_is_rejected():
    v = CodigoViajerValidator()
    assert v.validate(make_state(L=0.49)) == Decision.REJECT


def test_integrity_below_05_is_rejected():
    v = CodigoViajerValidator()
    assert v.validate(make_state(I=0.49)) == Decision.REJECT


def test_exactly_at_05_boundary_is_not_rejected():
    """L < 0.50 es REJECT; L == 0.50 exacto no lo es."""
    v = CodigoViajerValidator()
    # L == 0.50 no dispara el invariante (es estrictamente < 0.50)
    assert v.validate(make_state(L=0.50)) != Decision.REJECT
    # I == 0.50 tampoco dispara
    assert v.validate(make_state(I=0.50)) != Decision.REJECT


def test_rapid_entropy_spike_triggers_throttle():
    """Un salto grande de entropía en un solo paso debería disparar THROTTLE."""
    v = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)

    # Estado 1: armonía
    v.validate(make_state(L=1.0, S=0.02, I=1.0, B=1.0, days=0))
    # Estado 2: la entropía se dispara
    decision = v.validate(make_state(L=0.98, S=0.60, I=0.98, B=0.98, days=1))

    # Con S=0.60 debería estar en THROTTLE o REJECT, no en ALLOW
    assert decision != Decision.ALLOW


def test_gradual_drift_stays_allowed():
    """Una deriva muy lenta debe mantenerse en ALLOW."""
    v = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)

    S = 0.02
    for day in range(20):
        S = min(1.0, S + 0.005)
        decision = v.validate(make_state(L=0.99, S=S, I=0.99, B=0.99, days=day))

    # Una deriva tan lenta no debería disparar REJECT
    assert decision != Decision.REJECT


def test_collapse_to_reject_trajectory():
    """Trayectoria completa: armonía → deriva → colapso → REJECT."""
    v = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    decisions = []

    for t in range(36):
        p = t / 35.0
        L = max(0.0, min(1.0, 1.00 - 0.10 * p))
        S = max(0.0, min(1.0, 0.04 + 0.80 / (1.0 + math.exp(-1.70 * (t - 15.0)))))
        I = max(
            0.0,
            min(1.0, 0.96 - 0.10 * p - 0.50 / (1.0 + math.exp(-0.70 * (t - 30.0)))),
        )
        B = max(0.0, min(1.0, 1.00 - 0.12 * p))
        state = make_state(L=L, S=S, I=I, B=B, days=t)
        decisions.append(v.validate(state))

    # En algún momento debe aparecer REJECT (colapso de integridad)
    assert Decision.REJECT in decisions
    # THROTTLE debe aparecer antes que REJECT
    first_throttle = next(
        (i for i, d in enumerate(decisions) if d == Decision.THROTTLE), None
    )
    first_reject = next(
        (i for i, d in enumerate(decisions) if d == Decision.REJECT), None
    )
    if first_throttle is not None and first_reject is not None:
        assert first_throttle < first_reject, "THROTTLE debe preceder a REJECT"


def test_history_does_not_grow_indefinitely():
    """El historial debe respetar history_size."""
    v = CodigoViajerValidator(history_size=5)
    for day in range(20):
        v.validate(make_state(days=day))
    assert len(v.history) == 5


def test_evaluate_helical_distance_range():
    """Dh debe estar siempre en [0, 1]."""
    v = CodigoViajerValidator()
    for _ in range(10):
        v.validate(make_state())
    dh = v.evaluate_helical_distance(make_state())
    assert 0.0 <= dh <= 1.0


# ---------------------------------------------------------------------------
# StaticValidator
# ---------------------------------------------------------------------------

def test_static_perfect_state_allowed():
    v = StaticValidator()
    assert v.validate(make_state()) == Decision.ALLOW


def test_static_high_entropy_throttles():
    v = StaticValidator(s_threshold=0.60)
    assert v.validate(make_state(S=0.65)) == Decision.THROTTLE


def test_static_low_life_rejects():
    v = StaticValidator(l_threshold=0.50)
    assert v.validate(make_state(L=0.40)) == Decision.REJECT


def test_static_low_balance_throttles():
    v = StaticValidator(b_threshold=0.50)
    assert v.validate(make_state(B=0.40)) == Decision.THROTTLE


def test_static_reject_takes_priority_over_throttle():
    """Si un estado merece REJECT y THROTTLE, gana REJECT."""
    v = StaticValidator(l_threshold=0.50, s_threshold=0.60)
    # L < 0.50 → REJECT, S > 0.60 → THROTTLE. REJECT debe ganar.
    assert v.validate(make_state(L=0.40, S=0.70)) == Decision.REJECT


# ---------------------------------------------------------------------------
# Comparación dinámico vs estático
# ---------------------------------------------------------------------------

def test_dynamic_detects_earlier_than_static():
    """En la trayectoria canónica, el dinámico debe avisar antes que el estático."""
    dynamic = CodigoViajerValidator(max_velocity=0.50, max_acceleration=0.50)
    static = StaticValidator()

    t_dyn_throttle = None
    t_sta_reject = None

    base = datetime(2026, 1, 1)

    for t in range(36):
        p = t / 35.0
        L = max(0.0, min(1.0, 1.00 - 0.10 * p))
        S = max(0.0, min(1.0, 0.04 + 0.80 / (1.0 + math.exp(-1.70 * (t - 15.0)))))
        I = max(
            0.0,
            min(1.0, 0.96 - 0.10 * p - 0.50 / (1.0 + math.exp(-0.70 * (t - 30.0)))),
        )
        B = max(0.0, min(1.0, 1.00 - 0.12 * p))
        state = AgentState(
            timestamp=base + timedelta(days=t),
            life_preservation=L,
            entropy=S,
            node_integrity=I,
            resource_balance=B,
        )

        if dynamic.validate(state) == Decision.THROTTLE and t_dyn_throttle is None:
            t_dyn_throttle = t
        if static.validate(state) == Decision.REJECT and t_sta_reject is None:
            t_sta_reject = t

    assert t_dyn_throttle is not None, "El dinámico debería disparar THROTTLE"
    assert t_sta_reject is not None, "El estático debería disparar REJECT"
    assert t_dyn_throttle < t_sta_reject, (
        f"THROTTLE dinámico (t={t_dyn_throttle}) debe preceder a "
        f"REJECT estático (t={t_sta_reject})"
    )


# ---------------------------------------------------------------------------
# Runner sin pytest
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    # Descubre y ejecuta todos los tests definidos en este módulo
    tests = [
        (name, obj)
        for name, obj in list(globals().items())
        if name.startswith("test_") and callable(obj)
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            test_fn()
            print(f" ✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f" ✗ {name} — {e}")
            failed += 1
        except Exception as e:
            print(f" ✗ {name} — ERROR: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed de {len(tests)} tests")
    sys.exit(1 if failed else 0)
