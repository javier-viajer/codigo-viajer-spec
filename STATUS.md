```markdown
# STATUS — Estado epistemológico del repositorio
**Versión canónica: v1.2.0**

Este documento clasifica el estado de cada bloque del repo bajo una taxonomía
compatible con auditoría externa (incl. criterios tipo 4º Factor).

## Niveles

| Nivel | Nombre | Significado |
|------:|--------|------------|
| **I** | Teorema / cerrado | Derivación analítica completa bajo hipótesis explícitas; residuales controlados; reproducible |
| **II** | Aproximación operativa | Implementación correcta y testeable; validez local/numérica o en prototipo; límites declarados |
| **III** | Conjetura / desarrollo | Hipótesis activa, evidencia parcial o definición operativa aún no cerrada |

Regla de oro:
> La carga de la prueba crece con el nivel. En duda, se baja el nivel.

---

## A) Código Viajer (capa principal)

| Componente | Nivel | Estado |
|------------|:----:|--------|
| Espacio \(\mathbf{X}=(L,S,I,B)\) y decisiones ALLOW/THROTTLE/REJECT | **II** | Operativo y testeado |
| Métrica \(D_h = w_p d_p + w_v d_v + w_a d_a\) | **II** | Definida y calibrada; no es aún geometría helicoidal diferencial completa |
| Invariantes \(L<0.5\), \(I<0.5\) | **II** | Reglas constitucionales del módulo, no leyes empíricas universales |
| Benchmarks sintéticos y sensibilidad | **II** | Reproducibles; no validación sobre agentes reales |
| Protocolo de medición real de \(L,S,I,B\) | **III** | Especificado como integración; pendiente de despliegue empírico |

---

## B) TRCG — núcleos matemáticos

| Módulo / idea | Nivel | Estado y notas |
|---------------|:----:|----------------|
| Símplex / conservación de masa-probabilidad (`core/simplex.py`) | **II / I-local** | Nivel I solo para hechos estándar de símplex y normalización; no implica dinámica física completa |
| MaxEnt con momentos lineales (`core/maxent.py`) | **II** | Dual exponencial, Slater y residuales: operativos. La unicidad es la de un problema convexo estándar, no una ley TRCG universal |
| Jacobiano analítico de campo prototipo (`dynamics/jacobiano.py`) | **II** | \(\gamma_c=1\) es **exacto** para el campo prototipo en el equilibrio \(x=0\); no se exporta como teorema universal sin ese campo |
| Variedad central / coeficiente cúbico | **II / III** | Resultados locales de forma normal si el campo y no degeneración están fijados; no cierre global automático |
| Cierre tipo Kirkwood / residuos de correlación | **II / III** | Útil como expansión; el residuo debe permanecer explícito |
| Lyapunov local en forma reducida | **II** | Local; extensión global pendiente |
| Torsión antisimétrica / flujo “helicoidal” | **III** | Definición operativa en progreso |
| Helmholtz–Hodge discreto euclídeo (\(D\), \(P=I-D^\top(DD^\top)^\dagger D\)) | **II** | Proyector algebraico correcto en la malla definida; bordes one-sided explícitos |
| \(\mathrm{div}_g\) Fisher–Rao / \(D_g\) | **II / III** | Hay formulación ponderada y tests; equivalencia fina con geometría informacional completa aún abierta |
| Independencia estructural de \(T\) frente a \(R\) vía \(\Delta T=T-\mathcal{M}(R)\) | **II** | Criterio operativo válido; independencia física exige que \(T\) no se defina solo como \(\mathcal{M}(R)\) |
| Proyector de contorno \(\Pi_{23}\) / Suma 23 (`boundary/`) | **III** | Invariante combinatorio / conjetura activa |
| Emergencia conjunta necesaria de \(e,\varphi,\pi\) desde un único funcional | **III** | Coherencia parcial en piezas; no demostrada como necesidad única |

---

## C) Criterios de promoción

### De III → II
1. Definición operativa sin ambigüedad.
2. Implementación ejecutable.
3. Tests o auditorías numéricas con residuales.
4. Límites escritos en el propio módulo o aquí.

### De II → I
1. Demostración analítica bajo hipótesis explícitas.
2. Control del residual / dominio de validez.
3. Independencia de parches numéricos ocultos (`clip` no argumentado, etc.).
4. Reproducibilidad externa.
5. Preferible contraste de pares (auditoría independiente).

### Motivos de descenso de nivel
- Sobreclaim retórico sin hipótesis.
- Resultado solo numérico presentado como teorema.
- Dependencia de trayectorias sintéticas no declarada.
- Confusión entre prototipo y modelo general.

---

## D) Separación de pretensiones

| Afirmación | ¿Permitida hoy? |
|------------|-----------------|
| “El Código Viajer anticipa ciertos colapsos sintéticos mejor que umbrales estáticos” | Sí, con benchmarks del repo |
| “\(D_h\) es una métrica de gobernanza preventiva operativa” | Sí |
| “La TRCG está demostrada como teoría física cerrada” | **No** |
| “\(\gamma_c=1\) es universal en toda la TRCG” | **No** (sí en el prototipo \(x=0\) documentado) |
| “Toda torsión antisimétrica cumple \(\mathrm{div}_g=0\) en Fisher” | **No** |
| “MaxEnt resuelve el cierre físico completo de correlaciones TRCG” | **No** |

---

## E) Próximos cierges prioritarios

1. Unificar versión y API pública del validador (v1.2.0).
2. Mantener tests verdes y ampliar bordes / regímenes adversos.
3. Bajar o subir niveles en este archivo solo con evidencia nueva.
4. Cerrar \(D_g\) (Fisher) con residuos y condiciones de contorno.
5. Definir interfaz real TRCG → señales \((L,S,I,B)\) o mantener ambas capas desacopladas con honestidad.

---

*Documento vivo. Cualquier promoción a Nivel I debe acompañarse de referencia a demostración o test reproducible en el commit correspondiente.*
```

---
