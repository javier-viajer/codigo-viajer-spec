# Código Viajer — Control de Estabilidad Dinámica en ℝ⁴ (v1.1.2)

Módulo de gobernanza preventiva e inmutable para sistemas de IA autónomos basado en un espacio de estados de cuatro dimensiones.

---

## Arquitectura Formal

El validador evalúa el estado del agente:

$$
\mathbf{X} = (L,S,I,B) \in \mathbb{R}^4
$$

donde:

* **L (Life Preservation):** Preservación de la vida o del agente.
* **S (Entropy):** Nivel de entropía o desviación operativa.
* **I (Node Integrity):** Integridad del nodo.
* **B (Resource Balance):** Balance de recursos.

Todos los parámetros están definidos en el intervalo:

$$
[0,1]
$$

El atractor constitucional se define como:

$$
E=(1.0,0.0,1.0,1.0)
$$

representando el estado de máxima preservación, mínima entropía, máxima integridad y equilibrio óptimo de recursos.

---

## Métrica de Distancia Helicoidal

La estabilidad del sistema se calcula mediante la distancia helicoidal:

$$
D_h=\min\left(1.0,\,
w_p d_p +
w_v d_v +
w_a d_a
\right)
$$

donde:

* **dₚ** = distancia euclídea normalizada al atractor.
* **dᵥ** = magnitud normalizada del vector velocidad.
* **dₐ** = magnitud normalizada del vector aceleración.

La evaluación incorpora:

* Posición actual del sistema.
* Velocidad de cambio.
* Aceleración de la trayectoria.

El modelo no evalúa únicamente el estado presente del agente, sino también su tendencia dinámica.

---

## Espacio de Estados Dinámico

La trayectoria evoluciona en un espacio de estados de cuatro dimensiones:

$$
\mathbf{X}(t)=(L,S,I,B)
$$

con:

$$
\mathbf{V}=\frac{d\mathbf{X}}{dt}
$$

y

$$
\mathbf{A}=\frac{d^2\mathbf{X}}{dt^2}
$$

Esto permite detectar procesos de deriva antes de que se produzcan fallos constitucionales explícitos.

---

## Calibración Canónica (v1.1.2)

### Pesos

```text
w_p = 0.40
w_v = 0.35
w_a = 0.25
```

### Límites

```text
v_max = 0.50
a_max = 0.50
```

### Umbrales

```text
THROTTLE >= 0.35
REJECT >= 0.75
```

### Invariantes Constitucionales

```text
L < 0.50 -> REJECT
I < 0.50 -> REJECT
```

Ninguna trayectoria puede vulnerar estos límites fundamentales independientemente de su puntuación dinámica.

---

## Propiedades del Modelo

✅ Espacio de estados en ℝ⁴

✅ Distancia helicoidal acotada en [0,1]

✅ Memoria temporal integrada

✅ Detección preventiva mediante velocidad y aceleración

✅ Independencia respecto a la frecuencia de muestreo mediante normalización temporal

✅ Compatible con extensiones a espacios de dimensión N

✅ Arquitectura apta para simulación y experimentación en sistemas complejos

---

## Benchmark Falsable

El proyecto incluye un benchmark reproducible que compara:

* **Código Viajer (Control Dinámico)**
* **Naive Validator (Control Estático)**

sobre una trayectoria sintética compuesta por:

1. Fase de armonía.
2. Fase de deriva progresiva.
3. Fase de colapso constitucional.

### Ejecución

```bash
python benchmark_stochastic.py
```

El objetivo del benchmark es evaluar la capacidad de detección preventiva de trayectorias de deterioro frente a un controlador basado exclusivamente en umbrales estáticos.

---

## Fundamentación Teórica y Recursos Relacionados

El presente módulo constituye una implementación experimental inspirada en el ecosistema conceptual y técnico desarrollado por **Javier Viajer**.

### Marco Teórico

* **Tratado de Gobernanza Unitaria:** Propuesta metodológica orientada al estudio de estabilidad institucional, soberanía nodular y contención de dinámicas de colapso en sistemas complejos.

* **Soy Pirámide** y **Pirámide-Parábola:** Obras que desarrollan los principios geométricos y conceptuales que inspiran la noción de trayectoria helicoidal utilizada como referencia teórica del modelo.

### Publicaciones

* **La traición de las IAs (La música del futuro)**
* Serie de ensayos sobre gobernanza unitaria publicados bajo el sello de autor **Javier Viajer**

### Ecosistema Digital

* Web: https://musicalcodes.es
* Patreon: https://www.patreon.com/c/JavierViajer

Estos materiales proporcionan contexto conceptual adicional para la interpretación de los principios y objetivos del proyecto.

## Archivos del Proyecto

