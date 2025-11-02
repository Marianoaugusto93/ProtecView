# Ficheiro: callbacks/callbacks_sym.py
from dash import Input, Output, State, no_update
import numpy as np
import plotly.graph_objects as go
from app import app

from utils.utils_sym import create_phasor_diagram
from utils.utils_common import polar_to_complex
# --- MÓDULO 1: Componentes Simétricos ---

# --- Callback 1.1: Atualizar Rótulos (Labels) ---
@app.callback(
    [Output('sym_label_in_1', 'children'),
     Output('sym_label_in_2', 'children'),
     Output('sym_label_in_3', 'children'),
     Output('sym_label_out_1', 'children'),
     Output('sym_label_out_2', 'children'),
     Output('sym_label_out_3', 'children'),
     Output('sym_graph_title_in', 'children'),
     Output('sym_graph_title_out', 'children')],
    [Input('sym-direction-dropdown', 'value')]
)
def update_sym_labels(direction):
    if direction == 'phase-to-sym':
        in_1 = "Fase A Mag:"; in_2 = "Fase B Mag:"; in_3 = "Fase C Mag:"
        out_1 = "Sequência Zero (V0): "; out_2 = "Sequência Positiva (V1): "; out_3 = "Sequência Negativa (V2): "
        title_in = "Visualização de Fasores (Entrada: Fases)"
        title_out = "Visualização de Fasores (Saída: Simétricos)"
    else:  # sym-to-phase
        in_1 = "Seq. Zero (V0) Mag:"; in_2 = "Seq. Positiva (V1) Mag:"; in_3 = "Seq. Negativa (V2) Mag:"
        out_1 = "Fase A (Va): "; out_2 = "Fase B (Vb): "; out_3 = "Fase C (Vc): "
        title_in = "Visualização de Fasores (Entrada: Simétricos)"
        title_out = "Visualização de Fasores (Saída: Fases)"
    return in_1, in_2, in_3, out_1, out_2, out_3, title_in, title_out

# --- Callback 1.2: Cálculo Bi-direcional ---
@app.callback(
    [Output('sym_out_1', 'children'),
     Output('sym_out_2', 'children'),
     Output('sym_out_3', 'children'),
     Output('sym_graph_in', 'figure'),
     Output('sym_graph_out', 'figure')],
    [Input('btn_calcular_sym', 'n_clicks')],
    [State('sym-direction-dropdown', 'value'),
     State('sym_in_mag_1', 'value'), State('sym_in_ang_1', 'value'),
     State('sym_in_mag_2', 'value'), State('sym_in_ang_2', 'value'),
     State('sym_in_mag_3', 'value'), State('sym_in_ang_3', 'value')]
)
def calcular_componentes_bidirecional(n_clicks, direction,
                                      mag1, ang1, mag2, ang2, mag3, ang3):
    fig_vazia = go.Figure(layout=go.Layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'))
    if n_clicks is None or n_clicks == 0:
        return "Clique em 'Calcular'...", "", "", fig_vazia, fig_vazia
    try:
        m1 = float(mag1); a1 = float(ang1)
        m2 = float(mag2); a2 = float(ang2)
        m3 = float(mag3); a3 = float(ang3)
        V_in_1 = polar_to_complex(m1, a1); V_in_2 = polar_to_complex(m2, a2); V_in_3 = polar_to_complex(m3, a3)
        a = np.exp(1j * 2 * np.pi / 3)
        if direction == 'phase-to-sym':
            V_a = V_in_1; V_b = V_in_2; V_c = V_in_3
            V_out_1 = (1 / 3) * (V_a + V_b + V_c); V_out_2 = (1 / 3) * (V_a + a * V_b + (a ** 2) * V_c); V_out_3 = (1 / 3) * (V_a + (a ** 2) * V_b + a * V_c)
            in_labels = {"A": V_a, "B": V_b, "C": V_c}; in_colors = ["#ff0d57", "#00b200", "#009cff"]
            out_labels = {"0": V_out_1, "1": V_out_2, "2": V_out_3}; out_colors = ["#888888", "#ff0d57", "#00b200"]
        else:
            V_0 = V_in_1; V_1 = V_in_2; V_2 = V_in_3
            V_out_1 = V_0 + V_1 + V_2; V_out_2 = V_0 + (a ** 2) * V_1 + a * V_2; V_out_3 = V_0 + a * V_1 + (a ** 2) * V_2
            in_labels = {"0": V_0, "1": V_1, "2": V_2}; in_colors = ["#888888", "#ff0d57", "#00b200"]
            out_labels = {"A": V_out_1, "B": V_out_2, "C": V_out_3}; out_colors = ["#ff0d57", "#00b200", "#009cff"]
        def to_polar_str(complex_val):
            mag = np.abs(complex_val); ang = np.rad2deg(np.angle(complex_val)); return f"{mag:.2f} ∠ {ang:.2f}°"
        out_1_str = to_polar_str(V_out_1); out_2_str = to_polar_str(V_out_2); out_3_str = to_polar_str(V_out_3)
        fig_in = create_phasor_diagram(in_labels, in_colors, ""); fig_out = create_phasor_diagram(out_labels, out_colors, "")
        return out_1_str, out_2_str, out_3_str, fig_in, fig_out
    except Exception as e:
        return f"Erro: {e}", "", "", fig_vazia, fig_vazia