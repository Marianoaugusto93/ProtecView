# Ficheiro: callbacks/callbacks_ct.py
# (Removido template="plotly_dark")
from dash import Input, Output, State, html
import plotly.graph_objects as go
from app import app
from utils.utils_ct import check_ct_saturation


from utils.utils_ct import check_ct_saturation, calculate_sinusoidal_excitation_curve

# --- MÓDULO 6: Saturação de TC ---
@app.callback(
    [Output('out_ctsat_if_sec', 'children'),
     Output('out_ctsat_vk_req', 'children'),
     Output('out_ctsat_result', 'children'),
     Output('out_ctsat_result', 'style'),
     Output('ctsat_graph', 'figure')],
    [Input('btn_calc_ctsat', 'n_clicks')],
    [State('ctsat_if_primary', 'value'),
     State('ctsat_ratio_num', 'value'),
     State('ctsat_vk_actual', 'value'),
     State('ctsat_ik_actual', 'value'),  # Novo Input
     State('ctsat_rct', 'value'),
     State('ctsat_rb', 'value'),
     State('ctsat_xr_ratio', 'value')]
)
def handle_ct_saturation_calc(n_clicks, if_primary, ct_ratio_num, vk_actual_str, ik_actual_str, r_ct, r_b, xr_ratio):
    base_style = {'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px'}

    fig = go.Figure(layout=go.Layout(
        title="Análise de Saturação de TC (V-I)"
    ))

    if n_clicks is None or n_clicks == 0:
        fig.update_layout(xaxis_title="Corrente de Excitação (A)", yaxis_title="Tensão Secundária (V)")
        return "Clique em 'Verificar'", "Clique em 'Verificar'", "Aguardando cálculo...", base_style, fig

    try:
        vk_actual = float(vk_actual_str)
        ik_actual = float(ik_actual_str)
        results = check_ct_saturation(if_primary, ct_ratio_num, vk_actual, r_ct, r_b, xr_ratio)

        if_sec = results['if_sec']
        vk_required = results['vk_required']
        out_if_sec = f"{if_sec:.2f} A"
        out_vk_req = f"{vk_required:.2f} V"
        out_status = results['status']

        if out_status == 'SATURAÇÃO OK':
            base_style.update({'backgroundColor': '#28a745', 'color': '#ffffff'})
            cor_ponto = 'green'
        elif out_status == 'SATURAÇÃO CRÍTICA':
            base_style.update({'backgroundColor': '#dc3545', 'color': '#ffffff'})
            cor_ponto = 'red'
        else: # Erro
            base_style.update({'backgroundColor': '#ffc107', 'color': '#000000'})
            cor_ponto = 'yellow'

        # Plotar a curva de excitação senoidal
        exc_currents, exc_voltages = calculate_sinusoidal_excitation_curve(vk_actual, ik_actual)
        fig.add_trace(go.Scatter(
            x=exc_currents, y=exc_voltages,
            mode='lines',
            line=dict(color='cyan', width=2),
            name='Curva de Excitação do TC'
        ))

        # O ponto de operação é V_requerido vs If_secundária
        # A curva de excitação é V vs I_excitação. São eixos diferentes.
        # Para simplificar, vamos plotar o V_requerido na curva e um marcador.
        fig.add_shape(type="line",
              x0=0, y0=vk_required, x1=exc_currents[-1], y1=vk_required,
              line=dict(color="yellow", width=2, dash="dash"),
              name=f"Tensão Requerida ({vk_required:.2f} V)"
             )

        fig.add_trace(go.Scatter(
            x=[if_sec], y=[vk_required],
            mode='markers+text',
            marker=dict(color=cor_ponto, size=15, symbol='x'),
            text=[f"Ponto de Operação<br>V_req: {vk_required:.1f}V<br>I_sec: {if_sec:.1f}A"],
            textposition="bottom right",
            name="Ponto de Operação (If_sec)",
            xaxis='x2' # Usar um eixo secundário para a corrente de falta
        ))

        max_voltage = max(exc_voltages) * 1.1

        fig.update_layout(
            xaxis_title="Corrente de Excitação (A)",
            yaxis_title="Tensão Secundária (V)",
            yaxis_range=[0, max_voltage],
            legend_title="Legenda",
            # Criar um segundo eixo X para a corrente de falta
            xaxis2=dict(
                title="Corrente de Falta Secundária (A)",
                overlaying='x',
                side='top',
                range=[0, max(if_sec * 1.5, 20)]
            )
        )

        return out_if_sec, out_vk_req, out_status, base_style, fig

    except (ValueError, TypeError) as e:
        error_msg = f"Erro: Verifique os inputs. {e}"
        base_style.update({'backgroundColor': '#dc3545', 'color': '#ffffff'})
        fig.update_layout(title=error_msg)
        return "Erro", "Erro", "Erro de Input", base_style, fig
    except Exception as e:
        error_msg = f"Erro inesperado: {e}"
        base_style.update({'backgroundColor': '#dc3545', 'color': '#ffffff'})
        fig.update_layout(title=error_msg)
        return "Erro", "Erro", "Erro Inesperado", base_style, fig