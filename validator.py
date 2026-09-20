"""
validator.py - Módulo de Control Dinámico para el Código Viajer (v1.1.2)
Espacio de estados en R^4 con evaluación de trayectoria, velocidad y aceleración.
Soluciona la doble inserción en el historial mediante caché del estado y propiedad last_d_h.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from collections import deque
import math


class Decision(Enum):
    ALLOW = "ALLOW"
    THROTTLE = "THROTTLE"
    REJECT = "REJECT"


@dataclass
class AgentState:
    timestamp: datetime
    life_preservation: float # L in [0, 1]
    entropy: float # S in [0, 1]
    node_integrity: float # I in [0, 1]
    resource_balance: float # B in [0, 1]

    def to_vector(self) -> tuple[float, float, float, float]:
        return (self.life_preservation, self.entropy, self.node_integrity, self.resource_balance)


class CodigoViajerValidator:
    def __init__(
        self,
        reject_distance: float = 0.75,
        throttle_distance: float = 0.40,
        history_size: int = 20,
        max_velocity: float = 1.0,
        max_acceleration: float = 2.0,
        w_p: float = 0.60,
        w_v: float = 0.25,
        w_a: float = 0.15,
    ):
        self.reject_distance = reject_distance
        self.throttle_distance = throttle_distance
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.w_p = w_p
        self.w_v = w_v
        self.w_a = w_a
        self.history = deque(maxlen=history_size)
        self.attractor = (1.0, 0.0, 1.0, 1.0) # E = (L=1, S=0, I=1, B=1)
        self._last_d_h = 0.0

    @property
    def last_d_h(self) -> float:
        """Devuelve la última distancia helicoidal calculada sin alterar el historial."""
        return self._last_d_h

    def _euclidean_distance(self, v1, v2) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def _calculate_derivatives(self) -> tuple[tuple, tuple]:
        if len(self.history) < 2:
            return (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)

        curr = self.history[-1]
        prev = self.history[-2]
        dt = (curr.timestamp - prev.timestamp).total_seconds()
        if dt <= 0:
            dt = 1e-6

        v_curr = tuple((c - p) / dt for c, p in zip(curr.to_vector(), prev.to_vector()))

        if len(self.history) < 3:
            return v_curr, (0.0, 0.0, 0.0, 0.0)

        prev_2 = self.history[-3]
        dt_prev = (prev.timestamp - prev_2.timestamp).total_seconds() or 1e-6
        v_prev = tuple((p - p2) / dt_prev for p, p2 in zip(prev.to_vector(), prev_2.to_vector()))

        a_curr = tuple((vc - vp) / dt for vc, vp in zip(v_curr, v_prev))
        return v_curr, a_curr

    def compute_distance_and_update(self, state: AgentState) -> float:
        """Calcula D_h y actualiza la trayectoria en el historial exactamente UNA vez por tick."""
        d_p = self._euclidean_distance(state.to_vector(), self.attractor) / 2.0

        self.history.append(state)
        v_vec, a_vec = self._calculate_derivatives()

        norm_v = self._euclidean_distance(v_vec, (0, 0, 0, 0)) / self.max_velocity
        norm_a = self._euclidean_distance(a_vec, (0, 0, 0, 0)) / self.max_acceleration

        d_v = min(1.0, norm_v)
        d_a = min(1.0, norm_a)

        self._last_d_h = min(1.0, self.w_p * d_p + self.w_v * d_v + self.w_a * d_a)
        return self._last_d_h

    def validate(self, state: AgentState) -> Decision:
        """Evalúa las invariantes absolutas y la trayectoria en R^4."""
        # 1. Invariantes constitucionales absolutos (Hard Thresholds)
        if state.life_preservation < 0.50 or state.node_integrity < 0.50:
            self.compute_distance_and_update(state)
            return Decision.REJECT

        # 2. Evaluación de trayectoria dinámica en R^4
        d_h = self.compute_distance_and_update(state)

        if d_h >= self.reject_distance:
            return Decision.REJECT
        elif d_h >= self.throttle_distance:
            return Decision.THROTTLE
        return Decision.ALLOW

  
      
