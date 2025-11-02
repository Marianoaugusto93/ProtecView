# Ficheiro: callbacks/callbacks_fault.py
from dash import Input, Output, State
from app import app
from utils.utils_common import polar_to_complex
from utils.utils_fault import calculate_fault_currents

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