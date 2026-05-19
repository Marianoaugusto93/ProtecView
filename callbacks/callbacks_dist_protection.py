# Ficheiro: callbacks/callbacks_dist_protection.py
# (Removido template="plotly_dark")
from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx, no_update
import plotly.graph_objects as go
from app import app
import json
import numpy as np
import logging
from utils.utils_dist_protection import calculate_fuse_time
from utils.utils_tcc import get_tcc_time

logger = logging.getLogger(__name__)


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


# Callback para capturar valores dos componentes dinâmicos quando mudam
@app.callback(
    Output('dist_curve_values_store', 'data'),
    [
        Input({'type': 'fuse-type', 'index': ALL}, 'value'),
        Input({'type': 'fuse-rating', 'index': ALL}, 'value'),
        Input({'type': 'recloser-fast-curve', 'index': ALL}, 'value'),
        Input({'type': 'recloser-fast-pickup', 'index': ALL}, 'value'),
        Input({'type': 'recloser-fast-tds', 'index': ALL}, 'value'),
        Input({'type': 'recloser-slow-curve', 'index': ALL}, 'value'),
        Input({'type': 'recloser-slow-pickup', 'index': ALL}, 'value'),
        Input({'type': 'recloser-slow-tds', 'index': ALL}, 'value'),
    ],
    [
        State({'type': 'fuse-type', 'index': ALL}, 'id'),
        State({'type': 'fuse-rating', 'index': ALL}, 'id'),
        State({'type': 'recloser-fast-curve', 'index': ALL}, 'id'),
    ],
    prevent_initial_call=True
)
def sync_dist_values(fuse_types, fuse_ratings, rec_fast_curves, rec_fast_pickups, rec_fast_tds,
                     rec_slow_curves, rec_slow_pickups, rec_slow_tds,
                     fuse_type_ids, fuse_rating_ids, recloser_ids):
    """Sincronizar valores dos componentes dinâmicos com Store"""
    values_store = {
        'fuse_types': fuse_types or [],
        'fuse_ratings': fuse_ratings or [],
        'rec_fast_curves': rec_fast_curves or [],
        'rec_fast_pickups': rec_fast_pickups or [],
        'rec_fast_tds': rec_fast_tds or [],
        'rec_slow_curves': rec_slow_curves or [],
        'rec_slow_pickups': rec_slow_pickups or [],
        'rec_slow_tds': rec_slow_tds or [],
        'fuse_type_ids': fuse_type_ids or [],
        'fuse_rating_ids': fuse_rating_ids or [],
        'recloser_ids': recloser_ids or [],
    }
    logger.debug(f"Sincronizando valores: {len(fuse_types)} fusíveis, {len(recloser_ids)} religadores")
    return values_store


