import numpy as np

# --- [INÍCIO] NOVAS FUNÇÕES DO MÓDULO 6 (SATURAÇÃO DE TC) ---

def check_ct_saturation(if_primary, ct_ratio_num, vk_actual, r_ct, r_b, xr_ratio):
    """
    Verifica a saturação do TC usando a fórmula de tensão de kneepoint ANSI.
    Retorna um dicionário com todos os resultados dos cálculos.
    """
    results = {
        'if_sec': 0.0,
        'vk_required': 0.0,
        'status': 'Erro'  # 'Saturação OK' ou 'SATURAÇÃO CRÍTICA'
    }

    try:
        # --- 1. Calcular Rácio do TC ---
        # (Assumindo que o secundário é sempre 5A)
        ct_ratio = float(ct_ratio_num) / 5.0

        # --- 2. Calcular Corrente Secundária de Falta ---
        if_sec = float(if_primary) / ct_ratio
        results['if_sec'] = if_sec

        # --- 3. Calcular Resistência Total do Secundário ---
        r_total = float(r_ct) + float(r_b)

        # --- 4. Calcular Tensão de Kneepoint Requerida (Vk,req) ---
        # Vk_req = If_sec * (Rct + Rb) * (1 + X/R)
        vk_required = if_sec * r_total * (1 + float(xr_ratio))
        results['vk_required'] = vk_required

        # --- 5. Comparar ---
        if float(vk_actual) >= vk_required:
            results['status'] = 'SATURAÇÃO OK'
        else:
            results['status'] = 'SATURAÇÃO CRÍTICA'

        return results

    except Exception as e:
        results['status'] = f'Erro no cálculo: {e}'
        return results

def calculate_sinusoidal_excitation_curve(vk, ik, saturation_level=10):
    """
    Calcula a curva de excitação senoidal para um TC.

    Args:
        vk (float): Tensão de Kneepoint.
        ik (float): Corrente de excitação no ponto de Kneepoint.
        saturation_level (int): Fator para estender a curva na região de saturação.

    Returns:
        tuple: (correntes, tensões) para plotagem.
    """
    # Pontos antes do Kneepoint (região linear)
    currents1 = np.linspace(0, ik, 50)
    voltages1 = (currents1 / ik) * vk

    # Pontos após o Kneepoint (região de saturação)
    currents2 = np.linspace(ik, ik * saturation_level, 100)
    # A curva de saturação é modelada com uma função exponencial suave
    voltages2 = vk + (vk * 0.1) * (1 - np.exp(-(currents2 - ik) / (ik * 2)))

    # Combinar as duas partes
    currents = np.concatenate([currents1, currents2])
    voltages = np.concatenate([voltages1, voltages2])

    return currents, voltages
# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 6 (SATURAÇÃO DE TC) ---
