# Formalización Matemática del Modelo Pirámide-Parábola (TRCG)

Este documento unifica la arquitectura deductiva completa que demuestra cómo una red relacional homogénea abandona la planitud, clasifica sus estados mediante simetría de grupos finitos y converge hacia una estructura jerárquica piramidal gobernada por la envolvente parabólica y el invariante de la Suma 23.

---

## 1. Arquitectura Base y Grupo Finito de Automorfismos ($G$)

### 1.1 Resolución de la Compatibilidad Espacial-Modular
El sistema opera sobre una malla discreta de $N = 24$ nodos (Ley 24) acoplada a una base geométrica cuadrada con simetría rotacional $Z_4$ (giros de $90^\circ$). Para evitar conflictos entre la simetría espacial del cuadrado y la partición modular de 24 estados:
* El espacio nodal $V = \{v_1, \dots, v_{24}\}$ se particiona exactamente en **4 sectores simétricos** $V_k$ ($k \in \{0, 1, 2, 3\}$), correspondiendo cada sector a un cuadrante de la base con $\frac{24}{4} = 6$ nodos distribuidos sobre la envolvente parabólica.
* Cada rotación espacial de $90^\circ$ ($r^a$, $a \in \{0, 1, 2, 3\}$) se acopla biyectivamente a un desplazamiento modular de $6a$ posiciones ($\tau^{6a} \in Z_{24}$).

### 1.2 Estructura Algebraica del Grupo $G$
El conjunto de transformaciones admisibles $G = \{ (r^a, \tau^{6a}) \mid a \in \{0, 1, 2, 3\} \}$ constituye un **grupo finito de orden 4** ($|G| = 4$), isomorfo a $Z_4$, que cumple estrictamente los axiomas de grupo:
1. **Clausura:** $(r^{a_1}, \tau^{6a_1}) \circ (r^{a_2}, \tau^{6a_2}) = (r^{(a_1+a_2)\bmod 4}, \tau^{6(a_1+a_2)\bmod 24}) \in G$.
2. **Asociatividad:** Garantizada por la composición de operadores lineales sobre permutaciones finitas.
3. **Elemento Neutro:** $g_0 = (r^0, \tau^0)$.
4. **Elemento Inverso:** $g_a^{-1} = (r^{(4-a)\bmod 4}, \tau^{6(4-a)\bmod 24}) \in G$.

Al estar acotado topológicamente entre la base y el ápice de la pirámide, el grupo es estrictamente finito, habilitando su acción por permutaciones biyectivas sobre el espacio de configuraciones.

---

## 2. Combinatoria de Órbitas y Recuento mediante el Lema de Burnside

### 2.1 Espacio de Configuraciones ($X$)
Sea $S$ el conjunto finito de $q$ estados locales posibles por nodo ($|S| = q$). El espacio bruto de configuraciones globales es el conjunto de mapeos $X = \{x: V \to S\} = S^{24}$, con cardinalidad $|X| = q^{24}$. La acción de $g \in G$ sobre $x \in X$ se define por $(g \cdot x)(v_i) = x(g^{-1} \cdot v_i)$.

### 2.2 Subconjuntos de Puntos Fijos ($X^g$)
Para cada operador $g_a \in G$, la condición de invarianza $g_a \cdot x = x$ determina las siguientes cardinalidades:

| Operador ($g_a$) | Transformación Espacial / Modular | Condición de Invarianza sobre Sectores | Cardinalidad ($|X^{g_a}|$) |
| :--- | :--- | :--- | :--- |
| **$g_0$** | $0^\circ \quad (\Delta b = 0)$ | Sin restricción (identidad) | $q^{24}$ |
| **$g_1$** | $90^\circ \quad (\Delta b = 6)$ | $S_0 = S_1 = S_2 = S_3$ | $q^6$ |
| **$g_2$** | $180^\circ \quad (\Delta b = 12)$ | $S_0 = S_2$ y $S_1 = S_3$ | $q^{12}$ |
| **$g_3$** | $270^\circ \quad (\Delta b = 18)$ | $S_0 = S_1 = S_2 = S_3$ | $q^6$ |

### 2.3 Polinomio de Clases de Equivalencia ($|X/G|$)
Aplicando el Lema de Burnside:
$$|X/G| = \frac{1}{|G|} \sum_{g \in G} |X^g| = \frac{1}{4}\left(q^{24} + q^6 + q^{12} + q^6\right) = \frac{1}{4}q^{24} + \frac{1}{4}q^{12} + \frac{1}{2}q^6$$

