# Ficheiro: callbacks/callbacks_dist.py
# (Removido template="plotly_dark")
from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx, no_update
import plotly.graph_objects as go
from app import app
import json
from utils.utils_common import polar_to_complex

# --- Funções de Criação de Componentes Dinâmicos ---
def create_dist_zone_controls(index):
    colors = ['#009cff', '#ff0d57', '#28a745', '#ffc107', '#6f42c1']
    color = colors[index % len(colors)]

    return html.Div(
        className='module-container',
        style={'border': f'2px solid {color}', 'marginBottom': '10px', 'padding': '10px'},
        children=[
            html.H5(f"Zona {index}", style={'display': 'inline-block'}),
            html.Button("Remover", id={'type': 'remove-dist-zone', 'index': index}, n_clicks=0,
                        className='DashButton', style={'backgroundColor': '#ff4d4d', 'float': 'right'}),

            html.Label("Tipo de Zona:"),
            dcc.Dropdown(
                id={'type': 'dist-zone-type', 'index': index},
                options=[
                    {'label': 'Mho (Círculo)', 'value': 'mho'},
                    {'label': 'Quadrilateral (Polígono)', 'value': 'quad'},
                ],
                value='mho',
                clearable=False,
                className='DashDropdown'
            ),
            html.Br(),

            html.Div(id={'type': 'dist-zone-inputs', 'index': index}, children=[
                html.Label("Magnitude (Ω):"),
                dcc.Input(id={'type': 'dist-zone-param1', 'index': index}, value='8', type='number', className='DashInput'),
                html.Label(" Ângulo (°):"),
                dcc.Input(id={'type': 'dist-zone-param2', 'index': index}, value='80', type='number', className='DashInput'),
            ])
        ]
    )

# --- Callbacks de Gerenciamento (Adicionar/Remover) ---
@app.callback(
    Output('dist_zone_storage', 'data'),
    Input('btn_add_dist_zone', 'n_clicks'),
    State('dist_zone_storage', 'data')
)
def add_dist_zone(n_clicks, data):
    if n_clicks is None:
        return no_update

    new_index = data['next_id']
    data['zones'][str(new_index)] = {'id': new_index}
    data['next_id'] = new_index + 1
    return data

@app.callback(
    Output('dist_zone_storage', 'data', allow_duplicate=True),
    Input({'type': 'remove-dist-zone', 'index': ALL}, 'n_clicks'),
    State('dist_zone_storage', 'data'),
    prevent_initial_call=True
)
def remove_dist_zone(n_clicks_list, data):
    triggered_id = ctx.triggered_id
    if not triggered_id:
        return no_update

    index_to_remove = str(triggered_id['index'])
    if index_to_remove in data['zones']:
        del data['zones'][index_to_remove]

    return data

# --- Callback de Renderização ---
@app.callback(
    Output('dynamic_dist_zone_container', 'children'),
    Input('dist_zone_storage', 'data')
)
def render_dist_zones(data):
    if not data or not data.get('zones'):
        return []
    return [create_dist_zone_controls(int(id)) for id in data['zones'].keys()]

# --- Callback para Atualizar Labels ---
@app.callback(
    Output({'type': 'dist-zone-inputs', 'index': MATCH}, 'children'),
    Input({'type': 'dist-zone-type', 'index': MATCH}, 'value'),
    State({'type': 'dist-zone-type', 'index': MATCH}, 'id')
)
def update_zone_labels(zone_type, zone_id):
    index = zone_id['index']
    if zone_type == 'mho':
        return [
            html.Label("Magnitude (Ω):"),
            dcc.Input(id={'type': 'dist-zone-param1', 'index': index}, value='8', type='number', className='DashInput'),
            html.Label(" Ângulo (°):"),
            dcc.Input(id={'type': 'dist-zone-param2', 'index': index}, value='80', type='number', className='DashInput'),
        ]
    elif zone_type == 'quad':
        return [
            html.Label("Alcance X (Ω):"),
            dcc.Input(id={'type': 'dist-zone-param1', 'index': index}, value='10', type='number', className='DashInput'),
            html.Label(" Alcance R (Ω):"),
            dcc.Input(id={'type': 'dist-zone-param2', 'index': index}, value='5', type='number', className='DashInput'),
        ]
    return no_update

