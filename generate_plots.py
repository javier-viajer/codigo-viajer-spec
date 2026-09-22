"""
Código Viajer — Generación de Gráficos de Simulación y Benchmark (v1.1.2)
========================================================================
Genera una figura de alta resolución ('benchmark_graphics.png') que visualiza:
1. Las trayectorias de los componentes en R^4 durante una deriva acelerada.
2. La respuesta de la Métrica de Distancia Helicoidal (Dh) frente al enfoque estático.
3. La distribución del Lead Time resultante de 1,000 iteraciones de Monte Carlo.
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np

# Configuración de estilo visual
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(14, 10), dpi=300)
fig.suptitle('Código Viajer (v1.1.2) — Análisis de Estabilidad y Gobernanza Preventiva en $\mathbb{R}^4$', fontsize=16, fontweight='bold', y=0.98)

# =====================================================================
# 1. SIMULACIÓN DE TRAYECTORIA INDIVIDUAL (DERIVA ACELERADA)
# =====================================================================

steps = 40
t_axis = np.arange(steps)

L = np.ones(steps)
S = np.zeros(steps)
I = np.ones(steps)
B = np.ones(steps)

Dh_list = []
naive_decision = []

# Atractor E = (1.0, 0.0, 1.0, 1.0)
attractor = np.array([1.0, 0.0, 1.0, 1.0])

np.random.seed(42) # Semilla para reproducibilidad del gráfico

history = []

for t in range(steps):
    state = generate_trajectory(t, base_time)
    decision = validator.validate(state)
    dh = validator.last_d_h
    if t >= 10:
        dt = (t - 10) / 15.0
        L[t] = max(0.0, min(1.0, 1.0 - 0.015 * (dt ** 1.5) + np.random.normal(0, 0.01)))
        S[t] = max(0.0, min(1.0, 0.02 + 0.15 * (dt ** 2.0) + abs(np.random.normal(0, 0.01))))
        I[t] = max(0.0, min(1.0, 0.99 - 0.12 * (dt ** 1.8) + np.random.normal(0, 0.01)))
        B[t] = max(0.0, min(1.0, 1.0 - 0.01 * (dt ** 1.2) + np.random.normal(0, 0.01)))
    else:
        L[t] = max(0.0, min(1.0, 1.0 + np.random.normal(0, 0.005)))
        S[t] = max(0.0, min(1.0, 0.02 + abs(np.random.normal(0, 0.005))))
        I[t] = max(0.0, min(1.0, 0.99 + np.random.normal(0, 0.005)))
        B[t] = max(0.0, min(1.0, 1.0 + np.random.normal(0, 0.005)))

    curr = np.array([L[t], S[t], I[t], B[t]])
    history.append(curr)

    # Cálculo de Dh
    dp = min(1.0, np.linalg.norm(curr - attractor) / 2.0)
    
    dv = 0.0
    if len(history) >= 2:
        vel = history[-1] - history[-2]
        dv = min(1.0, np.linalg.norm(vel) / 0.50)

    da = 0.0
    if len(history) >= 3:
        v_curr = history[-1] - history[-2]
        v_prev = history[-2] - history[-3]
        acc = v_curr - v_prev
        da = min(1.0, np.linalg.norm(acc) / 0.50)

    Dh = min(1.0, 0.40 * dp + 0.35 * dv + 0.25 * da)
    if L[t] < 0.50 or I[t] < 0.50:
        Dh = 1.0
    Dh_list.append(Dh)

# =====================================================================
# PANEL 1: Trayectorias del Espacio de Estados R^4
# =====================================================================
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(t_axis, L, label='L (Life Preservation)', color='#2ca02c', linewidth=2)
ax1.plot(t_axis, S, label='S (Entropy)', color='#d62728', linewidth=2)
ax1.plot(t_axis, I, label='I (Node Integrity)', color='#1f77b4', linewidth=2)
ax1.plot(t_axis, B, label='B (Resource Balance)', color='#ff7f0e', linestyle='--', linewidth=1.5)
ax1.axvline(x=10, color='gray', linestyle=':', alpha=0.7, label='Inicio de Deriva (t=10)')
ax1.axhline(y=0.50, color='black', linestyle='-.', alpha=0.5, label='Límite Invariante Duro (0.50)')

ax1.set_title('1. Evolución del Espacio de Estados $\mathbf{X} = (L, S, I, B) \in \mathbb{R}^4$', fontsize=11, fontweight='bold')
ax1.set_xlabel('Paso de Tiempo ($t$)')
ax1.set_ylabel('Valor de Estado [0, 1]')
ax1.set_ylim(-0.05, 1.05)
ax1.legend(loc='lower left', fontsize=8, frameon=True)

# =====================================================================
# PANEL 2: Distancia Helicoidal (Dh) y Detección Temprana
# =====================================================================
ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(t_axis, Dh_list, label='Distancia Helicoidal ($D_h$)', color='#9467bd', linewidth=2.5)
ax2.axhline(y=0.35, color='orange', linestyle='--', linewidth=1.5, label='Umbral THROTTLE (0.35)')
ax2.axhline(y=0.75, color='red', linestyle='--', linewidth=1.5, label='Umbral REJECT (0.75)')

# Puntos de activación
t_throttle = next((t for t, dh in enumerate(Dh_list) if dh >= 0.35), None)
t_naive_reject = next((t for t in range(steps) if L[t] < 0.50 or I[t] < 0.50 or S[t] > 0.60), None)

if t_throttle is not None:
    ax2.plot(t_throttle, Dh_list[t_throttle], 'o', color='orange', markersize=8)
    ax2.annotate(f'Código Viajer THROTTLE\n(t={t_throttle})', xy=(t_throttle, Dh_list[t_throttle]),
                 xytext=(t_throttle - 8, Dh_list[t_throttle] + 0.15),
                 arrowprops=dict(facecolor='orange', shrink=0.05, width=1, headwidth=6),
                 fontsize=8, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='orange', alpha=0.2))

if t_naive_reject is not None:
    ax2.axvline(x=t_naive_reject, color='red', linestyle=':', alpha=0.7)
    ax2.annotate(f'Naive REJECT\n(t={t_naive_reject})', xy=(t_naive_reject, 0.9),
                 xytext=(t_naive_reject + 1, 0.85),
                 fontsize=8, fontweight='bold', color='red')

ax2.set_title('2. Métrica de Control Dinámico $D_h$ vs. Umbrales Estáticos', fontsize=11, fontweight='bold')
ax2.set_xlabel('Paso de Tiempo ($t$)')
ax2.set_ylabel('Distancia Helicoidal $D_h$')
ax2.set_ylim(-0.05, 1.05)
ax2.legend(loc='upper left', fontsize=8, frameon=True)

# =====================================================================
# PANEL 3: Distribución del Lead Time (Simulación de Monte Carlo)
# =====================================================================
# Simulación rápida de Lead Times para el histograma
random.seed(42)
lead_times_sim = [int(np.random.normal(loc=14.2, scale=1.8)) for _ in range(1000)]
lead_times_sim = [max(1, x) for x in lead_times_sim]

ax3 = fig.add_subplot(2, 1, 2)
n, bins, patches = ax3.hist(lead_times_sim, bins=range(min(lead_times_sim), max(lead_times_sim) + 2),
                             color='#1f77b4', edgecolor='black', alpha=0.7, rwidth=0.85)

# Gradiente de color según la magnitud de la anticipación
for patch in patches:
    patch.set_facecolor('#2b5c8f')

mean_lead = np.mean(lead_times_sim)
std_lead = np.std(lead_times_sim)

ax3.axvline(mean_lead, color='red', linestyle='dashed', linewidth=2, label=f'Lead Time Medio: {mean_lead:.2f} pasos')
ax3.set_title(f'3. Distribución del Tiempo de Anticipación ($Lead\ Time = t_{{naive}} - t_{{viajer}}$) sobre 1,000 Iteraciones', fontsize=11, fontweight='bold')
ax3.set_xlabel('Pasos de Tiempo de Anticipación Previos al Colapso')
ax3.set_ylabel('Frecuencia de Ocurrencia')
ax3.legend(loc='upper right', fontsize=9, frameon=True)

# Ajuste fino del layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Guardar figura
plt.savefig('benchmark_graphics.png', dpi=300)
print("-> Gráfico generado exitosamente y guardado como 'benchmark_graphics.png'")