@app.callback(
    Output('dist_tcc_graph', 'figure'),
    Input('btn_plot_dist_curves', 'n_clicks'),
    [
        State('dist_curve_storage', 'children'),
        State('dist_curve_values_store', 'data'),
    ],
    prevent_initial_call=True
)
def plot_dist_tcc_graph(n_clicks, storage_json: str, values_store: dict) -> go.Figure:
    """Plotar gráfico TCC de distribuição com fusíveis e religadores"""

    fig = go.Figure(layout=go.Layout(
        xaxis_type="log", yaxis_type="log",
        title="Coordenação de Distribuição",
        xaxis_title="Corrente (A)",
        yaxis_title="Tempo (s)"
    ))

    if n_clicks is None or n_clicks == 0:
        fig.update_layout(title="Adicione dispositivos e clique em 'Plotar Gráfico'")
        return fig

    # Parsear storage
    try:
        storage_list = json.loads(storage_json) if storage_json else []
    except (TypeError, json.JSONDecodeError):
        storage_list = []
        logger.warning("Falha ao parsear storage_json")

    if not storage_list:
        fig.update_layout(title="Nenhum dispositivo adicionado")
        return fig

    if values_store is None:
        values_store = {}

    currents = np.logspace(1, np.log10(20000), num=200)

    # Criar mapeamentos robustos a partir do values_store
    fuse_type_map = {}
    fuse_rating_map = {}
    recloser_map = {}

    try:
        # Mapeamento para fusíveis
        fuse_type_ids = values_store.get('fuse_type_ids', [])
        fuse_types = values_store.get('fuse_types', [])
        fuse_ratings = values_store.get('fuse_ratings', [])
        fuse_rating_ids = values_store.get('fuse_rating_ids', [])

        for f_id, f_type in zip(fuse_type_ids, fuse_types):
            if f_id and isinstance(f_id, dict):
                fuse_type_map[f_id.get('index')] = f_type

        for f_id, f_rating in zip(fuse_rating_ids, fuse_ratings):
            if f_id and isinstance(f_id, dict):
                fuse_rating_map[f_id.get('index')] = f_rating

        logger.debug(f"Mapa fusíveis: {fuse_type_map}, {fuse_rating_map}")

        # Mapeamento para religadores
        recloser_ids = values_store.get('recloser_ids', [])
        rec_fast_curves = values_store.get('rec_fast_curves', [])
        rec_fast_pickups = values_store.get('rec_fast_pickups', [])
        rec_fast_tds = values_store.get('rec_fast_tds', [])
        rec_slow_curves = values_store.get('rec_slow_curves', [])
        rec_slow_pickups = values_store.get('rec_slow_pickups', [])
        rec_slow_tds = values_store.get('rec_slow_tds', [])

        for r_id, fc, fp, ft, sc, sp, st in zip(
            recloser_ids, rec_fast_curves, rec_fast_pickups, rec_fast_tds,
            rec_slow_curves, rec_slow_pickups, rec_slow_tds
        ):
            if r_id and isinstance(r_id, dict):
                idx = r_id.get('index')
                try:
                    recloser_map[idx] = {
                        'fast_curve': fc,
                        'fast_pickup': float(fp) if fp else 100,
                        'fast_tds': float(ft) if ft else 0.1,
                        'slow_curve': sc,
                        'slow_pickup': float(sp) if sp else 100,
                        'slow_tds': float(st) if st else 0.5,
                    }
                except (ValueError, TypeError) as e:
                    logger.warning(f"Erro ao processar religador {idx}: {e}")
                    continue

        logger.debug(f"Mapa religadores: {recloser_map}")

    except Exception as e:
        logger.error(f"Erro ao criar mapeamentos: {e}", exc_info=True)
        fig.update_layout(title=f"Erro: {str(e)}")
        return fig

    # Plotar curvas
    trace_count = 0
    for curve_data in storage_list:
        curve_id = curve_data.get('id')
        curve_type = curve_data.get('type')

        if curve_type == 'fuse':
            f_type = fuse_type_map.get(curve_id)
            f_rating = fuse_rating_map.get(curve_id)

            if f_type is None or f_rating is None:
                logger.warning(f"Fusível {curve_id}: tipo={f_type}, rating={f_rating} - pulando")
                continue

            try:
                t_melt = [calculate_fuse_time(c, f_type, f_rating)[0] for c in currents]
                t_clear = [calculate_fuse_time(c, f_type, f_rating)[1] for c in currents]

                fig.add_trace(
                    go.Scatter(x=currents, y=t_melt, mode='lines',
                               line=dict(color='yellow', width=2, dash='dash'),
                               name=f"Fusível {f_rating}{f_type} (Melt)"))
                fig.add_trace(
                    go.Scatter(x=currents, y=t_clear, mode='lines',
                               line=dict(color='yellow', width=2),
                               name=f"Fusível {f_rating}{f_type} (Clear)"))
                trace_count += 2
                logger.info(f"Fusível {f_rating}{f_type} plotado")

            except Exception as e:
                logger.error(f"Erro ao calcular fusível {curve_id}: {e}")
                continue

        elif curve_type == 'recloser':
            if curve_id not in recloser_map:
                logger.warning(f"Religador {curve_id} não encontrado no mapa")
                continue

            recloser = recloser_map[curve_id]
            try:
                t_fast = [get_tcc_time(c, recloser['fast_pickup'], recloser['fast_tds'],
                                       recloser['fast_curve']) for c in currents]
                t_slow = [get_tcc_time(c, recloser['slow_pickup'], recloser['slow_tds'],
                                       recloser['slow_curve']) for c in currents]

                fig.add_trace(go.Scatter(x=currents, y=t_fast, mode='lines',
                                         line=dict(color='cyan', width=2, dash='dash'),
                                         name=f"Religador {curve_id} (Rápida)"))
                fig.add_trace(go.Scatter(x=currents, y=t_slow, mode='lines',
                                         line=dict(color='cyan', width=2),
                                         name=f"Religador {curve_id} (Lenta)"))
                trace_count += 2
                logger.info(f"Religador {curve_id} plotado")

            except Exception as e:
                logger.error(f"Erro ao calcular religador {curve_id}: {e}")
                continue

    if trace_count == 0:
        fig.update_layout(title="Nenhuma curva foi plotada. Verifique os valores dos dispositivos.")
        logger.warning("Nenhuma curva foi plotada")
    else:
        fig.update_layout(title=f"Coordenação de Distribuição ({trace_count} curvas)")

    fig.update_xaxes(range=[np.log10(10), np.log10(20000)], gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(range=[np.log10(0.01), np.log10(1000)], gridcolor='rgba(128,128,128,0.2)')

    logger.info(f"Gráfico plotado com sucesso: {trace_count} curvas")
    return fig