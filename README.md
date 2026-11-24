```markdown
# Código Viajer — Control de Estabilidad Dinámica en ℝ⁴
**Versión canónica: v1.2.0**

Módulo experimental de gobernanza preventiva para sistemas de IA autónomos.
Evalúa trayectorias en un espacio de estados de cuatro dimensiones y emite
decisiones `ALLOW` / `THROTTLE` / `REJECT`.

> Este repositorio contiene dos capas relacionadas pero distintas:
>
> 1. **Código Viajer** — validador dinámico operativo (capa principal).
> 2. **TRCG** — marco matemático en desarrollo (carpeta `core/`, `dynamics/`, `boundary/`).
>
> No se afirma que la TRCG esté demostrada como teoría física completa.
> El estado epistemológico de cada módulo TRCG se detalla en [`STATUS.md`](./STATUS.md).

---

## 1. Arquitectura del Código Viajer

El validador evalúa el estado del agente:

$$
\mathbf{X} = (L, S, I, B) \in [0,1]^4
$$

| Símbolo | Nombre | Significado |
|--------:|--------|-------------|
| \(L\) | Life Preservation | Preservación de la vida / continuidad del agente |
| \(S\) | Entropy | Desviación operativa / desorden |
| \(I\) | Node Integrity | Integridad del nodo |
| \(B\) | Resource Balance | Balance de recursos |

Atractor constitucional de referencia:

$$
E = (1.0,\ 0.0,\ 1.0,\ 1.0)
$$

### Métrica dinámica \(D_h\)

$$
D_h = \min\big(1.0,\ w_p\, d_p + w_v\, d_v + w_a\, d_a\big)
$$

donde:

- \(d_p\) — distancia normalizada al atractor \(E\)
- \(d_v\) — magnitud normalizada de la velocidad \(\mathbf{V}\)
- \(d_a\) — magnitud normalizada de la aceleración \(\mathbf{A}\)

**Nota de rigor:** \(D_h\) es una **distancia dinámica ponderada** (posición + velocidad + aceleración).
El término “helicoidal” se usa en este proyecto como etiqueta histórica del corpus Viajer;
no implica por sí solo una hélice diferencial rigurosa en una variedad riemanniana.

### Calibración canónica (v1.2.0)

```text
w_p = 0.40
w_v = 0.35
w_a = 0.25

v_max = 0.50
a_max = 0.50

THROTTLE si D_h >= 0.35
REJECT si D_h >= 0.75
```

Invariantes constitucionales (prioridad máxima):

```text
L < 0.50 → REJECT
I < 0.50 → REJECT
```

---

## 2. Instalación y uso rápido

```bash
# Dependencias mínimas (estándar + opcionales de informe gráfico)
pip install -r requirements.txt

# Tests
python test_validator.py
# o:
python -m pytest test_validator.py -v

# Benchmark estocástico
python benchmark_stochastic.py

# Benchmark multi-régimen
python benchmark_regimes.py

# Sensibilidad de hiperparámetros
python sensitivity_analysis.py

# Informe en consola
python generate_report.py
```

Ejemplo mínimo:

```python
from datetime import datetime
from validator import CodigoViajerValidator, AgentState, Decision

