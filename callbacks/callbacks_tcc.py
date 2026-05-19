from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx, no_update
import numpy as np
import plotly.graph_objects as go
from app import app
from utils.utils_tcc import get_tcc_time, generate_motor_curves
import json
import logging

logger = logging.getLogger(__name__)

tcc_curve_options = [
    {'label': 'IEC Standard Inverse', 'value': 'IEC Standard Inverse'},
    {'label': 'IEC Very Inverse', 'value': 'IEC Very Inverse'},
    {'label': 'IEC Extremely Inverse', 'value': 'IEC Extremely Inverse'},
    {'label': 'IEEE Moderately Inverse (MI)', 'value': 'IEEE Moderately Inverse'},
    {'label': 'IEEE Very Inverse (VI)', 'value': 'IEEE Very Inverse'},
    {'label': 'IEEE Extremely Inverse (EI)', 'value': 'IEEE Extremely Inverse'},
]

def create_tcc_curve_controls(index):
    colors = ['#ff9900', '#00cc00', '#009cff', '#ff0d57', '#ffc107', '#6f42c1']
    color = colors[index % len(colors)]

    return html.Div(
        className='module-container',
        style={'border': f'2px solid {color}', 'marginBottom': '10px', 'padding': '10px'},
        children=[
            html.H5(f"Relé {index}", style={'display': 'inline-block'}),
            html.Button("Remover", id={'type': 'remove-tcc-curve', 'index': index}, n_clicks=0,
                        className='DashButton', style={'backgroundColor': '#ff4d4d', 'float': 'right'}),

            html.Label("Tipo de Curva:"),
            dcc.Dropdown(id={'type': 'tcc-curve-type', 'index': index}, options=tcc_curve_options,
                         value='IEEE Moderately Inverse', className='DashDropdown'),
            html.Br(),
            html.Label("Pickup (A):"),
            dcc.Input(id={'type': 'tcc-curve-pickup', 'index': index}, value='5', type='number', className='DashInput'),
            html.Label("Time Dial (TDS):"),
            dcc.Input(id={'type': 'tcc-curve-tds', 'index': index}, value='1.0', type='number', className='DashInput'),
        ]
    )

@app.callback(
    Output('tcc_curve_storage', 'data'),
    Input('btn_add_tcc_curve', 'n_clicks'),
    State('tcc_curve_storage', 'data')
)
def add_tcc_curve(n_clicks, data):
    if n_clicks is None:
        return no_update

    new_index = data['next_id']
    data['curves'][str(new_index)] = {'id': new_index}
    data['next_id'] += 1
    return data

@app.callback(
    Output('tcc_curve_storage', 'data', allow_duplicate=True),
    Input({'type': 'remove-tcc-curve', 'index': ALL}, 'n_clicks'),
    State('tcc_curve_storage', 'data'),
    prevent_initial_call=True
)
def remove_tcc_curve(n_clicks, data):
    triggered_id = ctx.triggered_id
    if not triggered_id:
        return no_update

    index_to_remove = str(triggered_id['index'])
    if index_to_remove in data['curves']:
        del data['curves'][index_to_remove]

    return data

@app.callback(
    Output('dynamic_tcc_curve_container', 'children'),
    Input('tcc_curve_storage', 'data')
)
def render_tcc_curves(data):
    if not data or not data.get('curves'):
        return []
    return [create_tcc_curve_controls(int(id)) for id in data['curves'].keys()]


