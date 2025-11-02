# Ficheiro: callbacks/callbacks_tcc.py
# (Atualizado para incluir plotagem de curva de motor)

from dash import Input, Output, State
import numpy as np
import plotly.graph_objects as go
from app import app
from utils import get_tcc_time, generate_motor_curves  # <-- ADICIONA A NOVA FUNÇÃO


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
     State('tcc_fault_current', 'value'),
     # --- [NOVOS STATES DO MOTOR] ---
     State('tcc_motor_enable', 'value'),  # O checklist (é uma lista)
     State('tcc_motor_in', 'value'),
     State('tcc_motor_ip_in', 'value'),
     State('tcc_motor_t_start', 'value'),
     State('tcc_motor_t_locked', 'value')]
)
def plotar_curvas_tcc(n_clicks, r1_type, r1_pickup, r1_tds, r2_type, r2_pickup, r2_tds, fault_current,
                      # --- [NOVOS ARGUMENTOS DO MOTOR] ---
                      motor_enable, motor_in, motor_ip_in, motor_t_start, motor_t_locked):
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
        # --- 1. Plotar Curvas dos Relés (como antes) ---
        p1 = float(r1_pickup);
        td1 = float(r1_tds)
        p2 = float(r2_pickup);
        td2 = float(r2_tds)
        i_fault = float(fault_current)

        min_pickup = min(p1, p2)
        max_pickup = max(p1, p2)

        # (Se o motor for plotado, expande o range do gráfico)
        if 'plot_motor' in motor_enable:
            try:
                min_pickup = min(min_pickup, float(motor_in))
                max_pickup = max(max_pickup, float(motor_in) * float(motor_ip_in))
            except Exception:
                pass  # Ignora se os valores do motor estiverem errados

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

        # --- 2. Plotar CTI (como antes) ---
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

        # --- 3. [NOVO] Plotar Curvas do Motor ---
        # 'motor_enable' é uma lista. Verificamos se 'plot_motor' está nela.
        if 'plot_motor' in motor_enable:
            try:
                # Chama a função do utils.py
                motor_curves = generate_motor_curves(
                    motor_in, motor_ip_in, motor_t_start, motor_t_locked
                )

                # Plotar Curva de Partida (em L)
                fig.add_trace(go.Scatter(
                    x=motor_curves['start_currents'],
                    y=motor_curves['start_times'],
                    mode='lines',
                    line=dict(color='blue', width=2, dash='dash'),
                    name='Curva de Partida do Motor'
                ))

                # Plotar Curva Térmica (I²t)
                fig.add_trace(go.Scatter(
                    x=motor_curves['thermal_currents'],
                    y=motor_curves['thermal_times'],
                    mode='lines',
                    line=dict(color='red', width=2, dash='dashdot'),
                    name='Curva Térmica do Motor (Rotor Bloqueado)'
                ))

            except Exception as e:
                print(f"Erro ao plotar motor: {e}")
                # Não faz nada se os dados do motor estiverem inválidos

        # --- Ajuste Final dos Eixos ---
        # (Esta lógica foi movida de 'plotar_curvas_tcc' para cá para
        # garantir que todos os dados sejam considerados)
        valid_times = [t for t in times_r1 + times_r2 if t != np.inf and t is not None]
        max_time = max(valid_times) if valid_times else 100

        fig.update_xaxes(range=[np.log10(min_pickup * 0.9), np.log10(max_pickup * 110)])
        fig.update_yaxes(range=[np.log10(0.01), np.log10(max_time * 2)])

        return fig, cti_text

    except Exception as e:
        return fig, f"Erro ao plotar TCC: {e}"