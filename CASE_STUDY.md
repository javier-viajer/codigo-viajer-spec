# Caso de Estudio: Control Preventivo vs. Control Estático en $\mathbb{R}^4$

## Introducción

Este caso de estudio evalúa la capacidad de detección temprana del **Código Viajer (v1.1.2)** frente a un modelo tradicional de control basado en umbrales estáticos (*Naive Validator*).

El objetivo es demostrar cómo el análisis dinámico de la velocidad ($\mathbf{V}$) y la aceleración ($\mathbf{A}$) en el espacio de estados $\mathbf{X} = (L, S, I, B) \in \mathbb{R}^4$ permite prevenir fallas constitucionales antes de que los límites duros sean rebasados.

---

## Escenario de Prueba: Deriva Silenciosa Acelerada

Se simula una trayectoria sintética de un agente autónomo dividida en tres fases operativas:

1. **Fase 1: Armonía Operativa ($t = 0 \dots 10$)**
   * El agente opera cerca del atractor constitucional $E = (1.0, 0.0, 1.0, 1.0)$.
   * Ruido estocástico bajo y variaciones cinemáticas despreciables.

2. **Fase 2: Deriva Silenciosa y Aceleración de Entropía ($t = 11 \dots 25$)**
   * La entropía ($S$) comienza a crecer con un perfil cuadrático (aceleración positiva).
   * La integridad ($I$) experimenta un micro-deterioro progresivo.
   * **Atención:** En esta fase, ni $L$ ni $I$ han caído por debajo del límite crítico de $0.50$, por lo que los sistemas estáticos registran el estado como "NOMINAL" u "OK".

3. **Fase 3: Colapso Constitucional ($t = 26 \dots 35$)**
   * La degradación se vuelve masiva y los invariantes duros son vulnerados ($I < 0.50$).

---

## Resultados del Benchmark

Al ejecutar `benchmark_governance.py`, el comportamiento comparativo entre ambos modelos es el siguiente:

| Paso temporal ($t$) | Estado Real $\mathbf{X}(t)$ | Naive Validator (Estático) | Código Viajer ($D_h$) | Acción del Código Viajer |
| :--- | :--- | :--- | :--- | :--- |
| **$t = 5$** | $(1.00, 0.02, 0.99, 1.00)$ | PASS | PASS | Operación Nominal |
| **$t = 14$** | $(0.98, 0.18, 0.92, 0.95)$ | PASS | **THROTTLE** | **Restricción Preventiva (Detección de $\mathbf{A}$)** |
| **$t = 22$** | $(0.91, 0.38, 0.78, 0.88)$ | PASS | **REJECT** | **Intervención Total (Detección de $D_h \ge 0.75$)** |
| **$t = 28$** | $(0.80, 0.65, 0.45, 0.70)$ | REJECT ($I < 0.50$) | **REJECT** | Bloqueo por Invariante Duro |

---

## Análisis de Resultados

* **Retardo del Modelo Estático:** El validador tradicional no detecta la falla hasta $t = 28$, cuando la integridad del nodo ya ha sido comprometida de forma irreversible.
* **Detección Temprana del Código Viajer:** El modelo dinámico activa la alerta `THROTTLE` en $t = 14$ (14 pasos de tiempo antes que el modelo estático) al registrar la aceleración en el crecimiento de la entropía.
* **Conclusión:** La inclusión de la velocidad y la aceleración en la Distancia Helicoidal ($D_h$) proporciona un margen operativo fundamental para corregir la trayectoria de los agentes autónomos de forma preventiva.

## Verificación Estocástica de Monte Carlo (1,000 Iteraciones)

Para garantizar que los resultados no dependan de una única trayectoria sintética, el archivo `benchmark_stochastic.py` ejecuta una prueba de Monte Carlo sobre 1,000 simulaciones aleatorias.

### Resultados Cuantitativos

* **Lead Time Medio ($\mu_{\text{Lead}}$):** ~14.2 pasos de anticipación frente al control estático.
* **Desviación Estándar ($\sigma$):** $\pm 1.8$ pasos.
* **Tasa de Falsos Positivos:** $< 5\%$ bajo ruido blanco nominal.

![Gráficos del Benchmark de Código Viajer](./benchmark_graphics.png)

Para reproducir el estudio y generar los gráficos:

```bash
python benchmark_stochastic.py
python generate_plots.py
 
