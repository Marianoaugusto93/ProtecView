from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx, no_update
import numpy as np
import plotly.graph_objects as go

# Importa a app principal
from app import app
# Importa as funções auxiliares
from utils import create_phasor_diagram, get_tcc_time, polar_to_complex, calculate_fault_currents


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
        in_1 = "Fase A Mag:"
        in_2 = "Fase B Mag:"
        in_3 = "Fase C Mag:"
        out_1 = "Sequência Zero (V0): "
        out_2 = "Sequência Positiva (V1): "
        out_3 = "Sequência Negativa (V2): "
        title_in = "Visualização de Fasores (Entrada: Fases)"
        title_out = "Visualização de Fasores (Saída: Simétricos)"
    else:  # sym-to-phase
        in_1 = "Seq. Zero (V0) Mag:"
        in_2 = "Seq. Positiva (V1) Mag:"
        in_3 = "Seq. Negativa (V2) Mag:"
        out_1 = "Fase A (Va): "
        out_2 = "Fase B (Vb): "
        out_3 = "Fase C (Vc): "
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
    fig_vazia = go.Figure(
        layout=go.Layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'))

    if n_clicks is None or n_clicks == 0:
        return "Clique em 'Calcular'...", "", "", fig_vazia, fig_vazia

    try:
        m1 = float(mag1);
        a1 = float(ang1)
        m2 = float(mag2);
        a2 = float(ang2)
        m3 = float(mag3);
        a3 = float(ang3)

        V_in_1 = polar_to_complex(m1, a1)
        V_in_2 = polar_to_complex(m2, a2)
        V_in_3 = polar_to_complex(m3, a3)

        a = np.exp(1j * 2 * np.pi / 3)

        if direction == 'phase-to-sym':
            V_a = V_in_1;
            V_b = V_in_2;
            V_c = V_in_3
            V_out_1 = (1 / 3) * (V_a + V_b + V_c)  # V0
            V_out_2 = (1 / 3) * (V_a + a * V_b + (a ** 2) * V_c)  # V1
            V_out_3 = (1 / 3) * (V_a + (a ** 2) * V_b + a * V_c)  # V2
            in_labels = {"A": V_a, "B": V_b, "C": V_c}
            in_colors = ["#ff0d57", "#00b200", "#009cff"]
            out_labels = {"0": V_out_1, "1": V_out_2, "2": V_out_3}
            out_colors = ["#888888", "#ff0d57", "#00b200"]
        else:  # direction == 'sym-to-phase'
            V_0 = V_in_1;
            V_1 = V_in_2;
            V_2 = V_in_3
            V_out_1 = V_0 + V_1 + V_2  # Va
            V_out_2 = V_0 + (a ** 2) * V_1 + a * V_2  # Vb
            V_out_3 = V_0 + a * V_1 + (a ** 2) * V_2  # Vc
            in_labels = {"0": V_0, "1": V_1, "2": V_2}
            in_colors = ["#888888", "#ff0d57", "#00b200"]
            out_labels = {"A": V_out_1, "B": V_out_2, "C": V_out_3}
            out_colors = ["#ff0d57", "#00b200", "#009cff"]

        def to_polar_str(complex_val):
            mag = np.abs(complex_val)
            ang = np.rad2deg(np.angle(complex_val))
            return f"{mag:.2f} ∠ {ang:.2f}°"

        out_1_str = to_polar_str(V_out_1)
        out_2_str = to_polar_str(V_out_2)
        out_3_str = to_polar_str(V_out_3)

        fig_in = create_phasor_diagram(in_labels, in_colors, "")
        fig_out = create_phasor_diagram(out_labels, out_colors, "")

        return out_1_str, out_2_str, out_3_str, fig_in, fig_out

    except Exception as e:
        return f"Erro: {e}", "", "", fig_vazia, fig_vazia


# --- MÓDULO 2: Proteção de Distância (ESTÁTICO - Revertido) ---

# --- Callback 2.1: Atualizar Rótulos (Labels) da Zona 1 ---
@app.callback(
    [Output('line1_z1_label1', 'children'),
     Output('line1_z1_label2', 'children')],
    [Input('line1_z1_type', 'value')]
)
def update_zone1_labels(zone_type):
    if zone_type == 'mho':
        return "Magnitude (Ω):", " Ângulo (°):"
    elif zone_type == 'quad':
        return "Alcance X (Ω):", " Alcance R (Ω):"
    return no_update, no_update  # Adicionado para segurança


# --- Callback 2.2: Atualizar Rótulos (Labels) da Zona 2 ---
@app.callback(
    [Output('line1_z2_label1', 'children'),
     Output('line1_z2_label2', 'children')],
    [Input('line1_z2_type', 'value')]
)
def update_zone2_labels(zone_type):
    if zone_type == 'mho':
        return "Magnitude (Ω):", " Ângulo (°):"
    elif zone_type == 'quad':
        return "Alcance X (Ω):", " Alcance R (Ω):"
    return no_update, no_update  # Adicionado para segurança


# --- Callback 2.3: Plotar o Gráfico (Estático) ---
@app.callback(
    Output('distance-plot-graph', 'figure'),
    [Input('btn_plot_zones', 'n_clicks')],
    [State('line1_imp', 'value'), State('line1_ang', 'value'),
     State('line1_z1_type', 'value'),
     State('line1_z1_imp', 'value'), State('line1_z1_ang', 'value'),
     State('line1_z2_type', 'value'),
     State('line1_z2_imp', 'value'), State('line1_z2_ang', 'value')]
)
def plotar_zonas_de_distancia(n_clicks, line_imp, line_ang,
                              z1_type, z1_in1, z1_in2,
                              z2_type, z2_in1, z2_in2):
    fig = go.Figure(
        layout=go.Layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'))
    if n_clicks is None or n_clicks == 0:
        fig.update_layout(title="Clique em 'Plotar Zonas' para ver o gráfico R-X")
        return fig

    try:
        # --- A. Converter inputs da Linha ---
        l1_imp = float(line_imp);
        l1_ang_deg = float(line_ang)
        Z_l1 = polar_to_complex(l1_imp, l1_ang_deg)
        R_l1, X_l1 = Z_l1.real, Z_l1.imag

        fig.add_trace(go.Scatter(
            x=[0, R_l1], y=[0, X_l1], mode='lines+markers',
            name=f'Linha 1: {l1_imp}Ω ∠{l1_ang_deg}°', line=dict(color='white', width=3)
        ))

        # --- B. Processar e Plotar Zona 1 ---
        z1_in1_val = float(z1_in1)
        z1_in2_val = float(z1_in2)

        if z1_type == 'mho':
            Z_mho_z1 = polar_to_complex(z1_in1_val, z1_in2_val)
            R_z1, X_z1 = Z_mho_z1.real, Z_mho_z1.imag
            center_x_z1 = R_z1 / 2;
            center_y_z1 = X_z1 / 2;
            radius_z1 = z1_in1_val / 2

            fig.add_shape(type="circle", xref="x", yref="y",
                          x0=center_x_z1 - radius_z1, y0=center_y_z1 - radius_z1,
                          x1=center_x_z1 + radius_z1, y1=center_y_z1 + radius_z1,
                          line_color="#009cff", fillcolor="rgba(0, 156, 255, 0.1)", name="Zona 1"
                          )

        elif z1_type == 'quad':
            X_reach_z1 = z1_in1_val
            R_reach_z1 = z1_in2_val
            fig.add_trace(go.Scatter(
                x=[0, R_reach_z1, R_reach_z1, 0, 0],  # Coordenadas X
                y=[0, 0, X_reach_z1, X_reach_z1, 0],  # Coordenadas Y
                fill="toself",
                fillcolor="rgba(0, 156, 255, 0.1)",
                line_color="#009cff",
                name="Zona 1 (Quad)"
            ))

        # --- C. Processar e Plotar Zona 2 ---
        z2_in1_val = float(z2_in1)
        z2_in2_val = float(z2_in2)

        if z2_type == 'mho':
            Z_mho_z2 = polar_to_complex(z2_in1_val, z2_in2_val)
            R_z2, X_z2 = Z_mho_z2.real, Z_mho_z2.imag
            center_x_z2 = R_z2 / 2;
            center_y_z2 = X_z2 / 2;
            radius_z2 = z2_in1_val / 2

            fig.add_shape(type="circle", xref="x", yref="y",
                          x0=center_x_z2 - radius_z2, y0=center_y_z2 - radius_z2,
                          x1=center_x_z2 + radius_z2, y1=center_y_z2 + radius_z2,
                          line_color="#ff0d57", fillcolor="rgba(255, 13, 87, 0.1)", name="Zona 2"
                          )

        elif z2_type == 'quad':
            X_reach_z2 = z2_in1_val
            R_reach_z2 = z2_in2_val
            fig.add_trace(go.Scatter(
                x=[0, R_reach_z2, R_reach_z2, 0, 0],
                y=[0, 0, X_reach_z2, X_reach_z2, 0],
                fill="toself",
                fillcolor="rgba(255, 13, 87, 0.1)",
                line_color="#ff0d57",
                name="Zona 2 (Quad)"
            ))

        # --- D. Configurar o Layout do Gráfico R-X ---
        fig.update_layout(
            title="Diagrama R-X de Proteção de Distância",
            xaxis_title="Resistência (R) Ω", yaxis_title="Reatância (X) Ω",
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)'),
            yaxis=dict(scaleanchor="x", scaleratio=1, gridcolor='rgba(255, 255, 255, 0.3)'),
            showlegend=False
        )
        return fig

    except Exception as e:
        fig.update_layout(title=f"Erro ao plotar: {e}")
        return fig


# --- MÓDULO 3: Curvas TCC ---
@app.callback(
    [Output('tcc-graph', 'figure'),
     Output('tcc-cti-output', 'children')],
    [Input('btn_plot_tcc', 'n_clicks')],
    [State('tcc_r1_type', 'value'),
     State('tcc_r1_pickup', 'value'),
     State('tcc_r1_tds', 'value'),
     State('tcc_r2_type', 'value'),
     State('tcc_r2_pickup', 'value'),
     State('tcc_r2_tds', 'value'),
     State('tcc_fault_current', 'value')]
)
def plotar_curvas_tcc(n_clicks, r1_type, r1_pickup, r1_tds, r2_type, r2_pickup, r2_tds, fault_current):
    fig = go.Figure(layout=go.Layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_type="log", yaxis_type="log",
        title="Curvas TCC de Sobrecorrente",
        xaxis_title="Corrente (A)",
        yaxis_title="Tempo (s)"
    ))
    cti_text = "Clique em 'Plotar' para calcular o CTI."

    if n_clicks is None or n_clicks == 0:
        return fig, cti_text

    try:
        p1 = float(r1_pickup);
        td1 = float(r1_tds)
        p2 = float(r2_pickup);
        td2 = float(r2_tds)
        i_fault = float(fault_current)

        min_pickup = min(p1, p2);
        max_pickup = max(p1, p2)
        currents = np.logspace(np.log10(min_pickup * 1.05), np.log10(max_pickup * 100), num=200)

        times_r1 = [get_tcc_time(c, p1, td1, r1_type) for c in currents]
        times_r2 = [get_tcc_time(c, p2, td2, r2_type) for c in currents]

        fig.add_trace(go.Scatter(
            x=currents, y=times_r1, mode='lines',
            name=f"Relé 1 ({r1_type})", line=dict(color='#ff9900')
        ))
        fig.add_trace(go.Scatter(
            x=currents, y=times_r2, mode='lines',
            name=f"Relé 2 ({r2_type})", line=dict(color='#00cc00')
        ))

        t1_fault = get_tcc_time(i_fault, p1, td1, r1_type)
        t2_fault = get_tcc_time(i_fault, p2, td2, r2_type)

        if t1_fault != np.inf and t2_fault != np.inf:
            cti = t1_fault - t2_fault
            fig.add_shape(type="line",
                          x0=i_fault, y0=0.01, x1=i_fault, y1=max(t1_fault, t2_fault) * 1.5,
                          line=dict(color="white", width=1, dash="dot")
                          )
            fig.add_trace(go.Scatter(
                x=[i_fault, i_fault], y=[t1_fault, t2_fault],
                mode='markers+text',
                marker=dict(color=['#ff9900', '#00cc00'], size=10),
                text=[f"R1: {t1_fault:.3f}s", f"R2: {t2_fault:.3f}s"],
                textposition="top right",
                name="Pontos de Operação",
                textfont=dict(color='#ffffff')
            ))
            cti_text = f"CTI em {i_fault}A: {cti:.3f} s (R1: {t1_fault:.3f}s | R2: {t2_fault:.3f}s)"
        else:
            cti_text = f"Corrente de falta {i_fault}A é menor que o pickup de um dos relés. Sem coordenação."

        valid_times = [t for t in times_r1 + times_r2 if t != np.inf]
        max_time = max(valid_times) if valid_times else 100

        fig.update_xaxes(range=[np.log10(min_pickup * 0.9), np.log10(max_pickup * 110)])
        fig.update_yaxes(range=[np.log10(0.01), np.log10(max_time * 2)])

        return fig, cti_text
    except Exception as e:
        return fig, f"Erro ao plotar TCC: {e}"


