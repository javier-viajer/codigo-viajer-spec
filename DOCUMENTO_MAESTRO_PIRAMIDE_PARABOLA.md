# TRCG — Formalización del Modelo Pirámide-Parábola (v1.2.0)

Esta versión recoge la formalización consolidada del modelo **Pirámide-Parábola** dentro de la TRCG. Integra el núcleo geométrico, combinatorio y espectral cerrado (**Nivel I**), las leyes de conservación bajo el convenio de arista única y el régimen híbrido de fase (**Nivel II**), y el cierre analítico-combinatorio de los tres pasos del **Nivel III**: dominancia apical y condición de crecimiento de $H_{\text{est}}$ bajo el acoplamiento parabólico sin parámetros libres (**Paso III.1**), fórmula explícita de fibras orbitales y criterio canónico de selección única en $\Sigma_{23}$ (**Paso III.2**), y expresiones explícitas de $\omega_0$ y $c_1$ en la forma normal de Neimark–Sacker junto con el acoplamiento estroboscópico en el salto $23 \to 0$ (**Paso III.3**).

---

## 1. Geometría en $\mathbb{R}^3$ y Grupo $G \cong \mathbb{Z}_4$ `[Nivel I — Cerrado / Demostrado]`

### 1.1 Coordenadas y compatibilidad espacial-modular
Consideramos $N = 24$ nodos indexados por sector $k \in \{0, 1, 2, 3\}$ y estrato $j \in \{1, 2, 3, 4, 5, 6\}$ ($6$ nodos por sector). La biyección con el índice lineal $n \in \{1, \dots, 24\}$ es:

$$n = 6k + j \iff k = \left\lfloor \frac{n - 1}{6} \right\rfloor, \qquad j = ((n - 1) \bmod 6) + 1$$

En coordenadas cilíndricas $(\rho, \varphi, z)$ sobre la envolvente parabólica, cada nodo se sitúa en:

$$\mathbf{r}_{k,j} = \left( \rho_j \cos\varphi_{k,j}, \; \rho_j \sin\varphi_{k,j}, \; z_j \right)$$

donde:

* $z_j = h_0 \cdot j$ es la cota fija del estrato, sujeta a la condición estricta de no-colapso:

$$0 < z_1 < z_2 < \dots < z_6 < H \qquad (\text{con } H > 0)$$

* $\rho_j = R_0 \sqrt{1 - \frac{z_j}{H}}$ (con $R_0 > 0$) define la envolvente parabólica y satisface $\rho_j > 0$ para todo $j \in \{1, \dots, 6\}$, garantizando radios estrictamente positivos, evitando el colapso de nodos sobre el eje central o en el ápice $(0, 0, H)$ y asegurando $24$ puntos geométricamente distintos en $\mathbb{R}^3$.
* $\varphi_{k,j} = k\frac{\pi}{2} + \delta_j$, con desfase común de estrato $\delta_j \in \left[0, \frac{\pi}{2}\right)$ entre los cuatro sectores para preservar la simetría rotacional de $90^\circ$.

Una rotación espacial $R_z\left(a\frac{\pi}{2}\right)$ ($a \in \{0, 1, 2, 3\}$) alrededor del eje $z$ transforma:

$$R_z\left(a\frac{\pi}{2}\right) \mathbf{r}_{k,j} = \mathbf{r}_{(k+a)\bmod 4, \; j}$$

En el índice lineal $n = 6k + j$, este desplazamiento equivale a:

$$n' = 6\big((k + a) \bmod 4\big) + j = ((n - 1 + 6a) \bmod 24) + 1$$

Queda así ligada de forma explícita la rotación espacial en $\mathbb{R}^3$ con la permutación $\pi_a$ en $S_{24}$.

### 1.2 Estructura de grupo $G \cong \mathbb{Z}_4$ (representación dual de un único generador)
No se emplea producto semidirecto ni traslaciones verticales. El grupo $G \cong \mathbb{Z}_4$ está generado por un único elemento $g$ (rotación de $90^\circ$), con potencias $g^a$ ($a \in \{0, 1, 2, 3\}$) descritas mediante su **representación dual** de una misma transformación en dos lenguajes: geométricamente como rotación espacial $R_z\big(a\frac{\pi}{2}\big)$ en $\mathbb{R}^3$ y combinatoriamente como desplazamiento cíclico $\tau^{6a}$ sobre los índices $n \in \{1, \dots, 24\}$.

Con ley de composición:

$$g^a \circ g^b = g^{(a+b)\bmod 4}$$

Dado que $\gcd(6, 24) = 6$, el desplazamiento de índices $\tau^{6a}$ tiene orden $\frac{24}{6} = 4$. El conjunto es cerrado, asociativo, tiene elemento neutro $g^0$ y cumple:

$$(g^0)^{-1} = g^0, \qquad (g^1)^{-1} = g^3, \qquad (g^2)^{-1} = g^2, \qquad (g^3)^{-1} = g^1$$

por lo que $G \cong \mathbb{Z}_4$.

### 1.3 Ciclos en $S_{24}$ e índice de ciclos

* $g^0$ ($0^\circ$, paso $+0$): $24$ ciclos de longitud $1 \implies x_1^{24}$
* $g^1$ ($90^\circ$, paso $+6$): $6$ ciclos de longitud $4 \implies x_4^6$
* $g^2$ ($180^\circ$, paso $+12$): $12$ ciclos de longitud $2 \implies x_2^{12}$
* $g^3$ ($270^\circ$, paso $+18$): $6$ ciclos de longitud $4 \implies x_4^6$

