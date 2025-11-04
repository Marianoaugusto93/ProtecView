# Ficheiro: callbacks/callbacks_dist_protection.py
# (Removido template="plotly_dark")
from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx, no_update
import plotly.graph_objects as go
from app import app
import json
import numpy as np
from utils.utils_dist_protection import calculate_fuse_time
from utils.utils_tcc import get_tcc_time


# ... (Funções create_fuse_controls e create_recloser_controls ficam iguais) ...
def create_fuse_controls(index):
    fuse_ratings = [6, 10, 15, 25, 40, 65, 100, 140, 200]
    return html.Div(
        className='module-container',
        style={'border': '1px solid #555', 'marginBottom': '10px'},
        children=[
            html.H5(f"Fusível (ID: {index})", style={'display': 'inline-block'}),
            html.Button("Remover", id={'type': 'remove-dist-curve', 'index': index}, n_clicks=0,
                        className='DashButton', style={'backgroundColor': '#ff4d4d', 'float': 'right'}),
            html.Label("Tipo de Elo:"),
            dcc.Dropdown(
                id={'type': 'fuse-type', 'index': index},
                options=[{'label': 'Tipo K', 'value': 'K'}, {'label': 'Tipo T', 'value': 'T'}],
                value='K', clearable=False, className='DashDropdown'
            ),
            html.Label("Ampacidade (A):"),
            dcc.Dropdown(
                id={'type': 'fuse-rating', 'index': index},
                options=[{'label': f'{r} A', 'value': r} for r in fuse_ratings],
                value=40, clearable=False, className='DashDropdown'
            )
        ]
    )


def create_recloser_controls(index):
    curve_options = [
        {'label': 'IEC Standard Inverse', 'value': 'IEC Standard Inverse'},
        {'label': 'IEC Very Inverse', 'value': 'IEC Very Inverse'},
        {'label': 'IEC Extremely Inverse', 'value': 'IEC Extremely Inverse'},
        {'label': 'IEEE Moderately Inverse (MI)', 'value': 'IEEE Moderately Inverse'},
        {'label': 'IEEE Very Inverse (VI)', 'value': 'IEEE Very Inverse'},
        {'label': 'IEEE Extremely Inverse (EI)', 'value': 'IEEE Extremely Inverse'},
    ]
    return html.Div(
        className='module-container',
        style={'border': '1px solid #555', 'marginBottom': '10px'},
        children=[
            html.H5(f"Religador (ID: {index})", style={'display': 'inline-block'}),
            html.Button("Remover", id={'type': 'remove-dist-curve', 'index': index}, n_clicks=0,
                        className='DashButton', style={'backgroundColor': '#ff4d4d', 'float': 'right'}),
            html.Label("Curva Rápida (Fast):"),
            dcc.Dropdown(id={'type': 'recloser-fast-curve', 'index': index}, options=curve_options,
                         value='IEC Very Inverse', className='DashDropdown'),
            html.Label("Pickup Rápido (A):"),
            dcc.Input(id={'type': 'recloser-fast-pickup', 'index': index}, value='100', type='number',
                      className='DashInput'),
            html.Label("TDS Rápido:"),
            dcc.Input(id={'type': 'recloser-fast-tds', 'index': index}, value='0.1', type='number',
                      className='DashInput'),
            html.Br(),
            html.Label("Curva Lenta (Slow):"),
            dcc.Dropdown(id={'type': 'recloser-slow-curve', 'index': index}, options=curve_options,
                         value='IEC Extremely Inverse', className='DashDropdown'),
            html.Label("Pickup Lento (A):"),
            dcc.Input(id={'type': 'recloser-slow-pickup', 'index': index}, value='100', type='number',
                      className='DashInput'),
            html.Label("TDS Lento:"),
            dcc.Input(id={'type': 'recloser-slow-tds', 'index': index}, value='0.5', type='number',
                      className='DashInput'),
        ]
    )


