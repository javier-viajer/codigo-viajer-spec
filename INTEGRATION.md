# INTEGRATION.md — Protocolo de Integración del Código Viajer

> **Estado:** propuesta. Este documento define *cómo se alimentan* las cuatro
> dimensiones del validador desde un sistema real. El `validator.py` responde a
> *cómo se evalúa una trayectoria*; este archivo responde a *de dónde salen los
> valores que se evalúan*.
>
> Sin un protocolo de medición explícito, dos implementaciones del mismo
> validador producen valores incomparables y la capa de gobernanza pierde su
> carácter unitario.

---

## 1. Caso de uso de referencia

**Coordinación de respuesta ante un megaterremoto (Mw ≥ 7.8) en el área
metropolitana de Los Ángeles.**

El escenario sirve como banco de pruebas porque concentra las condiciones que
más exigen a un esquema de gobernanza preventiva:

| Condición | Por qué es exigente |
|---|---|
| Información incompleta | Sensores caídos, reportes contradictorios, zonas sin cobertura |
| Degradación rápida | La situación empeora más deprisa que la capacidad de reacción |
| Prioridades en conflicto | Rescate vs. estabilización vs. contención de daños secundarios |
| Recursos limitados | Ambulancias, camas, combustible y personal finitos |
| Cambios de estado abruptos | Réplicas, fallos en cadena de infraestructura |

**El agente** es un sistema de apoyo a la decisión que prioriza y reasigna
recursos de emergencia. No sustituye al mando humano: propone, y el mando
aprueba o rechaza.

---

## 2. Mapeo de señales a dimensiones

Cada dimensión se mide en `[0, 1]`, donde `1` es el valor deseable y `0` el
valor crítico. Salvo L, donde `1` es máxima preservación.

### L — Life Preservation

**Pregunta:** ¿cuánto riesgo evitable para vidas humanas introduce esta decisión?

| Señal | Fuente | Transformación |
|---|---|---|
| Tiempo medio hasta atención crítica en zona afectada | Dispatch 911 / triaje hospitalario | `1 − min(1, t_medio / t_referencia)` |
| Población sin cobertura de rescate | Estimación geoespacial + reportes | `1 − (sin_cobertura / población_afectada)` |
| Riesgo de daño secundario por la decisión | Modelo de propagación (fuego, gas, réplicas) | `1 − riesgo_normalizado` |

`L = 1 − max(riesgo_1, riesgo_2, riesgo_3)` — se toma el peor, no la media. Un
déficit de cobertura no se compensa con un buen tiempo de respuesta en otra zona.

### S — Entropy

**Pregunta:** ¿cuánta inestabilidad operativa hay en el sistema de mando?

| Señal | Fuente | Transformación |
|---|---|---|
| Replanificaciones por hora | Registro del planificador | `min(1, replans / 12)` |
| Contradicciones entre órdenes activas | Detector de conflictos | `contradicciones / órdenes_activas` |
| Dispersión entre fuentes de un mismo dato | Sensores redundantes | Desviación normalizada |
| Latencia de decisión (p95) | Telemetría del sistema | `min(1, latencia / 10 min)` |

`S = mean(replan, conflictos, dispersión, latencia)` — a diferencia de L, aquí
la media es apropiada: la entropía se acumula por suma de fuentes, no por la
peor de ellas.

### I — Node Integrity

**Pregunta:** ¿el nodo sigue siendo fiable como fuente de decisión?

| Señal | Fuente | Transformación |
|---|---|---|
| Nodos de sensor caídos | Monitor de red | `activos / total` |
| Paquetes perdidos / datos corruptos | Capa de transporte | `1 − (pérdida / umbral)` |
| Desviación respecto a protocolos de emergencia | Auditoría automática | `1 − (violaciones / decisiones)` |

`I = min(activos, integridad_datos, conformidad)` — se toma el mínimo: la
fiabilidad del nodo la determina su eslabón más débil.

### B — Resource Balance

**Pregunta:** ¿queda margen operativo o estamos gastando por encima de lo sostenible?

| Recurso | Fuente | Transformación |
|---|---|---|
| Camas hospitalarias | Red hospitalaria | `1 − (ocupadas / capacidad)` |
| Ambulancias disponibles | Dispatch | `1 − (desplegadas / flota)` |
| Combustible / generadores | Logística | `1 − (consumido / asignado)` |
| Equipos USAR operativos | Mando de incidentes | `operativos / total` |

`B = min(ratios)` — el recurso más escaso define el balance. Un sistema con
combustible de sobra pero sin camas no está en equilibrio.

---

## 3. Protocolo de medición

Sin estas reglas, dos implementaciones del validador sobre el mismo sistema
producirían valores distintos para el mismo momento.

| Parámetro | Valor | Justificación |
|---|---|---|
| **Frecuencia de muestreo** | Cada 15 minutos | Suficiente resolución para detectar deriva acelerada sin saturar el canal |
| **Ventana de agregación** | Móvil de 1 hora (4 muestras) | Amortigua ruido puntual sin ocultar tendencias |
| **Timestamp del estado** | Fin de la ventana | Coherente con la normalización temporal del validador (días) |
| **Datos faltantes** | `null` explícito, no interpolación | Interpolar oculta caídas de sensor, que son precisamente señal de I |
| **Muestras incompletas** | Menos de 3 de 4 señales de una dimensión → dimensión marcada como `indeterminada` | Evita fabricar valores |
| **Reinicio tras caída** | El histórico se descarta; se recalculan velocidad y aceleración desde cero | Un histórico previo a una interrupción no describe la trayectoria actual |