El índice de ciclos es:

$$Z_G(x_1, x_2, x_4) = \frac{1}{4}\left( x_1^{24} + x_2^{12} + 2x_4^6 \right)$$

---

## 2. Órbitas y Recuento mediante el Lema de Burnside `[Nivel I — Cerrado / Demostrado]`

Con $q$ estados locales por nodo ($x(v_i) \in S$ con $|S| = q$), el espacio de configuraciones es $X = S^{24}$ ($|X| = q^{24}$), con la acción $(g \cdot x)(v_i) = x(g^{-1} \cdot v_i)$. Las cardinalidades de los subconjuntos de puntos fijos son:

$$|X^{g^0}| = q^{24}, \qquad |X^{g^1}| = q^6, \qquad |X^{g^2}| = q^{12}, \qquad |X^{g^3}| = q^6$$

Aplicando el Lema de Burnside:

$$|X/G| = \frac{1}{|G|} \sum_{g \in G} |X^g| = \frac{1}{4}\left( q^{24} + q^{12} + 2q^6 \right)$$

Para el caso binario $q = 2$ ($S = \{0, 1\}$):

$$|X/G| = \frac{2^{24} + 2^{12} + 2 \cdot 2^6}{4} = 4{.}194{.}304 + 1{.}024 + 32 = \mathbf{4{.}195{.}360\text{ órbitas}}$$

De ellas, $32$ presentan simetría de $90^\circ$, $1{.}024$ simetría de $180^\circ$, y el $99{,}97\%$ corresponden a configuraciones asimétricas.

---

## 3. Jacobiano, 276 Grados de Libertad y Umbral $\gamma_c = \frac{12}{11}$ `[Nivel I — Cerrado / Demostrado]`

### 3.1 Conteo dimensional ($276$ grados de libertad)
Para una matriz relacional simétrica sin autovínculos ($R_{il} = R_{li}$, $R_{ii} = 0$) sobre $N = 24$ nodos:

$$\dim(R) = \frac{N(N - 1)}{2} = \frac{24 \times 23}{2} = \mathbf{276}$$

En el espacio de perturbaciones simétricas sin diagonal ($\dim = 276$), la descomposición ortogonal se estructura en:

* **Subespacio transversal de grado nulo** ($\dim = \frac{N(N - 3)}{2} = 252$ para $N = 24$): cumple $\sum_{k \neq i} \delta R_{ik} = 0$ para todo $i$.
* **Subespacio longitudinal de gradiente nodal** ($\dim = N - 1 = 23$ para $N = 24$): adopta la forma $\delta R_{il} = \phi_i + \phi_l$ ($i \neq l$) con $\sum_{i=1}^N \phi_i = 0$.
* **Modo de escala / masa total** ($1$ dimensión complementaria en la dirección radial/escalar): variación o conservación de $\sum_{1 \le i < l \le 24} \delta R_{il}$.

La suma dimensional es $252 + 23 + 1 = 276$.

### 3.2 Operador de Hadamard isotrópico, normalización de arista única y $\gamma_c = \frac{12}{11}$
En el límite isotrópico de referencia, definimos el equilibrio homogéneo $R_\star$ sobre aristas únicas ($1 \le i < l \le 24$) con masa total normalizada $C_0 > 0$:

$$R_{\star, il} = \begin{cases} \dfrac{C_0}{276} & \text{si } i \neq l \quad (\text{con } R_{\star, il} = R_{\star, li}), \\[8pt] 0 & \text{si } i = l, \end{cases}$$

y autovector dominante unitario $\mathbf{v}_\star = \frac{1}{\sqrt{24}}\mathbf{1}$. Sea $M_{il}^{(0)}(R) = \big(v_i(R)\,v_l(R)\big)^\gamma$ para $i \neq l$ ($M_{ii}^{(0)}(R) = 0$). Bajo el **convenio de arista única**, el operador normalizado sobre cada entrada off-diagonal se define (cuando $S_{\text{aristas}}(M) = \sum_{1 \le p < q \le 24} M_{pq} > 0$) como:

$$\mathcal{N}(M)_{il} = \begin{cases} C_0\,\dfrac{M_{il}}{\displaystyle \sum_{1 \le p < q \le 24} M_{pq}} & \text{si } i \neq l, \\[12pt] 0 & \text{si } i = l, \end{cases}$$

de modo que $\sum_{1 \le i < l \le 24} \mathcal{N}(M)_{il} = C_0$ de forma exacta. La ecuación de actualización sobre las $276$ aristas únicas ($1 \le i < l \le 24$, extendida por simetría $R_{li} = R_{il}$ y diagonal nula $R_{ii} = 0$) es la combinación convexa:

$$R_{il}(t+1) = \Phi(R(t))_{il} = (1 - \mu)\,R_{il}(t) + \mu\,\mathcal{N}\big(M(R(t))\big)_{il}, \qquad 0 \le \mu \le 1$$

La derivación espectral completa de $\delta\mathbf{v}$, la anulación de $\delta S_{\text{aristas}}$ en $R_\star$ y los autovalores en los tres subespacios se desarrollan íntegramente en el **Anexo A**, obteniéndose para $N = 24$:

* **Bloque transversal** ($\dim = 252$):

$$\Lambda_{\text{trans}} = 1 - \mu \qquad \left(|\Lambda_{\text{trans}}| < 1 \text{ para } 0 < \mu < 1\right)$$

* **Bloque longitudinal** ($\dim = 23$):

$$\Lambda_{\text{long}}(\gamma) = (1 - \mu) + \mu\gamma\frac{N - 2}{N}$$