# ... (Callbacks add_dist_curve, remove_dist_curve, render_dist_controls ficam iguais) ...
@app.callback(
    Output('dist_curve_storage', 'children'),
    Input('btn_add_dist_curve', 'n_clicks'),
    [State('dist_add_type_dropdown', 'value'),
     State('dist_curve_storage', 'children')]
)
def add_dist_curve(n_clicks, curve_type, storage_json):
    if n_clicks is None or n_clicks == 0:
        return no_update
    try:
        storage_list = json.loads(storage_json)
    except Exception:
        storage_list = []
    new_curve = {
        'id': n_clicks,
        'type': curve_type
    }
    storage_list.append(new_curve)
    return json.dumps(storage_list)


@app.callback(
    Output('dist_curve_storage', 'children', allow_duplicate=True),
    Input({'type': 'remove-dist-curve', 'index': ALL}, 'n_clicks'),
    State('dist_curve_storage', 'children'),
    prevent_initial_call=True
)
def remove_dist_curve(n_clicks_list, storage_json):
    button_id = ctx.triggered_id
    if not button_id:
        return no_update
    index_to_remove = button_id['index']
    try:
        storage_list = json.loads(storage_json)
    except Exception:
        storage_list = []
    new_list = [curve for curve in storage_list if curve['id'] != index_to_remove]
    return json.dumps(new_list)


@app.callback(
    Output('dynamic_dist_curve_container', 'children'),
    Input('dist_curve_storage', 'children')
)
def render_dist_controls(storage_json):
    try:
        storage_list = json.loads(storage_json)
    except Exception:
        storage_list = []
    children = []
    for curve in storage_list:
        if curve['type'] == 'fuse':
            children.append(create_fuse_controls(curve['id']))
        elif curve['type'] == 'recloser':
            children.append(create_recloser_controls(curve['id']))
    return children