| Archivo | Propósito |
|---|---|
| `validator.py` | Núcleo: `CodigoViajerValidator` (dinámico) y `StaticValidator` (estático) |
| `benchmark_stochastic.py` | Benchmark de Monte Carlo (1000 iteraciones) con tabla determinista |
| `generate_report.py` | Informe completo en consola: trayectoria, evolución de D_h y distribución del lead time — sin dependencias externas |
| `generate_plots.py` | Versión gráfica del informe (requiere `matplotlib` y `numpy`) |
| `test_validator.py` | 12 tests unitarios. Ejecutar con `python test_validator.py` o `python -m pytest test_validator.py -v` |
| `CASE_STUDY.md` | Caso de estudio reproducible con la trayectoria canónica |


## Archivos del Proyecto

| Archivo | Propósito |
|---|---|
| `validator.py` | Núcleo: `CodigoViajerValidator` (dinámico) y `StaticValidator` (estático) |
| `benchmark_stochastic.py` | Benchmark de Monte Carlo (1000 iteraciones) con tabla determinista |
| `benchmark_regimes.py` | Benchmark multi-régimen: logístico, oscilatorio y abrupto |
| `sensitivity_analysis.py` | Análisis de sensibilidad de pesos, umbrales y tamaño de histórico |
| `generate_report.py` | Informe completo en consola, sin dependencias externas |
| `generate_plots.py` | Versión gráfica del informe (requiere `matplotlib` y `numpy`) |
| `test_validator.py` | 12 tests unitarios |
| `CASE_STUDY.md` | Caso de estudio reproducible con la trayectoria canónica |

## Limitaciones conocidas

## Archivos del Proyecto

| Archivo | Propósito |
|---|---|
| `validator.py` | Núcleo: `CodigoViajerValidator` (dinámico) y `StaticValidator` (estático) |
| `benchmark_stochastic.py` | Benchmark de Monte Carlo (1.000 iteraciones) con tabla determinista |
| `benchmark_regimes.py` | Benchmark multi-régimen: logístico, oscilatorio y abrupto |
| `sensitivity_analysis.py` | Análisis de sensibilidad de pesos, umbrales y tamaño de histórico |
| `generate_report.py` | Informe completo en consola, sin dependencias externas |
| `generate_plots.py` | Versión gráfica del informe (requiere `matplotlib` y `numpy`) |
| `test_validator.py` | Tests unitarios del validador dinámico y estático |
| `CASE_STUDY.md` | Caso de estudio reproducible con la trayectoria canónica |

---

## Resultados

### Robustez frente a la forma del fallo

El control dinámico anticipa al validador estático en los tres regímenes
de fallo evaluados (500 iteraciones de Monte Carlo por régimen;
`benchmark_regimes.py`):

| Régimen | t THROTTLE dinámico | t REJECT estático | Lead time |
|---|---|---|---|
| Logístico (deriva suave) | 15.1 | 32.0 | 16.9 |
| Oscilatorio (amplitud creciente) | 14.6 | 34.1 | 19.4 |
| Abrupto (colapso en 5 pasos) | 29.2 | 32.5 | 3.3 |

La anticipación se mantiene positiva en los tres casos. Es máxima en las
derivas progresiva y oscilatoria (16.9 y 19.4 pasos) y se reduce al mínimo
(3.3 pasos) en el colapso abrupto, donde el margen temporal disponible es
intrínsecamente escaso.

### Robustez frente a la calibración

El análisis de sensibilidad (`sensitivity_analysis.py`) evalúa 231
combinaciones de pesos (w_p, w_v, w_a) con suma 1.0:

- Lead time medio global: 16.43 pasos
- Rango observado: [15.0, 17.0] pasos

La variación total es de 2 pasos, lo que indica que el resultado no depende
de la calibración canónica concreta: los pesos pueden redistribuirse dentro
de una malla amplia sin alterar de forma apreciable la anticipación.

---

## Limitaciones conocidas

- El benchmark usa trayectorias sintéticas diseñadas por el autor; no hay
  validación sobre datos de agentes reales.
- El origen de las cuatro dimensiones (L, S, I, B) en un sistema vivo no
  está especificado. El validador evalúa estados que alguien debe medir
  previamente.
- Los pesos y umbrales parten de una calibración inicial; el análisis de
  sensibilidad mide su influencia sobre el resultado, pero la elección de
  la malla evaluada sigue siendo del autor.
- El colapso abrupto limita la anticipación a 3.3 pasos, lo que sugiere que
  el método ofrece poco margen ante fallos que se consuman en muy pocos
  pasos.


## Licencia

Este proyecto se distribuye bajo la Licencia MIT.(LICENSE)

## Caso de Estudio Reproducible

El proyecto incluye un caso de estudio completo donde se compara el comportamiento del Código Viajer frente a un controlador estático tradicional.

El objetivo es demostrar la capacidad de detección preventiva de trayectorias de deterioro sistémico mediante el uso de posición, velocidad y aceleración dentro del espacio de estados.

Ver:
* [Caso de Estudio Completo (CASE_STUDY.md)](./CASE_STUDY.md)

---

> El Código Viajer no pretende sustituir los mecanismos de auditoría tradicionales, sino proporcionar una capa adicional de gobernanza preventiva basada en el análisis de trayectorias dinámicas y detección temprana de deriva sistémica.















