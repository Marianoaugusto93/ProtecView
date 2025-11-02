import numpy as np


def calculate_inrush(kva, kv, multiplier, restraint_factor):
    """
    Estima as correntes de Inrush (pico, Iop, Ir) em p.u. da corrente nominal.
    """
    results = {
        'i_nominal_amps': 0.0,
        'i_peak_amps': 0.0,
        'iop_pu': 0.0,
        'ir_pu': 0.0
    }

    try:
        # --- 1. Calcular Corrente Nominal (Amperes) ---
        # (Assumindo trifásico, kV é linha-linha)
        i_nominal_amps = float(kva) / (np.sqrt(3) * float(kv))
        results['i_nominal_amps'] = i_nominal_amps

        # --- 2. Calcular Corrente de Inrush de Pico (Amperes) ---
        i_peak_amps = i_nominal_amps * float(multiplier)
        results['i_peak_amps'] = i_peak_amps

        # --- 3. Calcular Iop e Ir em p.u. (referente a I_nominal) ---
        # Iop (RMS) = Ipeak / sqrt(2)
        # Iop (p.u.) = (Ipeak / sqrt(2)) / I_nominal
        # Iop (p.u.) = (I_nominal * multiplier) / (sqrt(2) * I_nominal)
        iop_pu = float(multiplier) / np.sqrt(2)
        results['iop_pu'] = iop_pu

        # Ir (Restrição) = Iop * restraint_factor (ex: 0.5 para 2º harmónico)
        # (Nota: Esta é uma simplificação. A restrição real depende da definição do relé)
        ir_pu = iop_pu * float(restraint_factor)
        results['ir_pu'] = ir_pu

        return results

    except Exception as e:
        print(f"Erro ao calcular inrush: {e}")
        return results