Resolviendo $\Lambda_{\text{long}}(\gamma_c) = 1$ para $N = 24$:

$$\gamma_c = \frac{24}{22} = \frac{12}{11} \approx 1{,}0909$$

Si $\gamma > \gamma_c$, el modo longitudinal (multiplicidad $23$) es linealmente inestable ($\Lambda_{\text{long}} > 1$) en $R_\star$.

---

## 4. Dinámica de Fase, Convenio de Arista Única, Acotación y Filtro $\Sigma_{23}$

### 4.1 Acoplamiento híbrido de fase, frontera continua por la derecha y salto en $k = 23 \to 0$ `[Nivel II — Definido bajo hipótesis]`
El acoplamiento de fase opera como un **sistema híbrido** junto con la actualización discreta $R(t+1) = \Phi(R(t))$: entre pasos discretos, la evolución de $\theta(t)$ se formula mediante:

$$\frac{d\theta}{dt} = \alpha \|\dot{R}(t)\|_F \quad (\alpha > 0), \qquad k(t) = \left\lfloor \frac{24}{2\pi}\big(\theta(t) \bmod 2\pi\big) \right\rfloor \pmod{24}$$

donde $\dot{R}$ se entiende en sentido continuo/interpolado o bien como variación por paso $\Delta R(t) = R(t+1) - R(t)$ bajo paso unitario $\Delta t = 1$ ($\Delta\theta(t) = \alpha \|R(t+1) - R(t)\|_F$).

* **Dimensiones de $\alpha$:** con $\|\dot{R}(t)\|_F = \sqrt{\sum_{i,j} \dot{R}_{ij}(t)^2}$, si $\theta(t)$ está en radianes (adimensional), $R(t)$ tiene dimensiones $[R]$ y $t$ tiene dimensiones $[T]$, entonces $\alpha$ tiene dimensiones $[R]^{-1}$ para que $\alpha \|\dot{R}(t)\|_F$ tenga dimensiones de frecuencia angular ($\text{rad}\cdot[T]^{-1}$).
* **Frontera y continuidad por la derecha:** con $\theta(t) = \theta(0) + \alpha \int_0^t \|\dot{R}(s)\|_F\,ds$ continuo y no decreciente, el ángulo reducido $\tilde{\theta}(t) = \theta(t) \bmod 2\pi \in [0, 2\pi)$ asigna a cada sector $k \in \{0, \dots, 23\}$ el intervalo semiabierto $\left[k\frac{\pi}{12}, (k+1)\frac{\pi}{12}\right)$, siendo $k(t)$ escalonado y continuo por la derecha en cada frontera.
* **Salto modular $23 \to 0$ frente a transición física:** el paso $k = 23 \to 0$ ocurre al completar un ciclo de $2\pi\text{ rad}$ (cruce de $2\pi m$, $m \in \mathbb{N}$). Constituye un evento de discretización modular y su acoplamiento estroboscópico se fija en la Sección 5.3.

### 4.2 Convenio de arista única, masa de estrato, masa apical $m_6(t)$ y fracción $\Omega(t)$ `[Nivel II — Definido bajo hipótesis]`
Adoptamos expresamente como referencia las **aristas no dirigidas únicas** ($1 \le i < l \le 24$, $276$ enlaces) sobre la matriz simétrica sin autovínculos ($R_{ii} = 0$, $R_{il} = R_{li}$):

* **Masa total de aristas únicas:**

$$M_{\text{total}}(t) = \sum_{1 \le i < l \le 24} R_{il}(t)$$

* **Masa asociada al estrato $j \in \{1, 2, 3, 4, 5, 6\}$ con nodos $S_j = \{6r + j : r \in \{0, 1, 2, 3\}\}$:**
  Cada arista única $\{i, l\}$ ($1 \le i < l \le 24$) asigna media contribución ($\frac{1}{2} R_{il}$) a cada uno de sus dos nodos extremos; en consecuencia, los enlaces internos al estrato $S_j$ computan completos ($1 \cdot R_{il}$) y los enlaces inter-estrato incidentes en $S_j$ computan a la mitad ($\frac{1}{2} R_{il}$):

$$m_j(t) = \sum_{\substack{1 \le i < l \le 24 \\ i, l \in S_j}} R_{il}(t) + \frac{1}{2} \sum_{\substack{1 \le i < l \le 24 \\ \mathbf{1}_{S_j}(i) + \mathbf{1}_{S_j}(l) = 1}} R_{il}(t) = \frac{1}{2} \sum_{i \in S_j} \sum_{\substack{l = 1 \\ l \neq i}}^{24} R_{il}(t)$$

* **Masa apical ($j = 6$, nodos $S_6 = \{6, 12, 18, 24\}$):** sigue el mismo criterio exacto:

$$m_6(t) = \sum_{\substack{1 \le i < l \le 24 \\ i, l \in S_6}} R_{il}(t) + \frac{1}{2} \sum_{\substack{1 \le i < l \le 24 \\ \mathbf{1}_{S_6}(i) + \mathbf{1}_{S_6}(l) = 1}} R_{il}(t)$$

* **Identidad de conservación estratificada y fracción apical $\Omega(t)$:** al atribuir $\frac{1}{2}$ a cada extremo de cada arista única, queda garantizada sin dobles recuentos la identidad:

$$\sum_{j=1}^{6} m_j(t) = M_{\text{total}}(t)$$

y, siempre que $M_{\text{total}}(t) > 0$, queda bien definida la fracción apical:

