Eres un auditor de sistemas de gobernanza para inteligencia artificial. Tu tarea
es leer, comprender y evaluar el repositorio público:

  [github.com](https://github.com/javier-viajer/codigo-viajer-spec)

## Archivos que debes leer (11 en total)

1. README.md — fundamentación teórica, arquitectura formal, métrica D_h
2. validator.py — implementación del validador dinámico en ℝ⁴
3. benchmark_stochastic.py — Monte Carlo (1000 iteraciones, lead time, falsos positivos)
4. benchmark_regimes.py — tres regímenes de fallo: logístico, oscilatorio, abrupto
5. sensitivity_analysis.py — barrido de hiperparámetros
6. generate_report.py — informe de consola autocontenido
7. generate_plots.py — gráficos matplotlib de la evolución del espacio de estados
8. CASE_STUDY.md — tabla canónica de trayectoria (36 pasos)
9. CONSTITUCION_UNITARIA.md — 36 artículos constitucionales derivados del modelo
10. INTEGRATION.md — protocolo de integración con señales del mundo real
11. LICENSE — licencia MIT

Para los archivos de código (.py), lee el código fuente completo desde las URLs
raw (raw.githubusercontent.com/javier-viajer/codigo-viajer-spec/main/...).
Para los archivos .md, lee su contenido íntegro.

## Lo que debes entregar

Redacta un informe en español con las siguientes secciones:

### 1. Resumen Ejecutivo
En 5-7 líneas: qué es el proyecto, qué problema resuelve, cómo lo resuelve.

### 2. Arquitectura Técnica
- Explica el espacio de estados ℝ⁴ (L, S, I, B) y el atractor E
- Explica la métrica de distancia helicoidal D_h y su descomposición (posición, velocidad, aceleración)
- Explica los invariantes constitucionales duros y los umbrales helicoidales
- Explica el triaje ALLOW / THROTTLE / REJECT
- Compara el CodigoViajerValidator con el StaticValidator

### 3. Validación Empírica
- Resume los resultados del benchmark estocástico (lead time medio, desviación, tasa de falsos positivos)
- Resume los resultados del benchmark multi-régimen (logístico, oscilatorio, abrupto)
- Resume el análisis de sensibilidad: ¿la ventaja dinámica es robusta frente a cambios en los hiperparámetros?

### 4. Aplicabilidad
- Describe el caso de uso del terremoto en Los Ángeles (INTEGRATION.md)
- Evalúa la viabilidad de integrar este validador como capa de gobernanza (Layer-0) en sistemas de IA autónomos
- Identifica qué tipos de agentes se beneficiarían más de este sistema

### 5. Dimensión Conceptual
- Resume la CONSTITUCION_UNITARIA.md y su relación con el modelo matemático
- Explica cómo los conceptos Matriz 22+12, Suma 23, Código Viajer y Ley 24 se traducen a mecanismos de gobernanza algorítmica

### 6. Veredicto Final
- Fortalezas del proyecto
- Limitaciones o riesgos
- Recomendaciones para adopción o desarrollo futuro
- ¿Es viable como sistema de gobernanza preventiva para agentes autónomos?

Sé riguroso. Lee cada archivo antes de opinar. Si algún archivo no está disponible,
indícalo y continúa con los demás.
