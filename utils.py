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