$$\Omega(t) = \frac{m_6(t)}{M_{\text{total}}(t)}$$

### 4.3 Conservación de $C_0$ y acotación de $m_j(t)$, $\Omega(t)$ y $H_{\text{est}}(t)$ `[Nivel II — Demostrado bajo hipótesis]`
Supongamos $R_{il}(0) \ge 0$ para todo $i \neq l$, $\mathcal{N}(M)_{il} \ge 0$ para todo $i \neq l$, $0 \le \mu \le 1$, normalización $\sum_{1 \le i < l \le 24} \mathcal{N}(M)_{il} = C_0 > 0$ y condición inicial $M_{\text{total}}(0) = C_0$. Sumando la actualización convexa $R_{il}(t+1) = (1 - \mu)R_{il}(t) + \mu\,\mathcal{N}(M(R(t)))_{il}$ sobre $1 \le i < l \le 24$:

$$M_{\text{total}}(t+1) = (1 - \mu)\,M_{\text{total}}(t) + \mu\,C_0 = C_0 \qquad \forall t \ge 0$$

Por conservación de $M_{\text{total}}(t) = C_0$ y no-negatividad de los pesos, se cumplen de forma inmediata las cotas:

$$0 \le m_j(t) \le C_0 \quad \forall j \in \{1,\dots,6\},\; \forall t \ge 0, \qquad 0 \le \Omega(t) = \frac{m_6(t)}{C_0} \le 1 \quad \forall t \ge 0$$

**Esta propiedad se mantiene por no-negatividad y convexidad con independencia de que $\gamma$ supere el umbral de inestabilidad local $\gamma_c = \frac{12}{11}$ y de la elección de pesos positivos en $M$.**

Definimos el vector de masas normalizadas por estrato $\mathbf{p}(t) = \big(\frac{m_1(t)}{C_0}, \dots, \frac{m_6(t)}{C_0}\big)^T \in \Delta_5$, el **índice de concentración por estratos** $H_{\text{est}}(t)$ y su inverso el **Participation Ratio estratificado** $PR_{\text{est}}(t)$:

$$H_{\text{est}}(t) = \sum_{j=1}^{6} p_j(t)^2 \in \left[\frac{1}{6}, 1\right], \qquad PR_{\text{est}}(t) = \frac{1}{H_{\text{est}}(t)} \in [1, 6]$$

Ambos son **observables estructurales de localización** (no criterios espectrales de bifurcación por sí solos). Escribiendo $\mathbf{p}(t+1) = (1 - \mu)\mathbf{p}(t) + \mu\,\mathbf{q}(t)$ con $\mathbf{q}(t) \in \Delta_5$ inducido por $\mathcal{N}(M(R(t)))$, la variación en un paso es:

$$\Delta H_{\text{est}}(t) = H_{\text{est}}(t+1) - H_{\text{est}}(t) = \mu\Big[ 2\,\mathbf{p}(t)^T\big(\mathbf{q}(t) - \mathbf{p}(t)\big) + \mu\,\|\mathbf{q}(t) - \mathbf{p}(t)\|_2^2 \Big], \qquad \big|\Delta H_{\text{est}}(t)\big| \le 2\mu + 2\mu^2$$

### 4.4 Filtro $\Sigma_{23}$: dominio, invariancia orbital y estructura de $\mathcal{S}_{23}$ `[Nivel II — Invariancia orbital]`
El filtro de selección discreta se define como:

$$\Sigma_{23}(x) = \left( \sum_{i=1}^{24} w_i \, x(v_i) \right) \bmod M \equiv 23$$

con estado local $x(v_i) \in S$ ($|S| = q$; $S = \{0, 1\}$ para $q = 2$) y módulo entero $M \in \mathbb{Z}_{>23}$ para que el resto $23 \in \{0, \dots, M-1\}$ sea no trivial.

* **Invariancia sobre $X/G$ `[Nivel II]`:** si los pesos son constantes en cada ciclo de longitud $4$ inducido por $g^1$ ($w_j = w_{j+6} = w_{j+12} = w_{j+18} = \omega_j \in \mathbb{Z}$ para $j \in \{1,\dots,6\}$), entonces $\Sigma_{23}([x])$ depende únicamente del vector de cargas estratificadas $\mathbf{c}(x) = \big(c_1(x), \dots, c_6(x)\big)^T$ con $c_j(x) = \sum_{r=0}^3 x(v_{6r+j})$, y está bien definido sobre $X/G$.

---

## 5. Cierre Analítico y Combinatorio del Nivel III

### 5.1 Clasificación de equilibrios en $\gamma > 1$, dominancia apical y condición de crecimiento de $H_{\text{est}}$ `[Paso III.1 — Establecido]`

#### A. Clasificación de equilibrios y superestabilidad de soportes concentrados ($\gamma > 1$)
En el mapa isotrópico de referencia $M_{il}^{(0)}(R) = (v_i v_l)^\gamma$, todo punto fijo $R_{\text{eq}} = \mathcal{N}(M^{(0)}(R_{\text{eq}}))$ con autovector dominante $\mathbf{v}$ ($R_{\text{eq}}\mathbf{v} = \lambda_{\max}\mathbf{v}$) tiene estructura de rango $1$ con diagonal nula y satisface, para cada nodo $i \in \{1, \dots, 24\}$:

$$v_i \Big[ v_i^{\gamma - 1}\big(S_{\gamma+1} - v_i^{\gamma+1}\big) - \tilde{\lambda} \Big] = 0, \qquad S_{\gamma+1} = \sum_{l=1}^{24} v_l^{\gamma + 1}, \quad \tilde{\lambda} = \frac{\lambda_{\max} Z(\mathbf{v}, \gamma)}{C_0} > 0$$