v = CodigoViajerValidator()
state = AgentState(
    timestamp=datetime.utcnow(),
    life_preservation=0.98,
    entropy=0.10,
    node_integrity=0.97,
    resource_balance=0.95,
)
print(v.validate(state)) # Decision.ALLOW / THROTTLE / REJECT
```

---

## 3. Archivos del proyecto

| Archivo / carpeta | Propósito |
|-------------------|-----------|
| `validator.py` | Núcleo: `CodigoViajerValidator` y `StaticValidator` |
| `test_validator.py` | Tests unitarios |
| `benchmark_stochastic.py` | Monte Carlo + trayectoria determinista |
| `benchmark_regimes.py` | Regímenes logístico / oscilatorio / abrupto |
| `sensitivity_analysis.py` | Sensibilidad de pesos, umbrales e histórico |
| `generate_report.py` | Informe textual reproducible |
| `CASE_STUDY.md` | Caso de estudio |
| `INTEGRATION.md` | Protocolo de medición y calibración |
| `CONSTITUCION_UNITARIA.md` | Marco constitucional del corpus |
| `STATUS.md` | Niveles epistemológicos TRCG |
| `core/` | Símplex, MaxEnt y cierres |
| `dynamics/` | Jacobiano, torsión y reducciones |
| `boundary/` | Proyectores de contorno (`Π₂₃`, etc.) |
| `LICENSE` | MIT |

---

## 4. Resultados reproducibles (Código Viajer)

### Robustez frente a la forma del fallo

Control dinámico vs estático (`benchmark_regimes.py`; orden de magnitud de los experimentos del repo):

| Régimen | Anticipación (lead time) | Lectura |
|---------|--------------------------|---------|
| Logístico (deriva suave) | alta | mejor margen preventivo |
| Oscilatorio | alta | detecta crecimiento de amplitud |
| Abrupto | baja | poco margen temporal intrínseco |

### Robustez frente a la calibración

El análisis de sensibilidad sobre combinaciones de pesos \((w_p,w_v,w_a)\) con suma 1 indica que el lead time **no colapsa** ante redistribuciones moderadas de la calibración canónica.
La calibración sigue siendo una elección del autor; la sensibilidad mide su influencia, no la elimina.

---

## 5. Limitaciones conocidas (Código Viajer)

1. Los benchmarks usan **trayectorias sintéticas** diseñadas para el estudio; no sustituyen validación sobre agentes reales.
2. La medición efectiva de \(L,S,I,B\) en un sistema vivo **no está resuelta dentro del validador**; debe proveerse desde fuera (`INTEGRATION.md`).
3. Pesos y umbrales son calibración inicial auditada por sensibilidad, no constantes universales.
4. En fallos abruptos el margen preventivo se reduce de forma estructural.
5. \(D_h\) no debe interpretarse automáticamente como geometría helicoidal diferencial completa.

---

## 6. Capa TRCG (en desarrollo)

Además del Código Viajer, el repositorio incluye módulos de la **Teoría Relacional Cuántico-Geométrica (TRCG)** / marco relacional asociado:

- geometría de símplex y conservación,
- cierres tipo MaxEnt,
- Jacobiano y umbrales espectrales de campos prototipo,
- torsión / proyectores (incluye líneas Helmholtz–Hodge),
- contornos tipo Suma 23.

**Estado:** mixto. Hay piezas operativas y conjeturales.
La clasificación viva está en [`STATUS.md`](./STATUS.md).

Principio de publicación:

- no se etiqueta como **Nivel I** lo que solo está verificado en un prototipo o numéricamente;
- toda promoción de nivel requiere sustento analítico, control de error y, cuando aplique, auditoría externa.

---

Historial de cambios: [`CHANGELOG.md`](./CHANGELOG.md)
```

## 7. Licencia y autoría

Distribuido bajo **Licencia MIT**. Ver [`LICENSE`](./LICENSE).

Proyecto del ecosistema conceptual y técnico de **Javier Viajer**.

- Web: https://musicalcodes.es
- Patreon: https://www.patreon.com/c/JavierViajer
- Repo: https://github.com/javier-viajer/codigo-viajer-spec

---

> El Código Viajer no sustituye auditorías, alineamiento ni controles de seguridad clásicos.
> Aporta una capa adicional de gobernanza preventiva basada en trayectoria, no solo en umbrales estáticos puntuales.
```

---

Relación con TRCG

Este repositorio contiene la especificación operativa de Código Viajer en cuatro dimensiones (4D), incluyendo el modelo de estado, la distancia dinámica y el validador.

El desarrollo matemático relacionado se mantiene en un repositorio independiente:

"TRCG Código Viajer Spec" (https://github.com/javier-viajer/trgc-codigo-viajer-spec)

TRCG contiene la investigación del núcleo de 24 dimensiones y la línea experimental de 47 dimensiones.

Ambos proyectos comparten una línea conceptual, pero sus modelos no deben considerarse transformaciones matemáticas equivalentes sin una demostración formal.

Consulta "REPOSITORY_RELATIONSHIP.md" (./REPOSITORY_RELATIONSHIP.md) para conocer la separación de responsabilidades y los criterios de integración. 




























