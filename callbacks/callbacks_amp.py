# Ficheiro: callbacks/callbacks_amp.py
# (Atualizado para o Módulo 9: Dimensionamento Completo de Cabos)

from dash import Input, Output, State, html
from app import app
# Importa TODAS as funções de utils que vamos usar
from utils.utils_ampacity import (
    get_temp_correction_factor, get_grouping_correction_factor, calculate_ampacity,
    calculate_voltage_drop, check_short_circuit_withstand
)

# --- MÓDULO 9: Dimensionamento Completo de Cabos ---
@app.callback(
    [  # Saídas de Ampacidade
        Output('out_amp_corrected', 'children'),
        Output('out_amp_result', 'children'),
        Output('out_amp_result', 'style'),
        # Saídas de Queda de Tensão (VD)
        Output('out_vd_volts', 'children'),
        Output('out_vd_percent', 'children'),
        Output('out_vd_result', 'children'),
        Output('out_vd_result', 'style'),
        # Saídas de Curto-Circuito (I²t)
        Output('out_sc_fault_energy_a2s', 'children'),
        Output('out_sc_cable_withstand_a2s', 'children'),
        Output('out_sc_result', 'children'),
        Output('out_sc_result', 'style')],
    [Input('btn_calc_ampacity', 'n_clicks')],
    [  # States de Ampacidade
        State('amp_base_current', 'value'),
        State('amp_insulation_type', 'value'),
        State('amp_ambient_temp', 'value'),
        State('amp_grouping_type', 'value'),
        # States de Queda de Tensão (VD)
        State('vd_load_current', 'value'),
        State('vd_length_km', 'value'),
        State('vd_system_voltage_v', 'value'),
        State('vd_cable_r_ohm_km', 'value'),
        State('vd_cable_x_ohm_km', 'value'),
        State('vd_cos_phi', 'value'),
        State('vd_limit_percent', 'value'),
        # States de Curto-Circuito (I²t)
        State('sc_fault_current_a', 'value'),
        State('sc_fault_time_s', 'value'),
        State('sc_cable_cross_section_mm2', 'value'),
        State('sc_material_constant_k', 'value')]
)
def handle_cable_sizing(n_clicks,
                        # Args de Ampacidade
                        base_current, insulation, temp, grouping,
                        # Args de VD
                        load_current, length_km, system_v, r_km, x_km, cos_phi, vd_limit_pct_str,
                        # Args de I²t
                        fault_i, fault_t, cross_section, k_material):
    # Estilos base para as caixas de resultado
    style_ok = {'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px',
                'backgroundColor': '#28a745', 'color': '#ffffff'}
    style_fail = {'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px',
                  'backgroundColor': '#dc3545', 'color': '#ffffff'}
    style_neutral = {'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px'}

    if n_clicks is None or n_clicks == 0:
        # Retorna 11 valores 'placeholder' (3 para amp, 4 para vd, 4 para sc)
        return "...", "Clique em 'Dimensionar'", style_neutral, \
            "...", "...", "Clique em 'Dimensionar'", style_neutral, \
            "...", "...", "Clique em 'Dimensionar'", style_neutral

    try:
        # --- 1. Lógica de Ampacidade ---
        f_temp = get_temp_correction_factor(insulation, float(temp))
        f_group = get_grouping_correction_factor(int(grouping))
        corrected_ampacity = calculate_ampacity(float(base_current), f_temp, f_group)

        out_amp_corrected = f"{corrected_ampacity:.2f} A"

        # Verifica o critério de ampacidade
        if corrected_ampacity >= float(load_current):
            out_amp_result = "OK (Ampacidade > Corrente de Carga)"
            out_amp_style = style_ok
        else:
            out_amp_result = "FALHA (Ampacidade < Corrente de Carga)"
            out_amp_style = style_fail

        # --- 2. Lógica de Queda de Tensão (VD) ---
        vd_results = calculate_voltage_drop(load_current, length_km, r_km, x_km, cos_phi, system_v)
        vd_limit_pct = float(vd_limit_pct_str)

        out_vd_volts = f"{vd_results['vd_volts']:.2f} V"
        out_vd_percent = f"{vd_results['vd_percent']:.2f} %"

        # Verifica o critério de VD
        if vd_results['vd_percent'] <= vd_limit_pct:
            out_vd_result = "OK (VD% <= Limite)"
            out_vd_style = style_ok
        else:
            out_vd_result = "FALHA (VD% > Limite)"
            out_vd_style = style_fail

        # --- 3. Lógica de Suportabilidade (I²t) ---
        sc_results = check_short_circuit_withstand(fault_i, fault_t, cross_section, k_material)

        out_sc_fault = f"{sc_results['fault_energy_a2s']:.2e} A²s"  # Notação científica
        out_sc_cable = f"{sc_results['cable_withstand_a2s']:.2e} A²s"  # Notação científica

        # Verifica o critério de I²t
        if sc_results['status'] == 'OK':
            out_sc_result = "OK (Cabo Suporta o Curto)"
            out_sc_style = style_ok
        else:
            out_sc_result = "FALHA (Cabo NÃO Suporta o Curto)"
            out_sc_style = style_fail

        # Retorna todos os 11 valores
        return out_amp_corrected, out_amp_result, out_amp_style, \
            out_vd_volts, out_vd_percent, out_vd_result, out_vd_style, \
            out_sc_fault, out_sc_cable, out_sc_result, out_sc_style

    except Exception as e:
        error_msg = f"Erro: {e}"
        # Retorna 11 valores de erro
        return error_msg, "Erro", style_neutral, \
            error_msg, "Erro", "Erro", style_neutral, \
            error_msg, "Erro", "Erro", style_neutral