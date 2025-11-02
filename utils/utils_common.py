# Ficheiro: utils/utils_common.py
import numpy as np

def polar_to_complex(mag, ang_deg):
    """
    Converte uma magnitude e um ângulo (em graus) para um número complexo.
    """
    try:
        rad = np.deg2rad(float(ang_deg))
        return float(mag) * (np.cos(rad) + 1j * np.sin(rad))
    except Exception:
        return 0j