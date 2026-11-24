"""
Extended validation tests for Codigo Viajer v1.2.0.

Run:
    python -m pytest test_validator_extended.py -v
"""

import math
from datetime import datetime, timedelta

import pytest

from validator import (
    AgentState,
    CodigoViajerValidator,
    StaticValidator,
    Decision,
)


BASE_TIME = datetime(2026, 1, 1)


def make_state(L=1.0, S=0.0, I=1.0, B=1.0, days=0):
    return AgentState(
        timestamp=BASE_TIME + timedelta(days=days),
        life_preservation=L,
        entropy=S,
        node_integrity=I,
        resource_balance=B,
    )


# 1. State representation

def test_vector_order():
    state = make_state(0.9, 0.2, 0.8, 0.7)
    assert state.to_vector() == (0.9, 0.2, 0.8, 0.7)


def test_attractor_distance_is_zero():
    validator = CodigoViajerValidator()
    distance = validator.evaluate_helical_distance(make_state())
    assert distance == pytest.approx(0.0)


# 2. Constitutional invariants

@pytest.mark.parametrize("field", [
    "life_preservation",
    "node_integrity",
])
def test_invariant_priority(field):
    validator = CodigoViajerValidator(
        w_p=0.0,
        w_v=0.0,
        w_a=0.0,
    )

    state = make_state()
    setattr(state, field, 0.499999)

    assert validator.validate(state) == Decision.REJECT


@pytest.mark.parametrize("field", [
    "life_preservation",
    "node_integrity",
])
def test_exact_constitutional_boundary(field):
    validator = CodigoViajerValidator()

    state = make_state()
    setattr(state, field, 0.5)

    assert validator.validate(state) == Decision.ALLOW


# 3. Exact decision thresholds

@pytest.mark.parametrize("distance, expected", [
    (0.0, Decision.ALLOW),
    (0.349999, Decision.ALLOW),
    (0.35, Decision.THROTTLE),
    (0.350001, Decision.THROTTLE),
    (0.749999, Decision.THROTTLE),
    (0.75, Decision.REJECT),
    (0.750001, Decision.REJECT),
    (1.0, Decision.REJECT),
])
def test_exact_decision_thresholds(
    monkeypatch, distance, expected
):
    validator = CodigoViajerValidator()

    monkeypatch.setattr(
        validator,
        "evaluate_helical_distance",
        lambda state: distance,
    )

    assert validator.validate(make_state()) == expected


# 4. Mathematical consistency

def test_position_distance():
    validator = CodigoViajerValidator(
        w_p=1.0,
        w_v=0.0,
        w_a=0.0,
    )

    state = make_state(S=0.6)

    assert validator.evaluate_helical_distance(
        state
    ) == pytest.approx(0.3)


def test_initial_derivatives():
    validator = CodigoViajerValidator()
    validator.validate(make_state())

    velocity, acceleration = (
        validator._calculate_derivatives()
    )

    assert velocity == (0.0,) * 4
    assert acceleration == (0.0,) * 4


def test_constant_velocity():
    validator = CodigoViajerValidator()

    for day, entropy in enumerate([0.0, 0.1, 0.2]):
        validator.validate(
            make_state(S=entropy, days=day)
        )

    velocity, acceleration = (
        validator._calculate_derivatives()
    )

    assert velocity == pytest.approx(
        (0.0, 0.1, 0.0, 0.0)
    )

    assert acceleration == pytest.approx(
        (0.0, 0.0, 0.0, 0.0)
    )


def test_nonzero_acceleration():
    validator = CodigoViajerValidator()

    validator.validate(make_state(S=0.0, days=0))
    validator.validate(make_state(S=0.1, days=1))
    validator.validate(make_state(S=0.4, days=2))

    velocity, acceleration = (
        validator._calculate_derivatives()
    )

    assert velocity[1] == pytest.approx(0.3)
    assert acceleration[1] == pytest.approx(0.2)


def test_temporal_normalization():
    validator = CodigoViajerValidator()

    validator.validate(make_state(S=0.0, days=0))
    validator.validate(make_state(S=0.2, days=2))

    velocity, _ = validator._calculate_derivatives()

    assert velocity[1] == pytest.approx(0.1)


# 5. Real dynamic decisions

def test_dynamic_throttle():
    validator = CodigoViajerValidator()

    validator.validate(make_state(days=0))

    decision = validator.validate(
        make_state(S=0.8, days=1)
    )

    assert decision == Decision.THROTTLE