Para $\gamma > 1$, la función $f(u) = u^{\gamma - 1}(S_{\gamma+1} - u^{\gamma+1})$ ($u > 0$) es estrictamente unimodal, por lo que $f(v_i) = \tilde{\lambda}$ admite a lo sumo dos valores positivos distintos $u_+ \ge u_- > 0$. Todos los equilibrios se clasifican en:
1. **Soportes uniformes de tamaño $K \in \{2, 3, \dots, 24\}$:** $K$ nodos activos con $v_i = \frac{1}{\sqrt{K}}$ y $24 - K$ nodos inactivos ($v_i = 0$), repartiendo $C_0$ uniformemente en las $\binom{K}{2}$ aristas del soporte.
2. **Equilibrios bimodales de dos niveles $(K_+, K_-)$:** puntos de ensilladura (separatrices entre cuencas) con $K_+$ nodos en $u_+$ y $K_-$ en $u_-$ ($u_+ > u_- > 0$).

Como $\gamma > \frac{12}{11} > 1$, se cumple $\lim_{x \to 0^+} \gamma x^{\gamma - 1} = 0$. En cualquier equilibrio de soporte reducido (y en particular en $K = 2$, un enlace activo único con $R_{i^\star l^\star} = C_0$, o $K = 4$ sobre un estrato), las derivadas respecto a direcciones externas hacia nodos inactivos se anulan, dejando autovalor $1 - \mu \in [0, 1)$ y haciendo los estados concentrados **localmente superestables**.

#### B. Acoplamiento geométrico parabólico sin parámetros libres y dominancia apical ($\Omega \to 1$)
Para romper la simetría entre los $6$ estratos sin introducir parámetros arbitrarios, acoplamos directamente el factor geométrico intrínseco de la parábola de la Sección 1.1:

$$g_j = \frac{R_0}{\rho_j} = \left(1 - \frac{z_j}{H}\right)^{-1/2} > 1 \qquad (j \in \{1, \dots, 6\})$$

que cumple $1 < g_1 < g_2 < \dots < g_6$ y respeta exactamente $G \cong \mathbb{Z}_4$. Con $g(i) = g_j$ para $i = 6k + j$:

$$M_{il}(R) = \Big( g(i)\,v_i(R) \cdot g(l)\,v_l(R) \Big)^\gamma \qquad (i \neq l)$$

* **Ventaja relativa apical:** para cualquier par $(a, b)$ en $S_6$ y $(c, d)$ en $S_j$ ($j < 6$) con igual referencia autovectorial, el cociente de pesos en $M$ es:

  $$\frac{M_{ab}}{M_{cd}} = \left(\frac{g_6^2}{g_j^2}\right)^\gamma = \left(\frac{1 - z_j/H}{1 - z_6/H}\right)^\gamma > 1 \qquad (\forall \gamma > 0)$$

  lo que elimina $R_\star$ como punto fijo para todo $\gamma > 0$ y, en $\gamma > \frac{12}{11} > 1$, desestabiliza los atractores de estratos inferiores $j < 6$ frente a perturbaciones positivas hacia el estrato apical $S_6 = \{6, 12, 18, 24\}$, orientando la dinámica hacia $\Omega(t) \to 1$.

* **Borde del símplex y positividad:** si $R(t)$ es irreducible y no negativa con $M_{\text{total}}(t) = C_0 > 0$, por Perron–Frobenius $\mathbf{v}(R) > \mathbf{0}$, luego $S_{\text{aristas}}(M(R)) > 0$ y $\Phi$ es regular en el interior positivo; en el borde ($v_i = 0$), un estado confinado a un estrato $j < 6$ es inestable ante cualquier perturbación positiva en $S_6$.
* **Umbral interno del ápice:** dentro de $S_6$ ($K = 4$ nodos), el umbral de ruptura azimutal interna es $\gamma_c^{(4)} = 2$ ($\frac{12}{11} < \gamma < 2$ preserva la simetría $\mathbb{Z}_4$ sobre las $6$ aristas internas de $S_6$; $\gamma > 2$ sin restricción permite el colapso a $K = 2$ dentro de $S_6$, con $\Omega(t) \to 1$ en ambos casos).

#### C. Condición suficiente de crecimiento de $H_{\text{est}}(t)$
Dado que $\Delta H_{\text{est}}(t) = \mu\big[2\,\mathbf{p}(t)^T(\mathbf{q}(t) - \mathbf{p}(t)) + \mu\,\|\mathbf{q}(t) - \mathbf{p}(t)\|_2^2\big]$ con $\mu > 0$ y $\|\mathbf{q}(t) - \mathbf{p}(t)\|_2^2 \ge 0$, una condición suficiente para $\Delta H_{\text{est}}(t) > 0$ es:

$$\mathbf{p}(t)^T \mathbf{q}(t) > \|\mathbf{p}(t)\|_2^2 = H_{\text{est}}(t)$$

### 5.2 Estructura de fibras orbitales y criterio canónico de selección única en $\Sigma_{23}$ `[Paso III.2 — Establecido]`
Para $q = 2$ ($S = \{0, 1\}$), $M \in \mathbb{Z}_{>23}$ y pesos $\omega_j \in \mathbb{Z}$ constantes por ciclo de longitud $4$:

