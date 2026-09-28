``
prompttemplate.md — AI Agent Automated Reading Instruction / Instrucción de Lectura Automatizada para Agentes de IA

> EN — Copy the appropriate block below and paste it as-is into ChatGPT, Claude, Gemini,
> DeepSeek or any other LLM with internet access. The agent will read the
> entire repository and return a structured report in your language.
>
> ES — Copia el bloque adecuado de abajo y pégalo tal cual en ChatGPT, Claude, Gemini,
> DeepSeek o cualquier otro LLM con acceso a internet. El agente leerá el
> repositorio entero y te devolverá un informe estructurado en tu idioma.

English version

`
You are an AI governance systems auditor. Your task is to read, understand, and
evaluate the public repository:

  https://github.com/javier-viajer/codigo-viajer-spec

Files you must read (11 total)
README.md — theoretical grounding, formal architecture, Dh metric
validator.py — dynamic validator implementation in ℝ⁴
benchmarkstochastic.py — Monte Carlo simulation (1000 iterations, lead time, false positives)
benchmarkregimes.py — three failure regimes: logistic, oscillatory, abrupt
sensitivityanalysis.py — hyperparameter sweep
generatereport.py — self-contained console report
testvalidator.py — unit tests (pytest, 15+ tests, invariants, trajectories, dynamic vs static comparison)
CASESTUDY.md — canonical trajectory table (36 steps)
CONSTITUCIONUNITARIA.md — 36 constitutional articles derived from the model
INTEGRATION.md — real-world signal integration protocol
LICENSE — MIT license

For code files (.py), read the full source code from raw URLs
(raw.githubusercontent.com/javier-viajer/codigo-viajer-spec/main/...).
For .md files, read their complete contents.

What you must deliver

Write a report in English with the following sections:

Executive Summary
In 5-7 lines: what the project is, what problem it solves, how it solves it.

Technical Architecture
• Explain the ℝ⁴ state space (L, S, I, B) and the attractor E
• Explain the helicoidal distance metric Dh and its decomposition (position, velocity, acceleration)
• Explain the hard constitutional invariants and helicoidal thresholds
• Explain the ALLOW / THROTTLE / REJECT triage
• Compare CodigoViajerValidator with StaticValidator

Empirical Validation
• Summarise the stochastic benchmark results (mean lead time, deviation, false positive rate)
• Summarise the multi-regime benchmark results (logistic, oscillatory, abrupt)
• Summarise the sensitivity analysis: is the dynamic advantage robust to hyperparameter changes?
• Summarise the testvalidator.py unit tests: which behaviours do they verify and with what coverage?

Applicability
• Describe the Los Angeles earthquake use case (INTEGRATION.md)
• Assess the viability of integrating this validator as a governance layer (Layer-0) in autonomous AI systems
• Identify which types of agents would benefit most from this system

Conceptual Dimension
• Summarise CONSTITUCIONUNITARIA.md and its relationship to the mathematical model
• Explain how the concepts Matrix 22+12, Sum 23, Código Viajer and Law 24 translate into algorithmic governance mechanisms

Final Verdict
• Project strengths
• Limitations or risks
• Recommendations for adoption or future development
• Is it viable as a preventive governance system for autonomous agents?

Be rigorous. Read every file before forming an opinion. If any file is unavailable,
state so and continue with the rest.
`

Versión en español

`
Eres un auditor de sistemas de gobernanza para inteligencia artificial. Tu tarea
es leer, comprender y evaluar el repositorio público:

  https://github.com/javier-viajer/codigo-viajer-spec

Archivos que debes leer (11 en total)
README.md — fundamentación teórica, arquitectura formal, métrica Dh
validator.py — implementación del validador dinámico en ℝ⁴
benchmarkstochastic.py — Monte Carlo (1000 iteraciones, lead time, falsos positivos)
benchmarkregimes.py — tres regímenes de fallo: logístico, oscilatorio, abrupto
sensitivityanalysis.py — barrido de hiperparámetros
generatereport.py — informe de consola autocontenido
testvalidator.py — tests unitarios (pytest, 15+ tests, invariantes, trayectorias y comparación dinámico vs estático)
CASESTUDY.md — tabla canónica de trayectoria (36 pasos)
CONSTITUCIONUNITARIA.md — 36 artículos constitucionales derivados del modelo
INTEGRATION.md — protocolo de integración con señales del mundo real
LICENSE — licencia MIT

Para los archivos de código (.py), lee el código fuente completo desde las URLs
raw (raw.githubusercontent.com/javier-viajer/codigo-viajer-spec/main/...).
Para los archivos .md, lee su contenido íntegro.

Lo que debes entregar

Redacta un informe en español con las siguientes secciones:

Resumen Ejecutivo
En 5-7 líneas: qué es el proyecto, qué problema resuelve, cómo lo resuelve.

Arquitectura Técnica
• Explica el espacio de estados ℝ⁴ (L, S, I, B) y el atractor E
• Explica la métrica de distancia helicoidal Dh y su descomposición (posición, velocidad, aceleración)
• Explica los invariantes constitucionales duros y los umbrales helicoidales
• Explica el triaje ALLOW / THROTTLE / REJECT
• Compara el CodigoViajerValidator con el StaticValidator

Validación Empírica
• Resume los resultados del benchmark estocástico (lead time medio, desviación, tasa de falsos positivos)
• Resume los resultados del benchmark multi-régimen (logístico, oscilatorio, abrupto)
• Resume el análsis de sensibilidad: ¿la ventaja dinámica es robusta frente a cambios en los hiperparámetros?
• Resume los tests unitarios de testvalidator.py: ¿qué comportamientos verifica y con qué cobertura?

Aplicabilidad
• Describe el caso de uso del terremoto en Los Ángeles (INTEGRATION.md)
• Evalúa la viabilidad de integrar este validador como capa de gobernanza (Layer-0) en sistemas de IA autónomos
• Identifica qué tipos de agentes se beneficiarían más de este sistema

Dimensión Conceptual
• Resume la CONSTITUCIONUNITARIA.md y su relación con el modelo matemático
• Explica cómo los conceptos Matriz 22+12, Suma 23, Código Viajer y Ley 24 se traducen a mecanismos de gobernanza algorítmica

Veredicto Final
• Fortalezas del proyecto
• Limitaciones o riesgos
• Recomendaciones para adopción o desarrollo futuro
• ¿Es viable como sistema de gobernanza preventiva para agentes autónomos?

Sé riguroso. Lee cada archivo antes de opinar. Si algún archivo no está disponible,
indícalo y continúa con los demás.
`

Usage notes / Notas de uso
• EN — This prompt assumes the LLM has internet access and can read GitHub raw URLs. If the LLM cannot access GitHub directly, provide the files as attachments or as copied text. The resulting report serves as an entry point for anyone — technical or not — to understand the project in under 10 minutes. If you are a developer and want to integrate the validator into your own system, consult INTEGRATION.md and validator.py directly.
• ES — Este prompt asume que el LLM tiene acceso a internet y puede leer URLs raw de GitHub. Si el LLM no puede acceder a GitHub directamente, proporciónale los archivos como adjuntos o como texto copiado. El informe resultante sirve como puerta de entrada para que cualquier persona —técnica o no— entienda el proyecto en menos de 10 minutos. Si eres desarrollador y quieres integrar el validador en tu propio sistema, consulta INTEGRATION.md y validator.py directamente.