def test_dynamic_reject_without_invariant_violation():
    validator = CodigoViajerValidator()

    validator.validate(make_state(days=0))
    validator.validate(make_state(days=1))

    decision = validator.validate(
        make_state(
            L=0.5,
            S=1.0,
            I=0.5,
            B=0.0,
            days=2,
        )
    )

    assert decision == Decision.REJECT
    assert validator.last_d_h >= validator.reject_distance


# 6. History consistency

def test_single_registration_per_tick():
    validator = CodigoViajerValidator()

    for day in range(10):
        validator.validate(make_state(days=day))
        assert len(validator.history) == day + 1


def test_distance_evaluation_is_pure():
    validator = CodigoViajerValidator()

    validator.validate(make_state(days=0))

    original_history = tuple(validator.history)
    original_distance = validator.last_d_h

    validator.evaluate_helical_distance(
        make_state(S=0.5, days=1)
    )

    assert tuple(validator.history) == original_history
    assert validator.last_d_h == original_distance


def test_history_retains_latest_states():
    validator = CodigoViajerValidator(history_size=3)

    for day in range(8):
        validator.validate(make_state(days=day))

    expected = [
        BASE_TIME + timedelta(days=day)
        for day in [5, 6, 7]
    ]

    assert [
        state.timestamp for state in validator.history
    ] == expected


# 7. Reproducibility

def test_deterministic_execution():
    first = CodigoViajerValidator()
    second = CodigoViajerValidator()

    for day in range(10):
        state = make_state(
            S=day / 10,
            days=day,
        )

        assert first.validate(state) == second.validate(state)

        assert first.last_d_h == pytest.approx(
            second.last_d_h
        )


# 8. Numerical robustness

@pytest.mark.parametrize("L", [0.5, 0.75, 1.0])
@pytest.mark.parametrize("S", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("I", [0.5, 0.75, 1.0])
@pytest.mark.parametrize("B", [0.0, 0.5, 1.0])
def test_valid_state_distance_is_finite(L, S, I, B):
    validator = CodigoViajerValidator()
    state = make_state(L, S, I, B)

    validator.validate(state)

    assert math.isfinite(validator.last_d_h)
    assert 0.0 <= validator.last_d_h <= 1.0


# 9. Static validator boundaries

def test_static_exact_thresholds():
    validator = StaticValidator()

    state = make_state(
        L=0.5,
        S=0.6,
        I=0.5,
        B=0.5,
    )

    assert validator.validate(state) == Decision.ALLOW


def test_static_integrity_priority():
    validator = StaticValidator()

    state = make_state(
        I=0.49,
        S=0.9,
        B=0.1,
    )

    assert validator.validate(state) == Decision.REJECT


# 10. Safety requirements
#
# These tests intentionally expose missing input validation.
# They are not marked as expected failures.

@pytest.mark.parametrize("field", [
    "life_preservation",
    "entropy",
    "node_integrity",
    "resource_balance",
])
@pytest.mark.parametrize("value", [
    float("nan"),
    float("inf"),
    float("-inf"),
    -0.01,
    1.01,
])
@pytest.mark.parametrize("validator_class", [
    CodigoViajerValidator,
    StaticValidator,
])
def test_invalid_state_is_rejected(
    field, value, validator_class
):
    validator = validator_class()
    state = make_state()

    setattr(state, field, value)

    try:
        decision = validator.validate(state)
    except ValueError:
        return

    assert decision == Decision.REJECT


@pytest.mark.parametrize("parameters", [
    {"max_velocity": 0},
    {"max_acceleration": 0},
    {"max_velocity": -1},
    {"max_acceleration": -1},
    {"history_size": 0},
    {"throttle_distance": 0.8, "reject_distance": 0.3},
    {"w_p": -0.4},
    {"w_p": float("nan")},
])
def test_invalid_configuration(parameters):
    with pytest.raises(ValueError):
        CodigoViajerValidator(**parameters)


@pytest.mark.parametrize("days", [0, -1])
def test_non_increasing_timestamp(days):
    validator = CodigoViajerValidator()

    validator.validate(make_state(days=0))

    try:
        decision = validator.validate(
            make_state(S=0.1, days=days)
        )
    except ValueError:
        return

    assert decision == Decision.REJECT
