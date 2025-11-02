import numpy as np
import plotly.graph_objects as go


# --- Função Auxiliar Módulo 1: Gráficos de Fasores ---
def create_phasor_diagram(phasors, colors, title):
    fig = go.Figure(layout=go.Layout(template="plotly_dark", title=title))
    max_magnitude = 0
    if not phasors:
        return fig

    for i, (label, phasor) in enumerate(phasors.items()):
        magnitude = np.abs(phasor)
        angle_deg = np.rad2deg(np.angle(phasor))

        if magnitude > max_magnitude:
            max_magnitude = magnitude
        if magnitude == 0:
            continue

        fig.add_trace(go.Scatterpolar(
            r=[0, magnitude], theta=[0, angle_deg], mode='lines',
            name=label, line=dict(color=colors[i]), thetaunit='degrees'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[magnitude * 1.1], theta=[angle_deg], mode='text',
            text=[f"<b>{label}</b><br>{magnitude:.2f}∠{angle_deg:.2f}°"],
            textfont=dict(color=colors[i], size=12),
            name=f"{label} (label)", showlegend=False, thetaunit='degrees'
        ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(42, 42, 42, 0.8)',
            radialaxis=dict(visible=True, range=[0, max_magnitude * 1.3], showline=False,
                            gridcolor='rgba(255, 255, 255, 0.3)'),
            angularaxis=dict(direction="clockwise", rotation=0, gridcolor='rgba(255, 255, 255, 0.3)')
        ),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig


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

# --- [INÍCIO] NOVAS FUNÇÕES DO MÓDULO 4 ---

def polar_to_complex(mag, ang_deg):
    """
    Converte uma magnitude e um ângulo (em graus) para um número complexo.
    """
    try:
        rad = np.deg2rad(float(ang_deg))
        return float(mag) * (np.cos(rad) + 1j * np.sin(rad))
    except Exception:
        return 0j


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
    # (Adicionamos um número muito pequeno, 'epsilon', para estabilidade numérica)
    epsilon = 1e-9

    # --- 1. Falta Trifásica (3PH) ---
    # I_3ph = V / Z1
    try:
        i_3ph = v_prefault / (z1 + epsilon)
        results['3ph'] = np.abs(i_3ph)
    except Exception:
        pass  # Mantém 0.0

    # --- 2. Falta Fase-Terra (LG) ---
    # I_lg = 3 * V / (Z1 + Z2 + Z0)
    try:
        z_total_lg = z1 + z2 + z0
        i_lg = (3 * v_prefault) / (z_total_lg + epsilon)
        results['lg'] = np.abs(i_lg)
    except Exception:
        pass  # Mantém 0.0

    # --- 3. Falta Fase-Fase (LL) ---
    # I1 = V / (Z1 + Z2)
    # I_fault (fase B ou C) = I1 * sqrt(3)
    try:
        z_total_ll = z1 + z2
        i_1 = v_prefault / (z_total_ll + epsilon)
        i_ll = i_1 * (np.sqrt(3))  # Magnitude (simplificado)
        results['ll'] = np.abs(i_ll)
    except Exception:
        pass  # Mantém 0.0

    return results
# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 4 ---

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

# No ficheiro: utils.py
# ... (as suas funções anteriores, calculate_ampacity, etc., ficam aqui em cima) ...

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

def generate_differential_curve(pickup, bp1, slope1, bp2, slope2, unrestrained):
    """
    Calcula os pontos (x, y) para a curva de restrição diferencial
    baseada no modelo de múltiplos breakpoints.

    :param pickup: Corrente de pickup (Idif >)
    :param bp1: Breakpoint 1 (Ir >)
    :param slope1: Inclinação 1 (em %)
    :param bp2: Breakpoint 2 (Ir >)
    :param slope2: Inclinação 2 (em %)
    :param unrestrained: Pickup Não Restrito (Idiff >>)
    :return: Duas listas: (lista_ir, lista_iop)
    """

    try:
        # --- 1. Converter inputs ---
        p = float(pickup)
        b1 = float(bp1)
        s1 = float(slope1) / 100.0  # Converte % para decimal
        b2 = float(bp2)
        s2 = float(slope2) / 100.0  # Converte % para decimal
        unres = float(unrestrained)

        # --- 2. Listas de pontos para o gráfico ---
        list_ir = []  # Eixo X (Restrição)
        list_iop = []  # Eixo Y (Operação)

        # Validação de inputs
        if b1 > b2:
            # Garante que breakpoint 1 é menor que breakpoint 2
            b1, b2 = b2, b1

            # --- Ponto 1: Início (Origem) ---
        list_ir.append(0)
        list_iop.append(p)

        # --- Ponto 2: Fim do Pickup / Início Slope1 ---
        list_ir.append(b1)
        list_iop.append(p)

        # --- Ponto 3: Fim do Slope 1 / Início Slope2 ---
        # Iop no breakpoint 2 = Pickup + (Slope1 * (Ir_bp2 - Ir_bp1))
        iop_at_bp2 = p + (s1 * (b2 - b1))

        # Verifica se o Ponto 3 já atingiu o limite "unrestrained"
        if iop_at_bp2 >= unres:
            # A curva atingiu o limite "unrestrained" durante o Slope 1
            # Precisamos encontrar o 'Ir' onde a linha do Slope 1 cruza 'unres'
            # unres = p + s1 * (Ir_cruzamento - b1)
            # (unres - p) / s1 = Ir_cruzamento - b1
            ir_cross = b1 + (unres - p) / (s1 + 1e-9)  # 1e-9 para evitar divisão por zero

            list_ir.append(ir_cross)
            list_iop.append(unres)
            # Adiciona um ponto final horizontal
            list_ir.append(max(ir_cross, b2) * 1.2)  # Ponto final para plotagem
            list_iop.append(unres)
            return list_ir, list_iop  # A curva termina aqui

        # Se não atingiu, adiciona o Ponto 3 normalmente
        list_ir.append(b2)
        list_iop.append(iop_at_bp2)

        # --- Ponto 4: Interseção do Slope 2 com Unrestrained ---
        # Encontra 'Ir' onde a linha do Slope 2 cruza 'unres'
        # unres = iop_at_bp2 + s2 * (Ir_cruzamento - b2)
        # (unres - iop_at_bp2) / s2 = Ir_cruzamento - b2
        ir_cross_2 = b2 + (unres - iop_at_bp2) / (s2 + 1e-9)

        list_ir.append(ir_cross_2)
        list_iop.append(unres)

        # --- Ponto 5: Linha Horizontal Final ---
        list_ir.append(ir_cross_2 * 1.2)  # Ponto final 20% além
        list_iop.append(unres)

        return list_ir, list_iop

    except Exception as e:
        print(f"Erro ao gerar curva diferencial: {e}")
        return [], []

# --- [FIM] NOVAS FUNÇÕES DO MÓDULO 7 (PROTEÇÃO DIFERENCIAL) ---