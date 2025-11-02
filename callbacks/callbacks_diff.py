# Ficheiro: callbacks/callbacks_diff.py
# (Com lógica de plotagem de preenchimento azul corrigida)

from dash import Input, Output, State
import plotly.graph_objects as go
from app import app
from utils import generate_differential_curve  # Importa a nossa função do utils.py
import numpy as np


# --- MÓDULO 7: Proteção Diferencial (87) ---
@app.callback(
    Output('diff_graph', 'figure'),
    [Input('btn_plot_diff', 'n_clicks')],
    [State('diff_pickup', 'value'),
     State('diff_bp1', 'value'),
     State('diff_slope1', 'value'),
     State('diff_bp2', 'value'),
     State('diff_slope2', 'value'),
     State('diff_unrestrained', 'value'),
     State('diff_test_iop', 'value'),
     State('diff_test_ir', 'value')]
)
def plot_differential_curve(n_clicks, pickup_str, bp1_str, slope1_str, bp2_str, slope2_str, unrestrained_str,
                            test_iop_str, test_ir_str):
    # Cria um gráfico base escuro
    fig = go.Figure(layout=go.Layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title="Curva de Restrição Diferencial (Iop vs Ir)",
        xaxis_title="Corrente de Restrição (Ir) [p.u.]",
        yaxis_title="Corrente de Operação (Iop) [p.u.]"
    ))

    if n_clicks is None or n_clicks == 0:
        fig.update_layout(title="Insira as definições do relé e clique em 'Plotar'")
        return fig

    try:
        # --- 1. Converter inputs para números ---
        p = float(pickup_str)
        b1 = float(bp1_str)
        s1 = float(slope1_str) / 100.0
        b2 = float(bp2_str)
        s2 = float(slope2_str) / 100.0
        unres = float(unrestrained_str)
        test_iop = float(test_iop_str)
        test_ir = float(test_ir_str)

        # --- 2. Gerar os pontos da curva de restrição (do utils.py) ---
        list_ir, list_iop = generate_differential_curve(p, b1, float(slope1_str), b2, float(slope2_str), unres)

        if not list_ir:  # Se a função utils falhar
            raise Exception("Falha ao gerar pontos da curva.")

        # --- 3. Determinar limites dinâmicos dos eixos ---
        # (Usamos list_ir[-1] que é o ponto final horizontal da curva)
        max_x_axis = max(list_ir[-1], test_ir, 1.0) * 1.1  # 10% de margem
        max_y_axis = max(list_iop[-1], test_iop, 1.0) * 1.2  # 20% de margem

        # --- 4. [CORREÇÃO] Estender a curva até ao limite do gráfico (max_x_axis) ---
        # Copia os pontos da curva base
        curve_ir_extended = list(list_ir)
        curve_iop_extended = list(list_iop)

        # Se o eixo X for maior que o fim da curva, estende a linha horizontal
        if max_x_axis > curve_ir_extended[-1]:
            curve_ir_extended.append(max_x_axis)
            curve_iop_extended.append(unres)  # Mantém a altura horizontal

        # --- 5. Plotar a "Zona de Operação" (Vermelha) ---
        # Usa a curva estendida para desenhar a área
        op_zone_ir = curve_ir_extended + [max_x_axis, 0, 0]
        op_zone_iop = curve_iop_extended + [max_y_axis, max_y_axis, curve_iop_extended[0]]

        fig.add_trace(go.Scatter(
            x=op_zone_ir,
            y=op_zone_iop,
            fill='toself',
            mode='none',
            fillcolor='rgba(255, 50, 50, 0.2)',  # Vermelho semi-transparente
            name='Zona de Operação'
        ))

        # --- 6. Plotar a "Zona de Bloqueio" (Azul) ---
        # Usa a mesma curva ESTENDIDA para o preenchimento azul
        fig.add_trace(go.Scatter(
            x=curve_ir_extended,  # <--- USA A LISTA ESTENDIDA
            y=curve_iop_extended,  # <--- USA A LISTA ESTENDIDA
            fill='tozeroy',
            mode='lines',
            line=dict(color='cyan', width=3),
            name='Curva de Restrição',
            fillcolor='rgba(0, 156, 255, 0.3)'  # Azul semi-transparente
        ))

        # --- 7. Verificar e Plotar o Ponto de Teste ---
        iop_limite_no_ponto = 0
        if test_ir < 0: test_ir = 0

        if test_iop >= unres:
            iop_limite_no_ponto = 0
        elif test_ir <= b1:
            iop_limite_no_ponto = p
        elif test_ir <= b2:
            iop_limite_no_ponto = p + (s1 * (test_ir - b1))
        else:  # test_ir > b2
            # Se o ponto de teste estiver além do BP2, calculamos o limite
            iop_no_bp2 = p + (s1 * (b2 - b1))
            iop_limite_no_ponto = iop_no_bp2 + (s2 * (test_ir - b2))

            # Garante que o limite não ultrapasse o "unrestrained"
            if iop_limite_no_ponto > unres:
                iop_limite_no_ponto = unres

        status_ponto = ""
        cor_ponto = ""
        if test_iop > iop_limite_no_ponto:
            status_ponto = "OPERAR"
            cor_ponto = "red"
        else:
            status_ponto = "BLOQUEAR (Restringir)"
            cor_ponto = "green"

        fig.add_trace(go.Scatter(
            x=[test_ir],
            y=[test_iop],
            mode='markers+text',
            marker=dict(color=cor_ponto, size=15),
            text=[f"Ponto de Teste<br>Status: {status_ponto}"],
            textposition="top right",
            name="Ponto de Teste"
        ))

        # --- 8. Ajustar Layout ---
        fig.update_layout(
            xaxis_range=[0, max_x_axis],
            yaxis_range=[0, max_y_axis],
            showlegend=False
        )

        return fig

    except Exception as e:
        fig.update_layout(title=f"Erro ao plotar: {e}")
        return fig