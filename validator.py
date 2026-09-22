"""
validator.py - Módulo de Control Dinámico para el Código Viajer (v1.1.3)
Espacio de estados en R^4 con evaluación de trayectoria, velocidad y aceleración.
Calibración de alta sensibilidad para detección preventiva de deriva.
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
        return (self.life_preservation, self.entropy,
                self.node_integrity, self.resource_balance)


class CodigoViajerValidator:
    """Validador dinámico basado en distancia helicoidal en R^4."""

    def __init__(
        self,
        reject_distance: float = 0.75,
        throttle_distance: float = 0.35,
        history_size: int = 20,
        max_velocity: float = 0.5,
        max_acceleration: float = 0.5,
        w_p: float = 0.40,
        w_v: float = 0.35,
        w_a: float = 0.25,
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

        # Normalización temporal a días/pasos unitarios
        dt = (curr.timestamp - prev.timestamp).total_seconds() / 86400.0
        if dt <= 0:
            dt = 1.0

        v_curr = tuple(
            (c - p) / dt for c, p in zip(curr.to_vector(), prev.to_vector())
        )

        if len(self.history) < 3:
            return v_curr, (0.0, 0.0, 0.0, 0.0)

        prev_2 = self.history[-3]
        dt_prev = (
            (prev.timestamp - prev_2.timestamp).total_seconds() / 86400.0
        ) or 1.0

        v_prev = tuple(
            (p - p2) / dt_prev
            for p, p2 in zip(prev.to_vector(), prev_2.to_vector())
        )

        a_curr = tuple((vc - vp) / dt for vc, vp in zip(v_curr, v_prev))
        return v_curr, a_curr

    def evaluate_helical_distance(self, state: AgentState) -> float:
        """Evaluación pura de D_h sobre el historial actual."""
        d_p = self._euclidean_distance(state.to_vector(), self.attractor) / 2.0
        v_vec, a_vec = self._calculate_derivatives()

        norm_v = self._euclidean_distance(v_vec, (0, 0, 0, 0)) / self.max_velocity
        norm_a = self._euclidean_distance(a_vec, (0, 0, 0, 0)) / self.max_acceleration

        d_v = min(1.0, norm_v)
        d_a = min(1.0, norm_a)

        return min(1.0, self.w_p * d_p + self.w_v * d_v + self.w_a * d_a)

    def validate(self, state: AgentState) -> Decision:
        """Registra el estado exactamente UNA vez por tick y evalúa la trayectoria."""
        self.history.append(state)
        self._last_d_h = self.evaluate_helical_distance(state)

        # Invariantes constitucionales duros
        if state.life_preservation < 0.50 or state.node_integrity < 0.50:
            return Decision.REJECT

        # Evaluación de umbrales helicoidales
        if self._last_d_h >= self.reject_distance:
            return Decision.REJECT
        elif self._last_d_h >= self.throttle_distance:
            return Decision.THROTTLE

        return Decision.ALLOW


class StaticValidator:
    """Validador estático competitivo para benchmarks justos.

    A diferencia de una simple comprobación de invariantes duros,
    este validador aplica umbrales sobre las cuatro dimensiones
    y sobre la entropía, que es el indicador más temprano de deriva.
    """

    def __init__(
        self,
        l_threshold: float = 0.50,
        s_threshold: float = 0.60,
        i_threshold: float = 0.50,
        b_threshold: float = 0.50,
    ):
        self.l_threshold = l_threshold
        self.s_threshold = s_threshold
        self.i_threshold = i_threshold
        self.b_threshold = b_threshold

    def validate(self, state: AgentState) -> Decision:
        if state.life_preservation < self.l_threshold:
            return Decision.REJECT
        if state.node_integrity < self.i_threshold:
            return Decision.REJECT
        if state.entropy > self.s_threshold:
            return Decision.THROTTLE
        if state.resource_balance < self.b_threshold:
            return Decision.THROTTLE
        return Decision.ALLOW

 
        
      
       

       
      
       

  

    
     
       

  
      
