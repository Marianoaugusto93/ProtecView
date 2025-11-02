# Ficheiro: utils/utils_ampacity.py
import numpy as np

# --- [INÍCIO] NOVAS FUNÇÕES DO MÓDULO 5 (AMPACIDADE) ---

# Tabela Fator de Correção de Temperatura (Exemplo baseado na IEC 60364-5-52, Tabela B.52.14)
TEMP_FACTORS = {
    'pvc': {  # Para PVC (70°C)
        10: 1.22, 15: 1.17, 20: 1.12, 25: 1.06, 30: 1.00,
        35: 0.94, 40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61, 60: 0.50
    },
    'xlpe_epr': {  # Para XLPE/EPR (90°C)
        10: 1.15, 15: 1.12, 20: 1.08, 25: 1.04, 30: 1.00,
        35: 0.96, 40: 0.91, 45: 0.87, 50: 0.82, 55: 0.76, 60: 0.71,
        65: 0.65, 70: 0.58, 75: 0.50, 80: 0.41
    }
}

# Tabela Fator de Correção de Agrupamento (Exemplo baseado na IEC 60364-5-52, Tabela B.52.17)
# (Assumindo cabos multipolares em feixe ou camada única)
GROUPING_FACTORS = {
    1: 1.00,  # 1 circuito
    2: 0.80,  # 2 circuitos
    3: 0.70,  # 3 circuitos
    4: 0.65,  # 4 circuitos
    5: 0.60,  # 5 circuitos (adicionamos mais alguns)
    6: 0.57,  # 6 circuitos
    7: 0.54,  # 7 circuitos
    8: 0.52,  # 8 circuitos
    9: 0.50  # 9 circuitos
}


def get_temp_correction_factor(insulation_type, temp):
    """
    Encontra o fator de correção de temperatura mais próximo da tabela.
    """
    if temp < 10: return TEMP_FACTORS[insulation_type].get(10)
    if temp > (60 if insulation_type == 'pvc' else 80):
        return TEMP_FACTORS[insulation_type].get(60 if insulation_type == 'pvc' else 80)

    # Arredonda a temperatura para o múltiplo de 5 mais próximo
    rounded_temp = int(5 * round(temp / 5))
    return TEMP_FACTORS[insulation_type].get(rounded_temp, 1.0)  # Retorna 1.0 se não encontrar


def get_grouping_correction_factor(num_circuits):
    """
    Encontra o fator de correção de agrupamento.
    """
    # Se o número for maior que a tabela, usa o último valor (o pior caso)
    if num_circuits > 9:
        return GROUPING_FACTORS[9]

    return GROUPING_FACTORS.get(num_circuits, 1.0)  # Retorna 1.0 se não encontrar (ex: 0)


def calculate_ampacity(base_current, f_temp, f_group):
    """
    Calcula a ampacidade corrigida final.
    """
    try:
        corrected_ampacity = float(base_current) * f_temp * f_group
        return corrected_ampacity
    except Exception:
        return 0.0

# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 5 (AMPACIDADE) ---

# --- [INÍCIO] NOVAS FUNÇÕES DO MÓDULO 9 (Dimensionamento de Cabos) ---

def calculate_voltage_drop(load_current, length_km, r_ohm_km, x_ohm_km, cos_phi, system_voltage_v):
    """
    Calcula a queda de tensão (VD) em Volts e percentual.
    Fórmula para sistema trifásico (assumido).
    """
    results = {
        'vd_volts': 0.0,
        'vd_percent': 0.0,
        'status': 'OK'
    }

    try:
        # Inputs
        I = float(load_current)
        L = float(length_km)
        R = float(r_ohm_km)
        X = float(x_ohm_km)
        cos_phi = float(cos_phi)
        V_linha = float(system_voltage_v)

        # Calcula o sin(phi)
        sin_phi = np.sqrt(1 - cos_phi ** 2)

        # Fórmula da Queda de Tensão Trifásica (em Volts)
        # VD (linha) = sqrt(3) * I * L * (R * cos(phi) + X * sin(phi))
        vd_volts = np.sqrt(3) * I * L * (R * cos_phi + X * sin_phi)
        results['vd_volts'] = vd_volts

        # Queda de Tensão Percentual
        vd_percent = (vd_volts / V_linha) * 100.0
        results['vd_percent'] = vd_percent

        return results

    except Exception as e:
        print(f"Erro ao calcular VD: {e}")
        return results


def check_short_circuit_withstand(fault_current_a, fault_time_s, cross_section_mm2, k_material):
    """
    Verifica a suportabilidade térmica de curto-circuito (I²t).
    Fórmula: (K * S)² >= (I_fault² * t)
    """
    results = {
        'fault_energy_a2s': 0.0,
        'cable_withstand_a2s': 0.0,
        'status': 'Erro'  # 'OK' ou 'FALHA'
    }

    try:
        # --- 1. Calcular a Energia da Falta (I²t) ---
        I_fault = float(fault_current_a)
        t = float(fault_time_s)
        fault_energy = (I_fault ** 2) * t
        results['fault_energy_a2s'] = fault_energy

        # --- 2. Calcular a Suportabilidade do Cabo (K²S²) ---
        K = float(k_material)
        S = float(cross_section_mm2)
        cable_withstand = (K ** 2) * (S ** 2)
        results['cable_withstand_a2s'] = cable_withstand

        # --- 3. Comparar ---
        if cable_withstand >= fault_energy:
            results['status'] = 'OK'
        else:
            results['status'] = 'FALHA (Cabo subdimensionado para curto)'

        return results

    except Exception as e:
        print(f"Erro ao calcular I²t: {e}")
        results['status'] = f"Erro: {e}"
        return results

# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 9 (Dimensionamento de Cabos) ---

