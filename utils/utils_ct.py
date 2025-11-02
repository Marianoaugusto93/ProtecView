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

# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 6 (SATURAÇÃO DE TC) ---
