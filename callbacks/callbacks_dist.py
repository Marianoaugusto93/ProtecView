# Ficheiro: callbacks/callbacks_dist.py
from dash import Input, Output, State, no_update
import plotly.graph_objects as go
from app import app
from utils import polar_to_complex

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