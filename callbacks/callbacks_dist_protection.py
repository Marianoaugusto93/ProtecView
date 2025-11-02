# Ficheiro: callbacks/callbacks_dist_protection.py
# (Com lógica de plotagem simplificada e corrigida)

from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx, no_update
import plotly.graph_objects as go
from app import app
import json
import numpy as np

# Importa as funções de cálculo dos nossos ficheiros utils
from utils.utils_dist_protection import calculate_fuse_time
from utils.utils_tcc import get_tcc_time


# --- Funções Auxiliares (Layouts Dinâmicos) ---
# (As funções create_fuse_controls e create_recloser_controls permanecem iguais)
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


# --- Callbacks Principais ---

# Callback 1: Adicionar Curva (Fusível ou Religador)
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


# Callback 2: Remover Curva
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


# Callback 3: Renderizar os Controles das Curvas
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


# --- [INÍCIO DA CORREÇÃO] ---
# Callback 4: Plotar o Gráfico (Lógica refeita e simplificada)
@app.callback(
    Output('dist_tcc_graph', 'figure'),
    Input('btn_plot_dist_curves', 'n_clicks'),
    [
        # States dos Fusíveis (coleta TODOS)
        State({'type': 'fuse-type', 'index': ALL}, 'value'),
        State({'type': 'fuse-rating', 'index': ALL}, 'value'),
        # States dos Religadores (coleta TODOS)
        State({'type': 'recloser-fast-curve', 'index': ALL}, 'value'),
        State({'type': 'recloser-fast-pickup', 'index': ALL}, 'value'),
        State({'type': 'recloser-fast-tds', 'index': ALL}, 'value'),
        State({'type': 'recloser-slow-curve', 'index': ALL}, 'value'),
        State({'type': 'recloser-slow-pickup', 'index': ALL}, 'value'),
        State({'type': 'recloser-slow-tds', 'index': ALL}, 'value'),
        # State do storage para saber a ordem e o tipo
        State('dist_curve_storage', 'children')
    ]
)
def plot_dist_tcc_graph(n_clicks,
                        fuse_types, fuse_ratings,
                        rec_fast_curves, rec_fast_pickups, rec_fast_tds,
                        rec_slow_curves, rec_slow_pickups, rec_slow_tds,
                        storage_json):
    fig = go.Figure(layout=go.Layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
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
    except Exception:
        storage_list = []

    # Gera um range de correntes
    # Começa em 10A (log10(10)=1)
    currents = np.logspace(1, np.log10(20000), num=200)

    # --- LÓGICA SIMPLIFICADA ---
    # Contadores para as listas de state (ALL)
    # As listas (fuse_types, fuse_ratings, etc.) são garantidas
    # pelo Dash de estarem na ordem do DOM (ordem em que aparecem no ecrã).
    fuse_i = 0
    rec_i = 0

    # Itera sobre a lista do storage para desenhar na ordem correta
    for curve in storage_list:
        if curve['type'] == 'fuse':
            # Se não houver mais fusíveis na lista de state, pula
            if fuse_i >= len(fuse_types):
                continue

            f_type = fuse_types[fuse_i]
            f_rating = fuse_ratings[fuse_i]

            # (Verificação de segurança)
            if f_type is None or f_rating is None:
                fuse_i += 1
                continue

            # Calcula os tempos de fusão e eliminação
            t_melt = [calculate_fuse_time(c, f_type, f_rating)[0] for c in currents]
            t_clear = [calculate_fuse_time(c, f_type, f_rating)[1] for c in currents]

            # Plota as duas curvas (Melt e Clear)
            fig.add_trace(
                go.Scatter(x=currents, y=t_melt, mode='lines', line=dict(color='yellow', width=2, dash='dash'),
                           name=f"Fusível {f_rating}{f_type} (Melt)"))
            fig.add_trace(go.Scatter(x=currents, y=t_clear, mode='lines', line=dict(color='yellow', width=2),
                                     name=f"Fusível {f_rating}{f_type} (Clear)"))

            fuse_i += 1

        elif curve['type'] == 'recloser':
            # Se não houver mais religadores na lista de state, pula
            if rec_i >= len(rec_fast_curves):
                continue

            # Obtém os dados do religador
            fast_curve = rec_fast_curves[rec_i]
            fast_pickup = float(rec_fast_pickups[rec_i])
            fast_tds = float(rec_fast_tds[rec_i])
            slow_curve = rec_slow_curves[rec_i]
            slow_pickup = float(rec_slow_pickups[rec_i])
            slow_tds = float(rec_slow_tds[rec_i])

            # Calcula os tempos (reutilizando a função do Módulo TCC)
            t_fast = [get_tcc_time(c, fast_pickup, fast_tds, fast_curve) for c in currents]
            t_slow = [get_tcc_time(c, slow_pickup, slow_tds, slow_curve) for c in currents]

            # Plota as duas curvas (Rápida e Lenta)
            fig.add_trace(go.Scatter(x=currents, y=t_fast, mode='lines', line=dict(color='cyan', width=2, dash='dash'),
                                     name=f"Religador {curve['id']} (Rápida)"))
            fig.add_trace(go.Scatter(x=currents, y=t_slow, mode='lines', line=dict(color='cyan', width=2),
                                     name=f"Religador {curve['id']} (Lenta)"))

            rec_i += 1
    # --- FIM DA LÓGICA SIMPLIFICADA ---

    fig.update_xaxes(range=[np.log10(10), np.log10(20000)])
    fig.update_yaxes(range=[np.log10(0.01), np.log10(1000)])

    return fig
# --- [FIM DA CORREÇÃO] ---