# --- Callback Principal de Plotagem ---
@app.callback(
    Output('distance-plot-graph', 'figure'),
    Input('btn_plot_zones', 'n_clicks'),
    [
        State('line1_imp', 'value'),
        State('line1_ang', 'value'),
        State('dist_zone_storage', 'data'),
        State({'type': 'dist-zone-type', 'index': ALL}, 'value'),
        State({'type': 'dist-zone-type', 'index': ALL}, 'id'),
        State({'type': 'dist-zone-param1', 'index': ALL}, 'value'),
        State({'type': 'dist-zone-param2', 'index': ALL}, 'value')
    ]
)
def plotar_zonas_de_distancia(n_clicks, line_imp, line_ang,
                              zone_data, zone_types, zone_ids,
                              zone_params1, zone_params2):
    fig = go.Figure(layout=go.Layout())

    if n_clicks is None or n_clicks == 0:
        fig.update_layout(title="Adicione Zonas e clique em 'Plotar' para ver o gráfico R-X")
        return fig

    # Mapeamento de IDs para valores
    type_map = {z_id['index']: z_type for z_id, z_type in zip(zone_ids, zone_types)}
    param1_map = {z_id['index']: val for z_id, val in zip(zone_ids, zone_params1)}
    param2_map = {z_id['index']: val for z_id, val in zip(zone_ids, zone_params2)}

    try:
        # Plotar a linha
        Z_l1 = polar_to_complex(float(line_imp), float(line_ang))
        fig.add_trace(go.Scatter(
            x=[0, Z_l1.real], y=[0, Z_l1.imag], mode='lines+markers',
            name=f'Linha: {line_imp}Ω ∠{line_ang}°', line=dict(color='white', width=3)
        ))

        colors = ['#009cff', '#ff0d57', '#28a745', '#ffc107', '#6f42c1']

        # Iterar sobre as zonas no storage
        for i, zone_id_str in enumerate(zone_data['zones'].keys()):
            zone_id = int(zone_id_str)
            zone_type = type_map.get(zone_id)
            param1 = param1_map.get(zone_id)
            param2 = param2_map.get(zone_id)
            color = colors[i % len(colors)]

            if zone_type == 'mho':
                Z_mho = polar_to_complex(float(param1), float(param2))
                center_x, center_y = Z_mho.real / 2, Z_mho.imag / 2
                radius = abs(Z_mho) / 2
                fig.add_shape(type="circle", xref="x", yref="y",
                              x0=center_x - radius, y0=center_y - radius,
                              x1=center_x + radius, y1=center_y + radius,
                              line_color=color, fillcolor=color.replace(')', ', 0.1)').replace('rgb', 'rgba'),
                              name=f"Zona {zone_id}")
            elif zone_type == 'quad':
                X_reach, R_reach = float(param1), float(param2)
                fig.add_trace(go.Scatter(
                    x=[0, R_reach, R_reach, 0, 0], y=[0, 0, X_reach, X_reach, 0],
                    fill="toself", fillcolor=color.replace(')', ', 0.1)').replace('rgb', 'rgba'),
                    line_color=color, name=f"Zona {zone_id} (Quad)"
                ))

        fig.update_layout(
            title="Diagrama R-X de Proteção de Distância",
            xaxis_title="Resistência (R) Ω", yaxis_title="Reatância (X) Ω",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            showlegend=False
        )
        return fig
    except Exception as e:
        fig.update_layout(title=f"Erro ao plotar: {e}")
        return fig