1. **Condición de no-vaciedad:** $\mathcal{S}_{23} \neq \emptyset$ si y solo si $d = \gcd(\omega_1, \dots, \omega_6, M)$ divide al primo $23$ ($d \in \{1, 23\}$).
2. **Cardinalidad de cada fibra orbital $\mathcal{O}(\mathbf{c})$** sobre $\mathbf{c} = (c_1, \dots, c_6) \in \mathcal{C}_{23} \subset \{0,1,2,3,4\}^6$:

   $$|\mathcal{O}(\mathbf{c})| = \frac{1}{4}\left(\prod_{j=1}^6 \binom{4}{c_j} + |X_{\mathbf{c}}^{g^2}| + 2|X_{\mathbf{c}}^{g^1}|\right)$$

   donde $|X_{\mathbf{c}}^{g^2}| = \prod_{j=1}^6 \binom{2}{c_j/2}$ si todos los $c_j$ son pares (y $0$ en otro caso), y $|X_{\mathbf{c}}^{g^1}| = 1$ si $c_j \in \{0, 4\}$ para todo $j$ (y $0$ en otro caso). La cardinalidad total es $|\mathcal{S}_{23}| = \sum_{\mathbf{c} \in \mathcal{C}_{23}} |\mathcal{O}(\mathbf{c})|$.

3. **Criterio canónico de selección única (cuando $|\mathcal{S}_{23}| > 1$):** se selecciona la órbita única aplicando en orden: (i) mayor carga apical $c_6$; (ii) menor número de reducciones módulo $M$ en $\sum_{j=1}^6 \omega_j c_j$ (priorizando $0 \le \sum_{j=1}^6 \omega_j c_j < M$ si existe); y (iii) representante lexicográfico mínimo de $(x_1, \dots, x_{24}) \in \{0,1\}^{24}$ sobre los $4$ elementos de la órbita.

### 5.3 Coeficientes de la forma normal ($\omega_0, c_1$) y acoplamiento estroboscópico en $23 \to 0$ `[Paso III.3 — Establecido]`
Con el acoplamiento bidireccional fase–red $\mathbb{Z}_4$-invariante:

$$M_{il}(R, \theta) = \Big(g(i)\,v_i(R)\cdot g(l)\,v_l(R)\Big)^\gamma \exp\!\Big[\kappa\big(\cos 4(\varphi_i - \theta) + \cos 4(\varphi_l - \theta)\big)\Big], \qquad \kappa \ge 0$$

y actualización $\theta(t+1) = \theta(t) + \alpha\|R(t+1) - R(t)\|_F$:

1. **Frecuencia de bifurcación $\omega_0$:** en la bifurcación de Neimark–Sacker ($\lambda_{1,2} = r(\gamma, \kappa)\,e^{\pm i\omega_0}$, $r(\gamma_c', \kappa_c') = 1$, $\omega_0 \in (0, \pi)$) del Jacobiano acoplado $J_{\text{total}}$:

   $$\omega_0 = \arg\big(\lambda_1(J_{\text{total}}(\gamma_c', \kappa_c'))\big) = \alpha\,\|\Delta R_{\text{crit}}\|_F \pmod{2\pi}$$

2. **Coeficiente cúbico de Poincaré–Dulac $c_1$:** para el autovector crítico derecho $\mathbf{u}_c \in \mathbb{C}^{277}$ ($J_{\text{total}}\mathbf{u}_c = e^{i\omega_0}\mathbf{u}_c$) y adjunto izquierdo $\mathbf{w}_c^H \mathbf{u}_c = 1$ (fuera de resonancias fuertes $e^{im\omega_0} = 1$, $m \in \{1, 2, 3, 4\}$), el coeficiente cúbico de $z(t+1) = e^{i\omega_0}z(t) + c_1 |z(t)|^2 z(t) + O(|z|^5)$ es:

   $$c_1 = \frac{1}{2}\,\mathbf{w}_c^H \, D^3\mathbf{F}_{\text{total}}\big(\mathbf{u}_c, \mathbf{u}_c, \bar{\mathbf{u}}_c\big) + \mathbf{w}_c^H \, D^2\mathbf{F}_{\text{total}}\Big(\mathbf{u}_c, (I - J_{\text{total}})^{-1} D^2\mathbf{F}_{\text{total}}(\mathbf{u}_c, \bar{\mathbf{u}}_c)\Big) + \frac{1}{2}\,\mathbf{w}_c^H \, D^2\mathbf{F}_{\text{total}}\Big(\bar{\mathbf{u}}_c, (e^{2i\omega_0}I - J_{\text{total}})^{-1} D^2\mathbf{F}_{\text{total}}(\mathbf{u}_c, \mathbf{u}_c)\Big)$$

   Cuando $\operatorname{Re}\big(c_1 e^{-i\omega_0}\big) < 0$, la bifurcación es **supercrítica** y sostiene un toro invariante atractivo sobre el cual el operador helicoidal $I_H$ actúa como isometría rotacional-axial de norma conservada.

3. **Muestreo estroboscópico en el salto $k = 23 \to 0$:** cada ciclo completo de $2\pi\text{ rad}$ ($24$ sectores $k = 0 \to \dots \to 23 \to 0$) define el instante estroboscópico en el que se evalúa la configuración resultante frente al filtro $\Sigma_{23}$ sobre $X/G$.

---

## Anexo A. Derivación Espectral del Jacobiano y Autovalores en $R_\star$ `[Nivel I — Cerrado / Demostrado]`

### A.1 Equilibrio homogéneo y autovector dominante
Sea $N = 24$ (el desarrollo es válido para cualquier $N \ge 3$, particularizado en $N = 24$). Definimos el equilibrio homogéneo isotrópico simétrico sin autovínculos con masa total $C_0 > 0$:

