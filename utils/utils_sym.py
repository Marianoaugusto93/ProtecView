# Ficheiro: utils/utils_sym.py
# (Removido template="plotly_dark" da função)

import numpy as np
import plotly.graph_objects as go


def create_phasor_diagram(phasors, colors, title):
    """
    Cria um diagrama de fasores polar usando Plotly.
    """
    # [CORREÇÃO] Removido template="plotly_dark"
    fig = go.Figure(layout=go.Layout(title=title))

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
        # [CORREÇÃO] Removido plot_bgcolor, paper_bgcolor
        # (O CSS vai tratar disto)
        polar=dict(
            # O CSS vai tratar das cores da grelha e do fundo
            radialaxis=dict(visible=True, range=[0, max_magnitude * 1.3], showline=False),
            angularaxis=dict(direction="clockwise", rotation=0)
        ),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig