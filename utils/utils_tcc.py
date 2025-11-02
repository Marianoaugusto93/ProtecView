# Ficheiro: utils/utils_tcc.py
import numpy as np

# --- Função Auxiliar Módulo 3: Cálculo de Tempo TCC ---
def get_tcc_time(current, pickup, tds, curve_type):
    """
    Calcula o tempo de operação de um relé usando fórmulas IEC ou IEEE.
    """
    try:
        M = current / pickup  # Múltiplo da corrente de pickup

        if M <= 1:  # Se a corrente for menor que o pickup, o relé não atua
            return np.inf  # Retorna "infinito"

        # Constantes k, alpha, B para as curvas
        # Fórmula: t = TDS * [ (k / (M^alpha - 1)) + B ]

        # --- Curvas IEC ---
        if curve_type == 'IEC Standard Inverse':
            k = 0.14
            alpha = 0.02
            B = 0
        elif curve_type == 'IEC Very Inverse':
            k = 13.5
            alpha = 1.0
            B = 0
        elif curve_type == 'IEC Extremely Inverse':
            k = 80.0
            alpha = 2.0
            B = 0

        # --- NOVAS Curvas IEEE C37.112 ---
        elif curve_type == 'IEEE Moderately Inverse':
            k = 0.0515
            alpha = 0.02
            B = 0.114
        elif curve_type == 'IEEE Very Inverse':
            k = 19.61
            alpha = 2.0
            B = 0.491
        elif curve_type == 'IEEE Extremely Inverse':
            k = 28.2
            alpha = 2.0
            B = 0.1217

        else:  # Default para IEC Standard Inverse (caso seguro)
            k = 0.14
            alpha = 0.02
            B = 0

        # Fórmula genérica: t = TDS * [ (k / (M^alpha - 1)) + B ]
        time = tds * ((k / (M ** alpha - 1)) + B)

        return time

    except Exception:
        return np.inf
# --- [FIM] Função de TCC (MODIFICADA) ---


# --- [INÍCIO] NOVAS FUNÇÕES DO MÓDULO 10 (PARTIDA DE MOTOR) ---

def generate_motor_curves(i_nominal, ip_in_ratio, t_start, t_locked):
    """
    Calcula os pontos (x, y) para as curvas de partida e térmica do motor.
    ... (resto da função) ...
    """

    results = {
        'start_currents': [],
        'start_times': [],
        'thermal_currents': [],
        'thermal_times': []
    }

    try:
        # --- 1. Converter inputs ---
        In = float(i_nominal)
        Ip_In = float(ip_in_ratio)
        ts = float(t_start)
        tl = float(t_locked)

        # Corrente de partida (Ip)
        Ip = In * Ip_In

        # --- 2. Gerar Curva de Partida (Starting Curve) ---
        results['start_currents'] = [Ip, Ip, In]
        results['start_times'] = [0.01, ts, ts]  # Começa em 0.01s para plot log

        # --- 3. Gerar Curva Térmica (Locked Rotor / Damage Curve) ---
        k = (Ip ** 2) * tl
        thermal_currents = np.linspace(In * 1.1, Ip * 1.1, 20)
        thermal_times = [k / (i ** 2) for i in thermal_currents]
        results['thermal_currents'] = thermal_currents
        results['thermal_times'] = thermal_times

        return results

    except Exception as e:
        print(f"Erro ao gerar curvas do motor: {e}")
        return results

# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 10 (PARTIDA DE MOTOR) ---