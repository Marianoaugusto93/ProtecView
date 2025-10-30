from dash import dcc, html

# Importa a app principal do app.py
from app import app
server = app.server # Adiciona esta linha
# Importa as variáveis de layout do layouts.py
from layouts import layout_home, layout_sym, layout_dist, layout_tcc
# Importa os callbacks. Só precisamos de o importar para que o Dash
# os "veja" e registe. Não precisamos de usar nada dele diretamente.
import callbacks

app.layout = html.Div(children=[

    html.H1(children='ProtecView: Ferramentas de Análise de Sistemas Elétricos'),

    # --- Container Principal de Abas ---
    dcc.Tabs(id="main-tabs", children=[

        # --- Aba 1: Home ---
        dcc.Tab(label='Home', children=[
            layout_home
        ], value='tab-home'),

        # --- Aba 2: Componentes Simétricos ---
        dcc.Tab(label='Componentes Simétricos', children=[
            layout_sym
        ], value='tab-sym'),

        # --- Aba 3: Proteção de Distância ---
        dcc.Tab(label='Proteção de Distância', children=[
            layout_dist
        ], value='tab-dist'),

        # --- Aba 4: Curvas TCC ---
        dcc.Tab(label='Curvas TCC', children=[
            layout_tcc
        ], value='tab-tcc'),

    ],
             className="Tabs",
             value='tab-home',
             #tab_className="Tab",  # <-- ADICIONA ESTA LINHA
             #selected_tab_className="Tab--selected"  # <-- ADICIONA ESTA LINHA
             ),

])
# --- 4. Executar o Servidor ---
#if __name__ == '__main__':
    # Nota: Estamos a executar 'app.run', não 'run.run'
   # app.run(debug=False)