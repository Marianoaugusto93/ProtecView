# Ficheiro: callbacks/callbacks_inrush.py
from dash import Input, Output, State
from app import app
from utils import calculate_inrush  # Importa a nossa nova função


# --- MÓDULO 8: Cálculo de Inrush ---
@app.callback(
    [Output('out_inrush_in', 'children'),
     Output('out_inrush_ipeak', 'children'),
     Output('out_inrush_iop', 'children'),
     Output('out_inrush_ir', 'children')],
    [Input('btn_calc_inrush', 'n_clicks')],
    [State('inrush_kva', 'value'),
     State('inrush_kv', 'value'),
     State('inrush_multiplier', 'value'),
     State('inrush_restraint_factor', 'value')]
)
def handle_inrush_calculation(n_clicks, kva, kv, multiplier, restraint_factor):
    if n_clicks is None or n_clicks == 0:
        return "Clique em 'Calcular'", "Clique em 'Calcular'", "Clique em 'Calcular'", "Clique em 'Calcular'"

    try:
        # --- 1. Chamar a função de cálculo (do utils.py) ---
        results = calculate_inrush(kva, kv, multiplier, restraint_factor)

        # --- 2. Formatar Saídas ---
        out_in = f"{results['i_nominal_amps']:.2f} A (Corrente Nominal)"
        out_ipeak = f"{results['i_peak_amps']:.2f} A (Pico)"

        # (Resultados em p.u. da Corrente Nominal)
        out_iop = f"{results['iop_pu']:.2f} p.u. (Base Inominal)"
        out_ir = f"{results['ir_pu']:.2f} p.u. (Base Inominal)"

        return out_in, out_ipeak, out_iop, out_ir

    except Exception as e:
        error_msg = f"Erro: {e}"
        return error_msg, error_msg, error_msg, error_msg