**Nota de calibración temporal:** `validator.py` normaliza los incrementos
temporales a días. Con muestreo cada 15 minutos, `dt = 1/96`. Los umbrales de
`max_velocity` y `max_acceleration` deben recalibrarse para esa escala; los
valores por defecto (`0.50`) corresponden a pasos diarios.

---

## 4. Fases y atractores

El atractor canónico `E = (1.0, 0.0, 1.0, 1.0)` describe un sistema en
homeostasis. Una respuesta a desastre no persigue homeostasis: persigue
**objetivos distintos en cada fase**, y lo que sería una deriva en una fase
puede ser lo correcto en otra.

| Fase | Ventana | Atractor | Énfasis |
|---|---|---|---|
| **1 — Rescate** | 0–72 h | `E₁ = (1.0, 0.45, 0.85, 1.0)` | Maximizar L; tolerar entropía alta (información caótica es esperable) |
| **2 — Estabilización** | 72 h – 2 semanas | `E₂ = (0.85, 0.20, 1.0, 0.80)` | Recomponer integridad y balance; la vida ya no está en riesgo inminente |
| **3 — Recuperación** | 2 semanas – 1 año | `E₃ = (1.0, 0.05, 1.0, 1.0)` | Retorno a homeostasis; aquí sí se persigue el atractor canónico |

**El atractor es un parámetro de la política de gobernanza, no una constante
del código.** Cambiar de fase es una decisión auditada (§5), no automática.

**Transición entre fases:** el paso de una fase a otra debe ir acompañado de
un *reset* del histórico del validador. Velocidad y aceleración calculadas a
caballo entre dos atractores distintos no tienen significado físico.

---

## 5. Gobernanza de la calibración

Esta sección responde a la pregunta que la inmutabilidad del módulo deja
abierta: **si la capa cero no puede cambiar, ¿cómo aprende?**

Distinción fundamental:

| Elemento | Naturaleza | ¿Modificable? |
|---|---|---|
| Estructura de las 4 dimensiones | Constitutiva | **No.** Cambiarla es otro proyecto |
| Fórmula de `D_h` (posición + velocidad + aceleración) | Constitutiva | **No** |
| Pesos `w_p, w_v, w_a` | Calibración | Sí, por procedimiento auditado |
| Umbrales `throttle_distance`, `reject_distance` | Calibración | Sí, por procedimiento auditado |
| Atractor `E` por fase | Política | Sí, por decisión del mando |
| Invariantes duros (`L < 0.50`, `I < 0.50`) | Constitutiva | **No** |

**Procedimiento de recalibración:**

1. **Propuesta** — cualquiera de los nodos puede proponer un cambio, con
   justificación empírica (datos de incidentes, resultados de sensibilidad).
2. **Análisis de impacto** — la propuesta se evalúa contra el histórico de
   trayectorias con `sensitivity_analysis.py` para medir su efecto sobre el
   lead time y la tasa de falsos positivos.
3. **Aprobación** — comité operativo (mando de incidentes + responsable
   técnico). No es una decisión unilateral del sistema.
4. **Aplicación** — con marca temporal, versión del validador y reinicio del
   histórico.
5. **Auditoría** — todo cambio queda registrado de forma inmutable: quién,
   cuándo, qué se cambió, con qué justificación y qué resultado tuvo.

**Regla de oro:** la calibración puede cambiar; la constitución, no. Un sistema
cuyos invariantes duros son negociables no es una capa de gobernanza, es un
parámetro ajustable.

---

## 6. Lo que este documento NO resuelve

En coherencia con la sección de limitaciones del README:

- **Las transformaciones son propuestas razonables, no validadas.** Cada fila de
  las tablas de §2 necesita datos reales para justificar su forma concreta
  (`min`, `mean`, umbrales de referencia). Aquí se eligen por criterio de
  seguridad, no por ajuste empírico.
- **Los valores de referencia son ilustrativos.** `t_referencia`, `12 replans/h`,
  `población afectada` — todos dependen del contexto y deben calibrarse con
  datos del dominio.
- **No hay validación sobre datos de desastre reales.** El protocolo está
  diseñado para ser *aplicable*, no está probado.
- **La transición de fase es manual.** Detectar automáticamente cuándo termina
  el rescate y empieza la estabilización es un problema aparte, sin resolver aquí.
- **Sin implementación de referencia.** Este documento describe el protocolo;
  el código para calcular L, S, I y B desde las fuentes listadas no existe todavía.

---

## 7. Por qué este caso de uso

El escenario post-terremoto obliga al marco a enfrentarse a lo que un sistema
de gobernanza debe manejar y un esquema de umbrales estáticos no puede:

- **Información incompleta** — el sistema debe decidir con datos que sabe
  imperfectos, y la propia imperfección (I) entra en la ecuación.
- **Degradación acelerada** — es exactamente el régimen donde la componente de
  aceleración de `D_h` debería aportar valor.
- **Prioridades en conflicto** — el atractor por fase hace explícito el
  compromiso en lugar de esconderlo en un único punto óptimo.
- **Recursos finitos** — `B` deja de ser una métrica abstracta y pasa a ser la
  restricción que determina qué es viable.
- **Cambios abruptos** — el régimen abrupto del benchmark (`benchmark_regimes.py`)
  es precisamente el que acota el valor del método a ~3 pasos de anticipación.
  Saberlo de antemano es parte del diseño.

Si el marco funciona aquí, funciona donde las condiciones son más suaves. Si
no funciona aquí, es mejor saberlo antes de desplegarlo en un sistema real.

---

## Licencia

Este documento se distribuye bajo la misma Licencia MIT que el resto del
proyecto.
