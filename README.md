# Código Viajer — Control de Estabilidad Dinámica en $\mathbb{R}^4$ (v1.1.2)

Módulo de gobernanza preventiva e inmutable para sistemas de IA autónomos basado en el espacio de estados de cuatro dimensiones.

## Arquitectura Formal

El validador evalúa el estado del agente $\mathbf{X} = (L, S, I, B) \in \mathbb{R}^4$:
* **$L$ (Life Preservation):** Preservación de la vida/agente $[0, 1]$.
* **$S$ (Entropy):** Nivel de entropía / desviación operativa $[0, 1]$.
* **$I$ (Node Integrity):** Integridad del nodo $[0, 1]$.
* **$B$ (Resource Balance):** Balance de recursos $[0, 1]$.

El atractor constitucional se sitúa en $E = (1.0, 0.0, 1.0, 1.0)$.

### Métrica de Distancia Helicoidal ($D_h$)

$$D_h = \min\left(1.0, w_p \cdot d_p + w_v \cdot d_v + w_a \cdot d_a\right)$$

Donde:
* $d_p$: Distancia euclídea normalizada al atractor $E$.
* $d_v$: Magnitud normalizada de la velocidad $\Vert{} \mathbf{V} \Vert{} / v_{\max}$.
* $d_a$: Magnitud normalizada de la aceleración $\Vert{} \mathbf{A} \Vert{} / a_{\max}$.

### Calibración Canónica (v1.1.2)
* **Weights:** $w_p = 0.40$, $w_v = 0.35$, $w_a = 0.25$
* **Limites:** $v_{\max} = 0.5$, $a_{\max} = 0.5$
* **Thresholds:** `THROTTLE` $\ge 0.35$, `REJECT` $\ge 0.75$
* **Hard Invariants:** $L < 0.50 \lor I < 0.50 \implies \text{REJECT}$

## Ejecución del Benchmark Falsable

```bash
python benchmark_governance.py


 


   
    
 
  

   
            
      