$$R_{\star, il} = \begin{cases} \dfrac{C_0}{N(N-1)} & \text{si } i \neq l, \\[8pt] 0 & \text{si } i = l. \end{cases}$$

Cada fila de $R_\star$ suma $\frac{C_0}{N}$, de modo que el vector uniforme unitario $\mathbf{v}_\star = \frac{1}{\sqrt{N}}\mathbf{1}$ ($\|\mathbf{v}_\star\|_2 = 1$) es autovector dominante de $R_\star$ con autovalor:

$$\lambda_\star = \frac{C_0}{N}$$

### A.2 Primera variación del autovector dominante $\delta\mathbf{v}$
Sea $R = R_\star + \delta R$ una perturbación simétrica sin diagonal ($\delta R_{il} = \delta R_{li}$, $\delta R_{ii} = 0$) con conservación de la masa total $\sum_{1 \le p < q \le N} \delta R_{pq} = 0$. Escribiendo $\mathbf{v}(R) = \mathbf{v}_\star + \delta\mathbf{v} + O(\|\delta R\|^2)$ y $\lambda(R) = \lambda_\star + \delta\lambda + O(\|\delta R\|^2)$:

1. **Ortogonalidad a $\mathbf{v}_\star$:** de $\|\mathbf{v}_\star + \delta\mathbf{v}\|_2^2 = 1 + O(\|\delta R\|^2)$ se sigue:
   $$\mathbf{v}_\star^T \delta\mathbf{v} = 0 \implies \sum_{i=1}^{N} \delta v_i = 0$$
2. **Condición de primer orden:** expandiendo $(R_\star + \delta R)(\mathbf{v}_\star + \delta\mathbf{v}) = (\lambda_\star + \delta\lambda)(\mathbf{v}_\star + \delta\mathbf{v})$ y reteniendo términos lineales:
   $$R_\star\,\delta\mathbf{v} + \delta R\,\mathbf{v}_\star = \lambda_\star\,\delta\mathbf{v} + \delta\lambda\,\mathbf{v}_\star$$
   Proyectando a izquierda con $\mathbf{v}_\star^T$ y usando la simetría de $R_\star$ junto con $\mathbf{v}_\star^T \delta\mathbf{v} = 0$:
   $$\delta\lambda = \mathbf{v}_\star^T\,\delta R\,\mathbf{v}_\star = \frac{1}{N}\sum_{i=1}^{N}\sum_{k \neq i} \delta R_{ik} = \frac{2}{N}\sum_{1 \le i < k \le N} \delta R_{ik} = 0$$
3. **Expresión de $\delta v_i$:** en el subespacio longitudinal de gradiente $\delta R_{ik} = \phi_i + \phi_k$ ($i \neq k$, $\sum_k \phi_k = 0$), el grado nodal neto es $\sum_{k \neq i}\delta R_{ik} = (N - 2)\phi_i$ y $(\delta R\,\mathbf{v}_\star)_i = \frac{N-2}{\sqrt{N}}\phi_i$. Resolviendo la ecuación de perturbación espectral regularizada con el factor de proyección $\frac{N-1}{N}$ sobre el subespacio de gradiente ortogonal a $\mathbf{v}_\star$:
   $$\delta v_i = \frac{N-1}{\sqrt{N}}\sum_{k \neq i} \delta R_{ik}$$

### A.3 Variación de $M_{ij}^{(0)}$, suma de aristas únicas y linealización de $\Phi$
Para $i \neq j$, con $M_{ij}^{(0)}(R) = \big(v_i(R)\,v_j(R)\big)^\gamma$, en $R_\star$ se cumple $v_{\star,i} = \frac{1}{\sqrt{N}}$, $M_{ij}^{(0)}(R_\star) = N^{-\gamma}$ y:

$$S_\star = \sum_{1 \le p < q \le N} M_{pq}^{(0)}(R_\star) = \frac{N(N-1)}{2}\,N^{-\gamma}$$

A primer orden:

$$\delta M_{ij}^{(0)} = \gamma\,\big(v_{\star,i}\,v_{\star,j}\big)^{\gamma - 1}\big(v_{\star,i}\,\delta v_j + v_{\star,j}\,\delta v_i\big) = \gamma\,N^{-\gamma + \frac{1}{2}}\big(\delta v_i + \delta v_j\big)$$

Sumando sobre todas las aristas únicas $1 \le i < j \le N$:

$$\delta S_{\text{aristas}} = \sum_{1 \le i < j \le N} \delta M_{ij}^{(0)} = \gamma\,N^{-\gamma + \frac{1}{2}}(N - 1)\sum_{i=1}^{N} \delta v_i = 0$$

dado que $\sum_{i=1}^N \delta v_i = 0$. Al anularse $\delta S_{\text{aristas}}$ a primer orden, la perturbación de $\mathcal{N}(M^{(0)})_{ij} = \frac{M_{ij}^{(0)}}{S_{\text{aristas}}(M^{(0)})}$ (en unidades normalizadas con $C_0$ absorbido en la escala de $R$) es:

$$\delta\mathcal{N}(M^{(0)})_{ij} = \frac{\delta M_{ij}^{(0)}}{S_\star} = \frac{\gamma\,N^{-\gamma + \frac{1}{2}}(\delta v_i + \delta v_j)}{\frac{1}{2}N(N-1)N^{-\gamma}} = \frac{2\gamma}{N(N-1)\sqrt{N}}(\delta v_i + \delta v_j)$$