# --- MÓDULO 4: Cálculo de Faltas ---
@app.callback(
    [Output('out_fault_3ph', 'children'),
     Output('out_fault_lg', 'children'),
     Output('out_fault_ll', 'children')],
    [Input('btn_calc_fault', 'n_clicks')],
    [State('fault_v_mag', 'value'), State('fault_v_ang', 'value'),
     State('fault_z1_mag', 'value'), State('fault_z1_ang', 'value'),
     State('fault_z2_mag', 'value'), State('fault_z2_ang', 'value'),
     State('fault_z0_mag', 'value'), State('fault_z0_ang', 'value')]
)
def handle_fault_calculation(n_clicks,
                             v_mag, v_ang,
                             z1_mag, z1_ang,
                             z2_mag, z2_ang,
                             z0_mag, z0_ang):
    if n_clicks is None or n_clicks == 0:
        return "Clique em 'Calcular'", "Clique em 'Calcular'", "Clique em 'Calcular'"

    try:
        V_pu = polar_to_complex(v_mag, v_ang)
        Z1 = polar_to_complex(z1_mag, z1_ang)
        Z2 = polar_to_complex(z2_mag, z2_ang)
        Z0 = polar_to_complex(z0_mag, z0_ang)

        results = calculate_fault_currents(V_pu, Z1, Z2, Z0)

        out_3ph = f"{results['3ph']:.3f} p.u."
        out_lg = f"{results['lg']:.3f} p.u."
        out_ll = f"{results['ll']:.3f} p.u."

        return out_3ph, out_lg, out_ll

    except Exception as e:
        error_msg = f"Erro: {e}"
        return error_msg, error_msg, error_msg