@app.callback(
    Output('dist_tcc_graph', 'figure'),
    Input('btn_plot_dist_curves', 'n_clicks'),
    [
        # Fuse states
        State({'type': 'fuse-type', 'index': ALL}, 'value'),
        State({'type': 'fuse-type', 'index': ALL}, 'id'),
        State({'type': 'fuse-rating', 'index': ALL}, 'value'),
        State({'type': 'fuse-rating', 'index': ALL}, 'id'),
        # Recloser states
        State({'type': 'recloser-fast-curve', 'index': ALL}, 'value'),
        State({'type': 'recloser-fast-curve', 'index': ALL}, 'id'),
        State({'type': 'recloser-fast-pickup', 'index': ALL}, 'value'),
        State({'type': 'recloser-fast-tds', 'index': ALL}, 'value'),
        State({'type': 'recloser-slow-curve', 'index': ALL}, 'value'),
        State({'type': 'recloser-slow-pickup', 'index': ALL}, 'value'),
        State({'type': 'recloser-slow-tds', 'index': ALL}, 'value'),
        # Storage
        State('dist_curve_storage', 'children')
    ],
    prevent_initial_call=True
)
def plot_dist_tcc_graph(n_clicks,
                        # Fuse args
                        fuse_types_val, fuse_type_ids, fuse_ratings_val, fuse_rating_ids,
                        # Recloser args
                        rec_fast_curves_val, recloser_ids, rec_fast_pickups_val, rec_fast_tds_val,
                        rec_slow_curves_val, rec_slow_pickups_val, rec_slow_tds_val,
                        # Storage arg
                        storage_json):
    fig = go.Figure(layout=go.Layout(
        xaxis_type="log", yaxis_type="log",
        title="Coordenação de Distribuição",
        xaxis_title="Corrente (A)",
        yaxis_title="Tempo (s)"
    ))

    if n_clicks is None or n_clicks == 0:
        fig.update_layout(title="Adicione dispositivos e clique em 'Plotar Gráfico'")
        return fig

    try:
        storage_list = json.loads(storage_json)
    except (TypeError, json.JSONDecodeError):
        storage_list = []

    currents = np.logspace(1, np.log10(20000), num=200)

    # Criar mapeamentos de ID para valores de forma robusta
    fuse_type_map = {f_id['index']: val for f_id, val in zip(fuse_type_ids, fuse_types_val)}
    fuse_rating_map = {f_id['index']: val for f_id, val in zip(fuse_rating_ids, fuse_ratings_val)}

    # Mapeamento para religadores
    # Assumindo que os IDs de todos os componentes de um religador são os mesmos.
    # Usaremos recloser_ids como a fonte da verdade para os índices.
    recloser_map = {}

    # Criar dicionários de mapeamento para cada propriedade do religador
    fast_curve_map = {r_id['index']: val for r_id, val in zip(recloser_ids, rec_fast_curves_val)}
    fast_pickup_map = {r_id['index']: val for r_id, val in zip(recloser_ids, rec_fast_pickups_val)}
    fast_tds_map = {r_id['index']: val for r_id, val in zip(recloser_ids, rec_fast_tds_val)}
    slow_curve_map = {r_id['index']: val for r_id, val in zip(recloser_ids, rec_slow_curves_val)}
    slow_pickup_map = {r_id['index']: val for r_id, val in zip(recloser_ids, rec_slow_pickups_val)}
    slow_tds_map = {r_id['index']: val for r_id, val in zip(recloser_ids, rec_slow_tds_val)}

    for r_id_dict in recloser_ids:
        idx = r_id_dict['index']
        try:
            recloser_map[idx] = {
                'fast_curve': fast_curve_map.get(idx),
                'fast_pickup': float(fast_pickup_map.get(idx)),
                'fast_tds': float(fast_tds_map.get(idx)),
                'slow_curve': slow_curve_map.get(idx),
                'slow_pickup': float(slow_pickup_map.get(idx)),
                'slow_tds': float(slow_tds_map.get(idx))
            }
        except (ValueError, TypeError):
            # Ignorar religador se os valores numéricos forem inválidos
            continue

    for curve_data in storage_list:
        curve_id = curve_data['id']
        curve_type = curve_data['type']

        if curve_type == 'fuse':
            f_type = fuse_type_map.get(curve_id)
            f_rating = fuse_rating_map.get(curve_id)

            if f_type is None or f_rating is None:
                continue

            t_melt = [calculate_fuse_time(c, f_type, f_rating)[0] for c in currents]
            t_clear = [calculate_fuse_time(c, f_type, f_rating)[1] for c in currents]

            fig.add_trace(
                go.Scatter(x=currents, y=t_melt, mode='lines', line=dict(color='yellow', width=2, dash='dash'),
                           name=f"Fusível {f_rating}{f_type} (Melt)"))
            fig.add_trace(go.Scatter(x=currents, y=t_clear, mode='lines', line=dict(color='yellow', width=2),
                                     name=f"Fusível {f_rating}{f_type} (Clear)"))

        elif curve_type == 'recloser' and curve_id in recloser_map:
            recloser = recloser_map[curve_id]

            t_fast = [get_tcc_time(c, recloser['fast_pickup'], recloser['fast_tds'], recloser['fast_curve']) for c in currents]
            t_slow = [get_tcc_time(c, recloser['slow_pickup'], recloser['slow_tds'], recloser['slow_curve']) for c in currents]

            fig.add_trace(go.Scatter(x=currents, y=t_fast, mode='lines', line=dict(color='cyan', width=2, dash='dash'),
                                     name=f"Religador {curve_id} (Rápida)"))
            fig.add_trace(go.Scatter(x=currents, y=t_slow, mode='lines', line=dict(color='cyan', width=2),
                                     name=f"Religador {curve_id} (Lenta)"))

    fig.update_xaxes(range=[np.log10(10), np.log10(20000)], gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(range=[np.log10(0.01), np.log10(1000)], gridcolor='rgba(128,128,128,0.2)')
    return fig