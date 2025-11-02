# Ficheiro: callbacks/callbacks_amp.py
from dash import Input, Output, State
from app import app
from utils import get_temp_correction_factor, get_grouping_correction_factor, calculate_ampacity


# --- MÓDULO 5: Ampacidade de Cabos ---
@app.callback(
    [Output('out_amp_f_temp', 'children'),
     Output('out_amp_f_group', 'children'),
     Output('out_amp_corrected', 'children')],
    [Input('btn_calc_ampacity', 'n_clicks')],
    [State('amp_base_current', 'value'),
     State('amp_insulation_type', 'value'),
     State('amp_ambient_temp', 'value'),
     State('amp_grouping_type', 'value')]
)
def handle_ampacity_calculation(n_clicks, base_current_str, insulation, temp_str, grouping):
    if n_clicks is None or n_clicks == 0:
        return "Clique em 'Calcular'", "Clique em 'Calcular'", "Clique em 'Calcular'"

    try:
        # --- 1. Converter inputs ---
        base_current = float(base_current_str)
        temp = float(temp_str)
        num_circuits = int(grouping)

        # --- 2. Obter Fatores de Correção (do utils.py) ---
        f_temp = get_temp_correction_factor(insulation, temp)
        f_group = get_grouping_correction_factor(num_circuits)

        # --- 3. Calcular Ampacidade Final (do utils.py) ---
        corrected_ampacity = calculate_ampacity(base_current, f_temp, f_group)

        # --- 4. Formatar Saídas ---
        out_f_temp = f"{f_temp:.2f}"
        out_f_group = f"{f_group:.2f}"
        out_corrected = f"{corrected_ampacity:.2f} A"

        return out_f_temp, out_f_group, out_corrected

    except Exception as e:
        error_msg = f"Erro: {e}"
        return error_msg, error_msg, error_msg