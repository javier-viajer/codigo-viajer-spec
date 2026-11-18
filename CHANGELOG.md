```markdown
# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
El versionado sigue [SemVer](https://semver.org/lang/es/) en la medida de lo posible.

## [1.2.0] — 2026-11-18

### Añadido
- `STATUS.md` como taxonomía epistemológica viva (Niveles I / II / III).
- Separación explícita en documentación entre **Código Viajer** (capa operativa) y **TRCG** (marco en desarrollo).
- Criterios de promoción y descenso de nivel para módulos TRCG.
- Tabla de pretensiones permitidas / no permitidas para evitar sobreclaim.

### Cambiado
- README reescrito: sin secciones duplicadas, versión canónica única **v1.2.0**.
- La métrica \(D_h\) se describe como **distancia dinámica ponderada** (posición, velocidad, aceleración); el término “helicoidal” queda como etiqueta histórica, no como teorema geométrico.
- Recalibración de niveles TRCG:
  - MaxEnt, Jacobiano de prototipo, Helmholtz euclídeo discreto → **Nivel II** (salvo hechos locales estándar).
  - Torsión Fisher completa, \(\Pi_{23}\), emergencia necesaria \(e,\varphi,\pi\) → **Nivel III** o mixto según módulo.
- Limitaciones del Código Viajer agrupadas y visibilizadas (trayectorias sintéticas, sensores externos, fallos abruptos).

### Corregido
- Inconsistencias de versionado entre README, validador e informes.
- Afirmaciones de “Nivel I / demostrado” sin hipótesis explícitas ni dominio de validez.

### Seguridad / gobernanza documental
- Principio de publicación: no etiquetar como teorema lo solo numérico o prototípico.

---

## [1.1.x] — 2026-09

### Resumen de la línea 1.1
- `CodigoViajerValidator` y `StaticValidator`.
- Benchmarks estocásticos y multi-régimen.
- Análisis de sensibilidad de pesos y umbrales.
- Tests unitarios del validador.
- Informes de trayectoria y lead time.
- Documentos `CASE_STUDY.md`, `INTEGRATION.md`, borradores constitucionales.

> Las subversiones 1.1.2 / 1.1.3 / 1.1.6 quedaron unificadas documentalmente en **1.2.0**.

---

## [1.0.0] — 2026-09

### Añadido
- Especificación inicial Layer-0 / Código Viajer.
- Matriz de restricciones y filtro de trayectoria en \(\mathbb{R}^4\).
- Publicación abierta del repositorio base.

---

## Tipos de cambios
- **Añadido** — funcionalidad o documentación nueva.
- **Cambiado** — cambios en comportamiento o criterio.
- **Corregido** — bugs o inconsistencias.
- **Deprecado** — aún disponible, pero en retirada.
- **Eliminado** — removido del árbol público.
- **Seguridad** — parches de seguridad o de gobernanza documental crítica.
```
