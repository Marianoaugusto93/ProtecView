# Ficheiro: callbacks/callbacks_ct.py
from dash import Input, Output, State, html
import plotly.graph_objects as go
from app import app
from utils import check_ct_saturation


# --- MÓDULO 6: Saturação de TC ---
@app.callback(
    [Output('out_ctsat_if_sec', 'children'),
     Output('out_ctsat_vk_req', 'children'),
     Output('out_ctsat_result', 'children'),
     Output('out_ctsat_result', 'style'),
     Output('ctsat_graph', 'figure')],  # <-- NOVA SAÍDA
    [Input('btn_calc_ctsat', 'n_clicks')],
    [State('ctsat_if_primary', 'value'),
     State('ctsat_ratio_num', 'value'),
     State('ctsat_vk_actual', 'value'),
     State('ctsat_rct', 'value'),
     State('ctsat_rb', 'value'),
     State('ctsat_xr_ratio', 'value')]
)
def handle_ct_saturation_calc(n_clicks, if_primary, ct_ratio_num, vk_actual_str, r_ct, r_b, xr_ratio):
    # Estilo base para o resultado (será modificado)
    base_style = {'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px'}

    # --- [NOVO] Gráfico Vazio por Padrão ---
    fig = go.Figure(layout=go.Layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title="Análise de Saturação de TC (V-I)"
    ))

    if n_clicks is None or n_clicks == 0:
        fig.update_layout(xaxis_title="Corrente Secundária (A)", yaxis_title="Tensão Secundária (V)")
        return "Clique em 'Verificar'", "Clique em 'Verificar'", "Aguardando cálculo...", base_style, fig

    try:
        vk_actual = float(vk_actual_str)  # Converte para float

        # --- 1. Chamar a função de cálculo (do utils.py) ---
        results = check_ct_saturation(if_primary, ct_ratio_num, vk_actual, r_ct, r_b, xr_ratio)

        # --- 2. Formatar Saídas ---
        if_sec = results['if_sec']
        vk_required = results['vk_required']
        out_if_sec = f"{if_sec:.2f} A"
        out_vk_req = f"{vk_required:.2f} V"
        out_status = results['status']

        # --- 3. Definir o estilo (cor) do resultado ---
        cor_ponto = ""
        if out_status == 'SATURAÇÃO OK':
            base_style['backgroundColor'] = '#28a745'  # Verde
            base_style['color'] = '#ffffff'
            cor_ponto = 'green'
        elif out_status == 'SATURAÇÃO CRÍTICA':
            base_style['backgroundColor'] = '#dc3545'  # Vermelho
            base_style['color'] = '#ffffff'
            cor_ponto = 'red'
        else:
            base_style['backgroundColor'] = '#ffc107'  # Amarelo (para erros)
            base_style['color'] = '#000000'
            cor_ponto = 'yellow'

        # --- 4. [NOVO] Criar o Gráfico ---

        # Define os eixos para o gráfico
        max_current = max(if_sec * 1.2, 10)  # 10A ou 120% da corrente de falta
        max_voltage = max(vk_actual, vk_required) * 1.2

        # a. Plota a Curva de Capacidade do TC (Linha C400)
        # (Aproximação: uma linha horizontal na tensão de kneepoint)
        fig.add_shape(type="line",
                      x0=0, y0=vk_actual, x1=max_current, y1=vk_actual,
                      line=dict(color="cyan", width=2, dash="dash"),
                      name=f"Capacidade do TC (Vk = {vk_actual}V)"
                      )

        # b. Plota o Ponto de Operação Requerido
        fig.add_trace(go.Scatter(
            x=[if_sec],
            y=[vk_required],
            mode='markers+text',
            marker=dict(color=cor_ponto, size=15),
            text=[f"Ponto de Operação<br>V_req: {vk_required:.0f}V<br>I_sec: {if_sec:.0f}A"],
            textposition="top right",
            name="Ponto Requerido"
        ))

        fig.update_layout(
            xaxis_title="Corrente Secundária (A)",
            yaxis_title="Tensão Secundária (V)",
            xaxis_range=[0, max_current],
            yaxis_range=[0, max_voltage],
            showlegend=False
        )

        return out_if_sec, out_vk_req, out_status, base_style, fig

    except Exception as e:
        error_msg = f"Erro: {e}"
        base_style['backgroundColor'] = '#ffc107'
        base_style['color'] = '#000000'
        fig.update_layout(title=error_msg)
        return error_msg, error_msg, error_msg, base_style, fig