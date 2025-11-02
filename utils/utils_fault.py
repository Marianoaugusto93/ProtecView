# Ficheiro: utils/utils_fault.py
import numpy as np
# Precisamos de importar a nossa própria função comum!
from utils.utils_common import polar_to_complex

def calculate_fault_currents(v_prefault, z1, z2, z0):
    """
    Calcula as correntes de falta (magnitudes) em p.u.
    Assume que V_prefault, Z1, Z2, e Z0 são números complexos.
    Retorna um dicionário com os resultados.
    """
    results = {
        '3ph': 0.0,
        'lg': 0.0,
        'll': 0.0
    }

    # Evita divisão por zero
    epsilon = 1e-9

    # --- 1. Falta Trifásica (3PH) ---
    try:
        i_3ph = v_prefault / (z1 + epsilon)
        results['3ph'] = np.abs(i_3ph)
    except Exception:
        pass  # Mantém 0.0

    # --- 2. Falta Fase-Terra (LG) ---
    try:
        z_total_lg = z1 + z2 + z0
        i_lg = (3 * v_prefault) / (z_total_lg + epsilon)
        results['lg'] = np.abs(i_lg)
    except Exception:
        pass  # Mantém 0.0

    # --- 3. Falta Fase-Fase (LL) ---
    try:
        z_total_ll = z1 + z2
        i_1 = v_prefault / (z_total_ll + epsilon)
        i_ll = i_1 * (np.sqrt(3))  # Magnitude (simplificado)
        results['ll'] = np.abs(i_ll)
    except Exception:
        pass  # Mantém 0.0

    return results
# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 4 ---