Para el régimen binario fundamental ($q = 2$, $S = \{0, 1\}$):
$$|X/G| = \frac{2^{24}}{4} + \frac{2^{12}}{4} + \frac{2^6}{2} = 4,194,304 + 1,024 + 32 = \mathbf{4,195,360}$$

De las $4,195,360$ órbitas estructuralmente distintas, solo $32$ poseen simetría cuadrangular estricta ($90^\circ$) y $1,024$ poseen simetría diametral ($180^\circ$). El **$99.97\%$ del espacio cociente corresponde a configuraciones asimétricas**.

---

## 3. Análisis Espectral del Jacobiano y Ruptura de la Planitud

### 3.1 Espacio de Relaciones Independientes
Para una matriz de adyacencia o interacción relacional simétrica $R$ ($R_{ij} = R_{ji}$, sin autovínculos $R_{ii} = 0$) sobre $N = 24$ nodos, el número de grados de libertad independientes es exacto:
$$\dim(R) = \frac{N(N-1)}{2} = \frac{24 \times 23}{2} = \mathbf{276}$$

### 3.2 Operador de Evolución No Lineal $\Phi(R)$ mediante Hadamard
Dado que una matriz de proyección de rango 1 construida con el autovector unitario de Perron-Frobenius $\mathbf{v}(R)$ ($\|\mathbf{v}(R)\|_2 = 1$), $P(R) = \mathbf{v}(R)\mathbf{v}(R)^T$, es idempotente bajo el producto matricial estándar ($P^\gamma = P$), la concentración no lineal de masa relacional requiere aplicar el exponente $\gamma$ **componente a componente** (potencia de Hadamard, $\circ \gamma$), anulando la diagonal y normalizando la masa total:

$$\Phi(R) = (1 - \mu) R + \mu \, \mathcal{N}\Big( \big(\mathbf{v}(R)\mathbf{v}(R)^T\big)^{\circ \gamma}_{\text{off-diag}} \Big)$$

donde $\mu \in [0, 1]$ es la tasa de acoplamiento y $\mathcal{N}(M) = \frac{M}{\sum_{i \neq j} M_{ij}}$ garantiza la conservación de la masa relacional unitaria en cada iteración.

### 3.3 Punto Fijo Homogéneo ($R_\star$) y Derivación Analítica de $\gamma_c$
El estado de equilibrio homogéneo $R_\star$ (planitud isótropa $T_2$) se define por:
$$R_{\star, ij} = \begin{cases} c_0 & \text{si } i \neq j \\ 0 & \text{si } i = j \end{cases}, \qquad c_0 = \frac{1}{N(N-1)} = \frac{1}{552}$$

Su autovector dominante de Perron-Frobenius es uniforme: $v_{\star, i} = \frac{1}{\sqrt{N}}$. Al evaluar $\Phi(R_\star)$, los factores $N^{-\gamma}$ se cancelan en la normalización $\mathcal{N}(\cdot)$, verificando que $\Phi(R_\star) = R_\star$ para todo $(\mu, \gamma)$.

Introduciendo una perturbación simétrica infinitesimal $\delta R$ que conserve la traza ($\sum_{i \neq j} \delta R_{ij} = 0$, $\delta R_{ii} = 0$), la teoría de perturbaciones de primer orden sobre matrices simétricas arroja:
$$\delta \mathbf{v} = \frac{1}{\lambda_\star - \lambda_2} \delta R \, \mathbf{v}_\star = \frac{1}{N c_0} \delta R \, \mathbf{v}_\star$$

Expandiendo la potencia de Hadamard $(v_i v_j)^\gamma \approx v_\star^{2\gamma} + \gamma v_\star^{2\gamma - 1}(\delta v_i + \delta v_j)$ y aplicando la condición de ortogonalidad $\sum_{i=1}^N \delta v_i = 0$, el operador linealizado $J(R_\star)\delta R$ adopta la forma explícita:
$$\delta \Phi_{ij} = (1 - \mu)\delta R_{ij} + \frac{\mu \gamma}{N} \left( \sum_{k \neq i} \delta R_{ik} + \sum_{k \neq j} \delta R_{jk} \right)$$

El espacio de perturbaciones de 276 dimensiones se descompone en dos subespacios invariantes ortogonales:
1. **Subespacio transversal de grado nulo** ($\sum_{k \neq i} \delta R_{ik} = 0$, dimensión $\frac{N(N-3)}{2} = 252$):
   $$\Lambda_{\text{trans}} = 1 - \mu \implies |\Lambda_{\text{trans}}| < 1 \quad \forall \mu \in (0, 1)$$
