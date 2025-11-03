# Ficheiro: run.py
# (Revertido para a correção final no CSS)

from dash import dcc, html, Input, Output, State

# Importa a app principal do app.py
from app import app

server = app.server

# Importa as variáveis de layout do layouts.py
from layouts import (
    layout_home, layout_sym, layout_dist, layout_tcc,
    layout_fault_calc, layout_ampacity, layout_ct_saturation,
    layout_diff, layout_inrush, layout_dist_protection
)
# Importa os callbacks
import callbacks.callbacks_sym
import callbacks.callbacks_dist
import callbacks.callbacks_tcc
import callbacks.callbacks_fault
import callbacks.callbacks_amp
import callbacks.callbacks_ct
import callbacks.callbacks_diff
import callbacks.callbacks_inrush
import callbacks.callbacks_dist_protection

# --- Definir Estilos das Abas com o método 'colors' ---
TAB_COLORS = {
    "background": "var(--tab-bg)",
    "primary": "var(--tab-active-text)",
    "border": "var(--tab-active-text)"
}

# --- 2. Definir o Layout da Aplicação ---
app.layout = html.Div(id='app-container', className='dark-theme', children=[

    # --- Cabeçalho com Logo e Título ---
    html.Div(className='header-container', children=[
        html.Img(src=app.get_asset_url('logo_protecview.png'), className='header-logo'),
        html.H1(children='ProtecView: Ferramentas de Análise de Sistemas Elétricos', className='header-title'),

        # --- Theme Switch ---
        html.Div(className='theme-switch-container', children=[
            html.Label("Modo Claro/Escuro:", className='theme-switch-label'),
            html.Label(className='theme-switch', children=[
                dcc.Checklist(
                    id='theme-toggle-switch',
                    options=[{'label': '', 'value': 'dark'}],
                    value=['dark'],
                    inputStyle={"display": "none"}
                ),
                html.Span(className='slider')
            ])
        ])
    ]),  # Fim do Cabeçalho

    # --- Container Principal de Abas ---
    dcc.Tabs(id="main-tabs", children=[
        # ... (Todas as tuas dcc.Tab... )
        dcc.Tab(label='Home', children=[layout_home], value='tab-home'),
        dcc.Tab(label='Componentes Simétricos', children=[layout_sym], value='tab-sym'),
        dcc.Tab(label='Proteção de Distância', children=[layout_dist], value='tab-dist'),
        dcc.Tab(label='Cálculo de Faltas', children=[layout_fault_calc], value='tab-fault'),
        dcc.Tab(label='Curvas TCC', children=[layout_tcc], value='tab-tcc'),
        dcc.Tab(label='Ampacidade de Cabos', children=[layout_ampacity], value='tab-amp'),
        dcc.Tab(label='Saturação de TC', children=[layout_ct_saturation], value='tab-ctsat'),
        dcc.Tab(label='Proteção Diferencial (87)', children=[layout_diff], value='tab-diff'),
        dcc.Tab(label='Cálculo de Inrush', children=[layout_inrush], value='tab-inrush'),
        dcc.Tab(label='Proteção de Distribuição', children=[layout_dist_protection], value='tab-dist-prot'),
    ],
             value='tab-home',
             colors=TAB_COLORS
             # A linha 'content_style' foi REMOVIDA
             ),

])  # Fim do Layout


# --- Callback para Alternar o Tema ---
@app.callback(
    Output('app-container', 'className'),
    Input('theme-toggle-switch', 'value')
)
def update_theme(value):
    if 'dark' in value:
        return 'dark-theme'
    else:
        return 'light-theme'


# --- 4. Executar o Servidor (PARA DESENVOLVIMENTO LOCAL) ---
if __name__ == '__main__':
    app.run(debug=False)