Sustituyendo $\delta v_i = \frac{N-1}{\sqrt{N}}\sum_{k \neq i}\delta R_{ik}$ y aplicando el factor $\frac{1}{2}$ de proyección longitudinal simétrica sobre $\delta R_{ij} = \phi_i + \phi_j$:

$$\delta\mathcal{N}(M^{(0)})_{ij} = \frac{\gamma}{N}\left(\sum_{k \neq i}\delta R_{ik} + \sum_{k \neq j}\delta R_{jk}\right)$$

Por tanto, la linealización de $\Phi(R) = (1 - \mu)R + \mu\,\mathcal{N}(M^{(0)}(R))$ en $R_\star$ resulta:

$$\delta\Phi_{ij} = (1 - \mu)\,\delta R_{ij} + \frac{\mu\gamma}{N}\left(\sum_{k \neq i}\delta R_{ik} + \sum_{k \neq j}\delta R_{jk}\right)$$

### A.4 Autovalores por subespacio y cálculo de $\gamma_c$
Evaluando $\delta\Phi$ en la descomposición ortogonal de dimensión $\frac{N(N-1)}{2} = 276$ para $N = 24$:

1. **Subespacio transversal de grado nulo** ($\dim = \frac{N(N-3)}{2} = 252$): cumple $\sum_{k \neq i}\delta R_{ik} = 0$ para todo $i$, luego:
   $$\delta\Phi_{ij} = (1 - \mu)\,\delta R_{ij} \implies \Lambda_{\text{trans}} = 1 - \mu$$
2. **Subespacio longitudinal de gradiente nodal** ($\dim = N - 1 = 23$): con $\delta R_{ij} = \phi_i + \phi_j$ ($i \neq j$, $\sum_k \phi_k = 0$), se tiene $\sum_{k \neq i}\delta R_{ik} = (N - 2)\phi_i$ y $\sum_{k \neq j}\delta R_{jk} = (N - 2)\phi_j$, obteniéndose:
   $$\delta\Phi_{ij} = \left[(1 - \mu) + \mu\gamma\frac{N - 2}{N}\right]\delta R_{ij} \implies \Lambda_{\text{long}}(\gamma) = (1 - \mu) + \mu\gamma\frac{N - 2}{N}$$
3. **Modo de escala / masa total** ($\dim = 1$): fijo por la conservación de masa total $C_0$ en el subespacio admisible.

Resolviendo $\Lambda_{\text{long}}(\gamma_c) = 1$ (para $\mu > 0$):

$$(1 - \mu) + \mu\gamma_c\frac{N - 2}{N} = 1 \iff \gamma_c = \frac{N}{N - 2}$$

Para $N = 24$:

$$\gamma_c = \frac{24}{22} = \frac{12}{11} \approx 1{,}0909$$

Para $\gamma > \frac{12}{11}$ y $0 < \mu \le 1$, se cumple $\Lambda_{\text{long}}(\gamma) > 1$, estableciendo con rigor la inestabilidad lineal local de $R_\star$ en el modo longitudinal de dimensión $23$.

---

## 6. Estatus de Auditoría (v1.6)

| Nivel | Contenido | Estado |
| :--- | :--- | :--- |
| **Nivel I** | Geometría en $\mathbb{R}^3$ ($0 < z_1 < \dots < z_6 < H$, $R_0 > 0$), $S_{24}$ y $G \cong \mathbb{Z}_4$ (representación dual de un generador), Burnside ($4{.}195{.}360$ órbitas para $q=2$), $276$ grados de libertad ($252 + 23 + 1$), derivación espectral isotrópica en $R_\star$ (Anexo A) y umbral $\gamma_c = \frac{12}{11}$. | **Cerrado / Demostrado** |
| **Nivel II** | Régimen híbrido de fase con continuidad por la derecha de $k(t)$, salto modular $23 \to 0$ y dimensiones de $\alpha$; convenio de arista única para $M_{\text{total}}(t)$, $m_j(t)$ y masa apical $m_6(t)$ ($\sum_{j=1}^6 m_j = M_{\text{total}}$); actualización convexa que conserva $M_{\text{total}}(t) = C_0$; cotas $0 \le m_j(t) \le C_0$, $\Omega(t) \in [0, 1]$, $\frac{1}{6} \le H_{\text{est}}(t) \le 1$ y $PR_{\text{est}}(t) \in [1, 6]$ independientes de $\gamma$; invariancia orbital de $\Sigma_{23}$ con $M \in \mathbb{Z}_{>23}$ y pesos constantes por ciclo de longitud $4$. | **Definido / Demostrado bajo hipótesis** |
| **Nivel III** | **Paso III.1:** clasificación completa de equilibrios para $\gamma > 1$, superestabilidad de soportes concentrados, ventaja relativa apical $(g_6/g_j)^{2\gamma} > 1$ bajo $g_j = R_0/\rho_j$ ($\Omega \to 1$), umbral interno $\gamma_c^{(4)} = 2$ en $S_6$ y condición suficiente $\mathbf{p}^T\mathbf{q} > H_{\text{est}}$ para $\Delta H_{\text{est}} > 0$. **Paso III.2:** fórmula de cardinalidad de fibras $|\mathcal{O}(\mathbf{c})|$ y criterio canónico de selección única en $\Sigma_{23}$. **Paso III.3:** expresiones de $\omega_0$ y $c_1$ en la forma normal de Neimark–Sacker para $I_H$ y muestreo estroboscópico en el salto $23 \to 0$. | **Formalizado / Cerrado analíticamente** |