2. **Subespacio longitudinal de gradiente nodal** ($\delta R_{ij} = \phi_i + \phi_j$ para $i \neq j$, con $\sum_{i=1}^N \phi_i = 0$, dimensión $N - 1 = 23$):
   Dado que $\sum_{k \neq i} (\phi_i + \phi_k) = (N - 2)\phi_i$, el autovalor exacto de este bloque de multiplicidad $23$ es:
   $$\Lambda_{\text{long}}(\gamma) = (1 - \mu) + \mu \gamma \left(\frac{N - 2}{N}\right)$$

Igualando $\Lambda_{\text{long}}(\gamma_c) = 1$ para determinar la pérdida de estabilidad lineal del plano $R_\star$:
$$(1 - \mu) + \mu \gamma_c \left(\frac{N - 2}{N}\right) = 1 \implies \mathbf{\gamma_c = \frac{N}{N - 2}}$$

* **Para $N = 24$ sin autovínculos ($\dim = 276$):** El umbral crítico deducido analíticamente es **$\gamma_c = \frac{24}{22} = \frac{12}{11} \approx 1.0909$**.
* **Caso con autovínculos ($\dim = 300$) o límite continuo ($N \to \infty$):** El factor $\frac{N-2}{N}$ se sustituye por $1$, recuperando $\gamma_c = 1$.

Para $\gamma > \gamma_c$, el modo longitudinal de multiplicidad $23$ se desestabiliza ($\Lambda_{\text{long}} > 1$), biseccionando la red en gradientes opuestos y expulsando al sistema hacia el dominio asimétrico ($99.97\%$) cuantificado por Burnside.

---

## 4. Sincronización Híbrida y Campo de Selección de la Suma 23

### 4.1 Acoplamiento de Fase y Salto en $k = 23$
El avance del índice modular $k(t) \in \mathbb{Z}_{24}$ se modela como proyección discreta de la fase continua acumulada $\theta(t)$ impulsada por el flujo relacional:
$$\frac{d\theta}{dt} = \alpha \|\dot{R}(t)\|_F, \qquad k(t) = \left\lfloor \frac{24}{2\pi} \big(\theta(t) \bmod 2\pi\big) \right\rfloor \pmod{24}$$

Al definirse la tensión informacional $\Omega(t) = \frac{\text{Tr}(R_{\text{apex}}(t))}{\text{Tr}(R_{\text{total}}(t))}$, el umbral crítico $\Omega_c$ queda fijado por la singularidad del Jacobiano del estrato ($\det(J_{\text{estrato}}) = 0$). En el instante $t_c$ en que $\Omega(t_c) = \Omega_c$, la fase acumulada completa $2\pi$, conduciendo el contador modular hasta $k = 23$ y disparando el operador de inyección isométrica helicoidal $I_H$ ($\|I_H(R)\|_F = \|R\|_F$).

### 4.2 Filtro Variacional $\Sigma_{23}$ y Fijación del Ápice
Para evitar que la expulsión hacia el espacio asimétrico derive en dispersión estocástica, el funcional escalar de la Suma 23 actúa como invariante de selección topológica sobre el espacio cociente $X/G$:
$$\Sigma_{23}([x]) = \sum_{i=1}^{24} w_i \, x(v_i) \equiv 23 \pmod{M}$$
donde los pesos $w_i$ están acoplados a la curvatura de la envolvente parabólica y a las conexiones del triángulo a la cruz. Este filtro restringe las $4,195,360$ clases de órbita a la variedad resonante $\mathcal{M}_{23}$, seleccionando el atractor cuyas coordenadas espaciales convergen al baricentro del ápice:
$$\mathbf{r}_{\text{apex}} = \lim_{t \to \infty} \frac{\sum_{i=1}^{24} R_{i,\text{apex}}(t)\,\mathbf{r}_i}{\sum_{i=1}^{24} R_{i,\text{apex}}(t)} = (0, 0, z_{\text{apex}})$$

---

## 5. Síntesis y Estatus Epistemológico

1. **Nivel I (Demostrado Analíticamente):** La compatibilidad entre el grupo finito $G \cong Z_4$ y los $24$ nodos, la dimensión $276$, el polinomio exacto de Burnside ($4,195,360$ órbitas para $q=2$), la formulación mediante producto de Hadamard y la deducción exacta del umbral de bifurcación $\gamma_c = \frac{12}{11}$ en $R_\star$.
2. **Nivel II (Formulación Dinámica en Verificación Numérica):** La parametrización explícita de la constante de fase $\alpha$ para el cierre de ciclo en $k=23$ y la tabla cerrada de pesos $w_i$ del funcional $\Sigma_{23}$ para la selección única de órbita.
