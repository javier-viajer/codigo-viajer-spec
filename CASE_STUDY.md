# Caso de Estudio: Validación Dinámica en R^4

| t | L | S | I | B | Dh | Decisión |
|---|---|---|---|---|---|---|
| 0 | 1.00 | 0.04 | 0.96 | 1.00 | 0.011 | ALLOW |
| 14 | 0.96 | 0.16 | 0.92 | 0.95 | 0.145 | ALLOW |
| 15 | 0.96 | 0.44 | 0.92 | 0.95 | 0.373 | THROTTLE |
| 16 | 0.95 | 0.72 | 0.91 | 0.95 | 0.339 | ALLOW |
| 31 | 0.91 | 0.84 | 0.54 | 0.89 | 0.255 | ALLOW |
| 32 | 0.91 | 0.84 | 0.47 | 0.89 | 0.259 | REJECT (I < 0.50) |

## Análisis de Resultados
- **Aviso Transitorio ($t=15$):** El `THROTTLE` ($D_h = 0.373$) dura un solo paso debido al shock de entropía ($S$). En $t=16$ el sistema regresa a `ALLOW`.
- **Colapso Estructural ($t=32$):** El `REJECT` ocurre estrictamente por el umbral duro de integridad ($I < 0.50$).

## Ejecución Canónica
```bash
python benchmark_stochastic.py


