import numpy as np

class TRCGSimplexCore:
    """
    Nivel I - TRCG Module: Geometría y Conservación del Símplex R
    Define las restricciones fundamentales del símplex informacional de dimensión N = 24,
    incluyendo normalización, validación de pertenencia y proyección ortogonal.
    """
    def __init__(self, N: int = 24):
        self.N = N # Dimensión modular del símplex

    def initialize_barycentric(self) -> np.ndarray:
        """
        Retorna el punto barocéntrico uniforme de referencia en el símplex (R_i = 1/N).
        Representa el estado homogéneo de máxima simetría antes de la bifurcación.
        """
        return np.ones(self.N) / self.N

    def validate_simplex(self, R: np.ndarray, tol: float = 1e-7) -> bool:
        """
        Verifica rigurosamente si un vector R pertenece al símplex informacional:
        1. Consistencia dimensional ( len(R) == N )
        2. No negatividad ( R_i >= 0 )
        3. Normalización estricta ( sum(R_i) == 1 )
        """
        if len(R) != self.N:
            return False
        if np.any(R < -tol):
            return False
        if not np.isclose(np.sum(R), 1.0, atol=tol):
            return False
        return True

    def project_to_simplex(self, y: np.ndarray) -> np.ndarray:
        """
        Proyecta un vector arbitrario y sobre el símplex de probabilidad estándar
        mediante optimización lineal exacta. Garantiza que las actualizaciones 
        dinámicas no abandonen el espacio físico de estados.
        """
        n = len(y)
        u = np.sort(y)[::-1]
        cssv = np.cumsum(u) - 1
        ind = np.arange(n) + 1
        cond = u - cssv / ind > 0
        
        if not np.any(cond):
            return self.initialize_barycentric()
            
        rho = ind[cond][-1]
        theta = cssv[rho - 1] / rho
        w = np.maximum(y - theta, 0)
        return w / np.sum(w)

    def shannon_entropy(self, R: np.ndarray) -> float:
        """
        Calcula la entropía de Shannon S(R) = - sum(R_i log R_i),
        métrica escalar base para los potenciales de divergencia KL.
        """
        eps = 1e-15
        R_safe = np.clip(R, eps, 1.0)
        return -np.sum(R_safe * np.log(R_safe))

# --- Bloque de Validación y Ejecución (Nivel I) ---
if __name__ == "__main__":
    N_dim = 24
    simplex_core = TRCGSimplexCore(N=N_dim)
    
    print(f"==================================================")
    print(f" AUDITORÍA DE GEOMETRÍA DEL SÍMPLEX TRCG (N = {N_dim})")
    print(f"==================================================")
    
    # 1. Prueba del punto barocéntrico
    R_bar = simplex_core.initialize_barycentric()
    is_valid_bar = simplex_core.validate_simplex(R_bar)
    entropy_bar = simplex_core.shannon_entropy(R_bar)
    
    print(f" Estado Barocéntrico | Suma: {np.sum(R_bar):.6f}")
    print(f" ¿Pertenece al Símplex (Nivel I)?: {is_valid_bar}")
    print(f" Entropía de Shannon Base: {entropy_bar:.4f}")
    
    # 2. Prueba de proyección de un vector fuera de rango
    np.random.seed(42)
    y_arbitrary = np.random.randn(N_dim) * 3.0
    R_projected = simplex_core.project_to_simplex(y_arbitrary)
    is_valid_proj = simplex_core.validate_simplex(R_projected)
    
    print(f"\n Vector Externo Proyectado | Suma: {np.sum(R_projected):.6f}")
    print(f" ¿Válido tras proyección ortogonal?: {is_valid_proj}")
    print(f"==================================================")