@app.callback(
    [Output('tcc-graph', 'figure'),
     Output('tcc-cti-output', 'children')],
    Input('btn_plot_tcc', 'n_clicks'),
    [
        State('tcc_curve_storage', 'data'),
        State({'type': 'tcc-curve-type', 'index': ALL}, 'value'),
        State({'type': 'tcc-curve-type', 'index': ALL}, 'id'),
        State({'type': 'tcc-curve-pickup', 'index': ALL}, 'value'),
        State({'type': 'tcc-curve-tds', 'index': ALL}, 'value'),
        State('tcc_fault_current', 'value'),
        State('tcc_motor_enable', 'value'),
        State('tcc_motor_in', 'value'),
        State('tcc_motor_ip_in', 'value'),
        State('tcc_motor_t_start', 'value'),
        State('tcc_motor_t_locked', 'value')
    ]
)
def plotar_curvas_tcc(n_clicks, curve_data,
                      curve_types, curve_ids, curve_pickups, curve_tds,
                      fault_current, motor_enable, motor_in, motor_ip_in,
                      motor_t_start, motor_t_locked):
    fig = go.Figure(layout=go.Layout(
        xaxis_type="log", yaxis_type="log",
        title="Curvas TCC de Sobrecorrente",
        xaxis_title="Corrente (A)",
        yaxis_title="Tempo (s)"
    ))
    cti_text = "Adicione curvas e clique em 'Plotar' para calcular o CTI."

    if n_clicks is None or n_clicks == 0:
        return fig, cti_text

    type_map = {c_id['index']: val for c_id, val in zip(curve_ids, curve_types)}
    pickup_map = {c_id['index']: float(val) for c_id, val in zip(curve_ids, curve_pickups)}
    tds_map = {c_id['index']: float(val) for c_id, val in zip(curve_ids, curve_tds)}

    all_pickups = list(pickup_map.values())
    min_pickup = min(all_pickups) if all_pickups else 1
    max_pickup = max(all_pickups) if all_pickups else 100

    if 'plot_motor' in motor_enable:
        try:
            min_pickup = min(min_pickup, float(motor_in))
            max_pickup = max(max_pickup, float(motor_in) * float(motor_ip_in))
        except Exception:
            pass

    currents = np.logspace(np.log10(min_pickup * 0.5), np.log10(max_pickup * 100), num=200)

    colors = ['#ff9900', '#00cc00', '#009cff', '#ff0d57', '#ffc107', '#6f42c1']

    all_times = []

    for i, curve_id_str in enumerate(curve_data['curves'].keys()):
        curve_id = int(curve_id_str)

        c_type = type_map.get(curve_id)
        c_pickup = pickup_map.get(curve_id)
        c_tds = tds_map.get(curve_id)

        times = [get_tcc_time(c, c_pickup, c_tds, c_type) for c in currents]
        all_times.extend(times)

        fig.add_trace(go.Scatter(
            x=currents, y=times, mode='lines',
            name=f"Relé {curve_id} ({c_type})",
            line=dict(color=colors[i % len(colors)])
        ))

    i_fault = float(fault_current)
    fault_times = {}
    for curve_id_str in curve_data['curves'].keys():
        curve_id = int(curve_id_str)
        c_type = type_map.get(curve_id)
        c_pickup = pickup_map.get(curve_id)
        c_tds = tds_map.get(curve_id)

        t_fault = get_tcc_time(i_fault, c_pickup, c_tds, c_type)
        if t_fault != np.inf:
            fault_times[curve_id] = t_fault

    # Simple CTI calculation between first two relays
    if len(fault_times) >= 2:
        ids = sorted(fault_times.keys())
        t1, t2 = fault_times[ids[0]], fault_times[ids[1]]
        cti = abs(t1 - t2)
        cti_text = f"CTI ({ids[0]}-{ids[1]}) @ {i_fault}A: {cti:.3f}s"

        fig.add_shape(type="line", x0=i_fault, y0=0.01, x1=i_fault, y1=max(t1, t2) * 1.5,
                      line=dict(color="white", width=1, dash="dot"))

        for i, (id, t) in enumerate(fault_times.items()):
             fig.add_trace(go.Scatter(
                x=[i_fault], y=[t],
                mode='markers+text',
                marker=dict(color=colors[i % len(colors)], size=10),
                text=[f"R{id}: {t:.3f}s"],
                textposition="top right", name=f"Ponto R{id}",
                textfont=dict(color='white')
            ))
    else:
        cti_text = "CTI requer pelo menos 2 relés operando na falta."


    if 'plot_motor' in motor_enable:
        try:
            motor_curves = generate_motor_curves(motor_in, motor_ip_in, motor_t_start, motor_t_locked)
            fig.add_trace(go.Scatter(
                x=motor_curves['start_currents'], y=motor_curves['start_times'],
                mode='lines', line=dict(color='blue', width=2, dash='dash'), name='Curva de Partida do Motor'
            ))
            fig.add_trace(go.Scatter(
                x=motor_curves['thermal_currents'], y=motor_curves['thermal_times'],
                mode='lines', line=dict(color='red', width=2, dash='dashdot'),
                name='Curva Térmica do Motor'
            ))
        except Exception as e:
            logger.error("Erro ao plotar motor", exc_info=True)

    valid_times = [t for t in all_times if t != np.inf and t is not None]
    max_time = max(valid_times) if valid_times else 100
    fig.update_xaxes(range=[np.log10(min_pickup * 0.9), np.log10(max_pickup * 110)])
    fig.update_yaxes(range=[np.log10(0.01), np.log10(max_time * 2)])
    return fig, cti_text