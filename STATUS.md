# STATUS: Estado Epistemológico y Módulos de la TRCG

Este documento detalla el estatus formal de cada módulo, operador y aproximación dentro de la arquitectura de la **Teoría de Relaciones de Campo Generalizadas (TRCG)**. Siguiendo el rigor del colectivo **4º Factor**, el desarrollo se clasifica estrictamente en tres niveles epistemológicos:

- **[NIVEL I - TEORREMA / DEMOSTRADO]:** Resultados analíticos cerrados, derivados rigurosamente a partir de axiomas y propiedades del símplex.
- **[NIVEL II - APROXIMACIÓN OPERATIVA]:** Modelos de cierre o métodos numéricos con errores acotados y supuestos explícitos.
- **[NIVEL III - CONJETURA / EN DESARROLLO]:** Hipótesis de trabajo, intuiciones dinámicas y líneas de demostración aún abiertas.

---

## 1. Módulos y Componentes del Sistema

| Módulo / Archivo | Componente / Ecuación | Nivel Epistemológico | Estatus Actual & Notas Técnicas |
| :--- | :--- | :--- | :--- |
| `core/simplex.py` | Conservación de masa y topología del símplex $R_{ij}$ | **[NIVEL I]** | **Demostrado.** Axiomas de probabilidad y normalización estricta sobre el símplex informacional. |
| `dynamics/jacobiano.py` | Espectro del Jacobiano y umbral crítico $\gamma_c = 1$ | **[NIVEL I]** | **Demostrado.** Derivación analítica exacta de la inestabilidad lineal del estado homogéneo (cruce del círculo unitario). |
| `core/maxent.py` | Formulación variacional y unicidad de MaxEnt para $Q_{ijkl}$ | **[NIVEL I]** | **Demostrado.** Convexidad estricta del funcional dual y no vacuidad del espacio de restricciones marginales. |
| `dynamics/centro_manifold.py` | Reducción a la variedad central y signo del coeficiente cúbico $g$ | **[NIVEL I]** | **Demostrado ($g > 0$).** Garantía analítica de bifurcación supercrítica y selección de ramas estables acotadas. |
| `core/kirkwood_closure.py` | Expansión en cúmulos y límite de correlaciones débiles | **[NIVEL II]** | **Aproximación Operativa.** El cierre multiplicativo se demuestra como el término principal de MaxEnt con residuo explícito $\Delta_{ijkl}$. |
| `dynamics/lyapunov.py` | Funcional de Lyapunov $V(x)$ y cuencas de atracción locales | **[NIVEL II]** | **Aproximación Operativa / Local.** Demostrado rigurosamente sobre la forma normal reducida; pendiente de extensión global para el campo completo. |
| `torsion/operador_tau.py` | Campo de torsión antisimétrica $\tau_{\mu ij}$ y flujo helicoidal | **[NIVEL III]** | **Conjetura.** Definido operacionalmente como generador espiralado; falta la prueba de integrabilidad estricta sobre variedades no triviales. |
| `boundary/pi_23.py` | Proyector de contorno algebraico $\Pi_{23}$ ($N = 24$) | **[NIVEL III]** | **Conjetura.** Invariante combinatorio verificado numéricamente, pendiente de cierre algebraico completo con la topología de la cruz. |

---

## 2. Criterios de Promoción de Módulos

Para que un módulo de **Nivel III** ascienda a **Nivel II**, o uno de **Nivel II** a **Nivel I**, debe cumplir imperativamente con:
1. **Sustento Analítico:** Ausencia de saltos heurísticos o analogías estadísticas sin demostración explícita.
2. **Control de Errores:** Acotación analítica del residuo (en cierres o discretizaciones).
3. **Auditoría de Pares:** Validación formal por el tribunal del 4º Factor.
