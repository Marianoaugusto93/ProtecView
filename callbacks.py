from dash import Input, Output, State
import numpy as np
import plotly.graph_objects as go

# Importa a app principal
from app import app
# Importa as funções auxiliares
from utils import create_phasor_diagram, get_tcc_time


# --- Callback MÓDULO 1: Componentes Simétricos ---
@app.callback(
    [Output('out_v0', 'children'),
     Output('out_v1', 'children'),
     Output('out_v2', 'children'),
     Output('phasor-graph-phase', 'figure'),
     Output('phasor-graph-symmetrical', 'figure')],
    [Input('btn_calcular_sym', 'n_clicks')],
    [State('mag_a', 'value'), State('ang_a', 'value'),
     State('mag_b', 'value'), State('ang_b', 'value'),
     State('mag_c', 'value'), State('ang_c', 'value')]
)
def calcular_componentes(n_clicks, mag_a, ang_a, mag_b, ang_b, mag_c, ang_c):
    fig_vazia = go.Figure(
        layout=go.Layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'))
    if n_clicks == 0:
        return "Clique em 'Calcular'...", "", "", fig_vazia, fig_vazia

    try:
        v_a_mag = float(mag_a);
        v_a_ang_deg = float(ang_a)
        v_b_mag = float(mag_b);
        v_b_ang_deg = float(ang_b)
        v_c_mag = float(mag_c);
        v_c_ang_deg = float(ang_c)

        V_a = v_a_mag * (np.cos(np.deg2rad(v_a_ang_deg)) + 1j * np.sin(np.deg2rad(v_a_ang_deg)))
        V_b = v_b_mag * (np.cos(np.deg2rad(v_b_ang_deg)) + 1j * np.sin(np.deg2rad(v_b_ang_deg)))
        V_c = v_c_mag * (np.cos(np.deg2rad(v_c_ang_deg)) + 1j * np.sin(np.deg2rad(v_c_ang_deg)))

        a = np.exp(1j * 2 * np.pi / 3)
        V_0 = (1 / 3) * (V_a + V_b + V_c);
        V_1 = (1 / 3) * (V_a + a * V_b + (a ** 2) * V_c);
        V_2 = (1 / 3) * (V_a + (a ** 2) * V_b + a * V_c)

        out_v0_str = f"{np.abs(V_0):.2f} ∠ {np.rad2deg(np.angle(V_0)):.2f}°"
        out_v1_str = f"{np.abs(V_1):.2f} ∠ {np.rad2deg(np.angle(V_1)):.2f}°"
        out_v2_str = f"{np.abs(V_2):.2f} ∠ {np.rad2deg(np.angle(V_2)):.2f}°"

        fasores_fase = {"A": V_a, "B": V_b, "C": V_c};
        cores_fase = ["#ff0d57", "#00b200", "#009cff"]
        fig_fase = create_phasor_diagram(fasores_fase, cores_fase, "Componentes de Fase")
        fasores_simetricos = {"0": V_0, "1": V_1, "2": V_2};
        cores_simetricos = ["#888888", "#ff0d57", "#00b200"]
        fig_simetrica = create_phasor_diagram(fasores_simetricos, cores_simetricos, "Componentes Simétricos")

        return out_v0_str, out_v1_str, out_v2_str, fig_fase, fig_simetrica
    except Exception as e:
        return f"Erro: {e}", "", "", fig_vazia, fig_vazia


# --- Callback MÓDULO 2: Proteção de Distância ---
@app.callback(
    Output('distance-plot-graph', 'figure'),
    [Input('btn_plot_zones', 'n_clicks')],
    [State('line1_imp', 'value'), State('line1_ang', 'value'),
     State('line1_z1_imp', 'value'), State('line1_z1_ang', 'value'),
     State('line1_z2_imp', 'value'), State('line1_z2_ang', 'value')]
)
def plotar_zonas_de_distancia(n_clicks, line_imp, line_ang, z1_imp, z1_ang, z2_imp, z2_ang):
    fig = go.Figure(
        layout=go.Layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'))
    if n_clicks == 0:
        fig.update_layout(title="Clique em 'Plotar Zonas' para ver o gráfico R-X")
        return fig

    try:
        l1_imp = float(line_imp);
        l1_ang_deg = float(line_ang)
        z1_imp = float(z1_imp);
        z1_ang_deg = float(z1_ang)
        z2_imp = float(z2_imp);
        z2_ang_deg = float(z2_ang)

        def polar_para_cart(mag, ang_deg):
            rad = np.deg2rad(ang_deg);
            R = mag * np.cos(rad);
            X = mag * np.sin(rad);
            return R, X

        R_l1, X_l1 = polar_para_cart(l1_imp, l1_ang_deg)
        R_z1, X_z1 = polar_para_cart(z1_imp, z1_ang_deg)
        R_z2, X_z2 = polar_para_cart(z2_imp, z2_ang_deg)

        fig.add_trace(go.Scatter(
            x=[0, R_l1], y=[0, X_l1], mode='lines+markers',
            name=f'Linha 1: {l1_imp}Ω ∠{l1_ang_deg}°', line=dict(color='white', width=3)
        ))

        center_x_z1 = R_z1 / 2;
        center_y_z1 = X_z1 / 2;
        radius_z1 = z1_imp / 2
        fig.add_shape(type="circle", xref="x", yref="y",
                      x0=center_x_z1 - radius_z1, y0=center_y_z1 - radius_z1,
                      x1=center_x_z1 + radius_z1, y1=center_y_z1 + radius_z1,
                      line_color="#009cff", fillcolor="rgba(0, 156, 255, 0.1)", name="Zona 1"
                      )

        center_x_z2 = R_z2 / 2;
        center_y_z2 = X_z2 / 2;
        radius_z2 = z2_imp / 2
        fig.add_shape(type="circle", xref="x", yref="y",
                      x0=center_x_z2 - radius_z2, y0=center_y_z2 - radius_z2,
                      x1=center_x_z2 + radius_z2, y1=center_y_z2 + radius_z2,
                      line_color="#ff0d57", fillcolor="rgba(255, 13, 87, 0.1)", name="Zona 2"
                      )

        fig.update_layout(
            title="Diagrama R-X de Proteção de Distância",
            xaxis_title="Resistência (R) Ω", yaxis_title="Reatância (X) Ω",
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)'),
            yaxis=dict(scaleanchor="x", scaleratio=1, gridcolor='rgba(255, 255, 255, 0.3)'),
        )
        max_range = max(radius_z2 * 1.5, center_y_z2 + radius_z2 * 1.1)
        fig.update_xaxes(range=[-radius_z2 * 0.5, max_range])
        fig.update_yaxes(range=[-radius_z2 * 0.5, max_range])
        return fig
    except Exception as e:
        fig.update_layout(title=f"Erro ao plotar: {e}")
        return fig


# --- Callback MÓDULO 3: Curvas TCC ---
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
    if n_clicks == 0:
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
            name=f"Relé 1 ({r1_type})", line=dict(color='#ff9900')  # Laranja
        ))
        fig.add_trace(go.Scatter(
            x=currents, y=times_r2, mode='lines',
            name=f"Relé 2 ({r2_type})", line=dict(color='#00cc00')  # Verde
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