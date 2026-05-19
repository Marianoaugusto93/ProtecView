# Ficheiro: utils/utils_common.py

from typing import Union
import logging
import numpy as np

logger = logging.getLogger(__name__)


def polar_to_complex(mag: Union[float, int], ang_deg: Union[float, int]) -> complex:
    """
    Convert magnitude and angle (in degrees) to complex number.

    Args:
        mag: Magnitude value
        ang_deg: Angle in degrees

    Returns:
        Complex number representation
    """
    try:
        rad = np.deg2rad(float(ang_deg))
        return float(mag) * (np.cos(rad) + 1j * np.sin(rad))
    except (ValueError, TypeError) as e:
        logger.warning(f"Error converting polar to complex: {e}")
        return 0j