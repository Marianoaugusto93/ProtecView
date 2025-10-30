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