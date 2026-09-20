"""
benchmark_governance.py - Benchmark Falsable de Gobernanza Digital (v1.1.2)
Demuestra la detección preventiva (THROTTLE) frente a un controlador estático (Naive).
"""

from datetime import datetime, timedelta
from validator import AgentState, CodigoViajerValidator, Decision


class NaiveValidator:
    """Controlador estático sin historia ni derivadas (basado en umbrales rígidos)."""

    def validate(self, state: AgentState) -> Decision:
        if state.life_preservation < 0.50 or state.node_integrity < 0.50 or state.entropy > 0.75:
            return Decision.REJECT
        elif state.entropy > 0.50:
            return Decision.THROTTLE
        return Decision.ALLOW


def run_benchmark():
    # Instanciamos usando los valores por defecto optimizados de validator.py
    viajer_validator = CodigoViajerValidator(
        reject_distance=0.75,
        throttle_distance=0.35,
        history_size=20,
        max_velocity=0.5,
        max_acceleration=0.5,
        w_p=0.40,
        w_v=0.35,
        w_a=0.25,
    )
    naive_validator = NaiveValidator()

    base_date = datetime(2026, 10, 1, 0, 0, 0)
    timeline = []

    # Fase 1: Armonía (Días 1-10)
    for day in range(1, 11):
        timeline.append((
            f"Día {day:02d} [Armonía]",
            AgentState(base_date + timedelta(days=day), 0.92, 0.08, 0.95, 0.90),
        ))

    # Fase 2: Deriva Silenciosa y Aceleración de Entropía (Días 11-18)
    entropy_ramp = [0.12, 0.18, 0.28, 0.42, 0.55, 0.62, 0.68, 0.72]
    integrity_ramp = [0.93, 0.90, 0.86, 0.81, 0.76, 0.70, 0.65, 0.60]
    for idx, day in enumerate(range(11, 19)):
        timeline.append((
            f"Día {day:02d} [Deriva]",
            AgentState(
                base_date + timedelta(days=day),
                0.88 - (idx * 0.02),
                entropy_ramp[idx],
                integrity_ramp[idx],
                0.85 - (idx * 0.03),
            ),
        ))

    # Fase 3: Colapso Constitucional (Días 19-25)
    for idx, day in enumerate(range(19, 26)):
        timeline.append((
            f"Día {day:02d} [Colapso]",
            AgentState(
                base_date + timedelta(days=day),
                max(0.70 - (idx * 0.08), 0.20),
                min(0.75 + (idx * 0.04), 0.98),
                max(0.55 - (idx * 0.08), 0.15),
                max(0.60 - (idx * 0.08), 0.10),
            ),
        ))

    print("=" * 85)
    print(" EVALUACIÓN COMPARATIVA ATÓMICA: CÓDIGO VIAJER (DINÁMICO) VS. NAIVE (ESTÁTICO)")
    print("=" * 85)
    print(
        f"{'TIMELINE':<20} | {'L':<4} | {'S':<4} | {'I':<4} | {'B':<4} | {'D_h':<6} | {'VIAJER (R^4)':<13} | {'NAIVE (Umbral)'}"
    )
    print("-" * 85)

    v_throttle_day, n_throttle_day = None, None

    for label, state in timeline:
        d_viajer = viajer_validator.validate(state)
        d_naive = naive_validator.validate(state)
        
        d_h = viajer_validator.last_d_h

        if d_viajer == Decision.THROTTLE and v_throttle_day is None:
            v_throttle_day = label
        if d_naive == Decision.THROTTLE and n_throttle_day is None:
            n_throttle_day = label

        print(
            f"{label:<20} | {state.life_preservation:.2f} | {state.entropy:.2f} | {state.node_integrity:.2f} | "
            f"{state.resource_balance:.2f} | {d_h:.4f} | {d_viajer.value:<13} | {d_naive.value}"
        )

    print("=" * 85)
    print(" RESULTADOS DEL BENCHMARK:")
    print(f" -> Primer THROTTLE detectado por Código Viajer: {v_throttle_day}")
    print(f" -> Primer THROTTLE detectado por Modelo Naive: {n_throttle_day}")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmark()



   
         

  
       




        
           

   
     
    



    
             
           
    

   

  
        
   
