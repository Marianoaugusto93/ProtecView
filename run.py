from dash import dcc, html

# Importa a app principal do app.py
from app import app

server = app.server
# Importa as variáveis de layout do layouts.py
from layouts import layout_home, layout_sym, layout_dist, layout_tcc
# Importa os callbacks
import callbacks

# --- [CORREÇÃO] Definir Estilos das Abas com o métod 'colors' ---
# Esta é a forma correta de estilizar abas no dash==3.2.0
TAB_COLORS = {
    "background": "#2a2a2a",  # Cor de fundo da aba NÃO selecionada
    "primary": "#00aaff",  # Cor do texto da aba SELECIONADA
    "border": "#4a4a4a"  # Cor da borda inferior
}
# --- [FIM DA CORREÇÃO] ---


# --- 2. Definir o Layout da Aplicação ---
app.layout = html.Div(children=[

    html.H1(children='ProtecView: Ferramentas de Análise de Sistemas Elétricos'),

    # --- Container Principal de Abas (MODIFICADO) ---
    dcc.Tabs(id="main-tabs", children=[

        # --- Aba 1: Home ---
        dcc.Tab(label='Home', children=[
            layout_home  # Usa a variável importada
        ], value='tab-home'),

        # --- Aba 2: Componentes Simétricos ---
        dcc.Tab(label='Componentes Simétricos', children=[
            layout_sym  # Usa a variável importada
        ], value='tab-sym'),

        # --- Aba 3: Proteção de Distância ---
        dcc.Tab(label='Proteção de Distância', children=[
            layout_dist  # Usa a variável importada
        ], value='tab-dist'),

        # --- Aba 4: Curvas TCC ---
        dcc.Tab(label='Curvas TCC', children=[
            layout_tcc  # Usa a variável importada
        ], value='tab-tcc'),

    ],
             value='tab-home',

             # --- [ALTERAÇÃO CRÍTICA] ---
             # Removemos os argumentos 'tab_style' e 'selected_tab_style'
             # E adicionamos o argumento 'colors'
             colors=TAB_COLORS
             ),

])  # Fim do Layout

# --- 4. Executar o Servidor (PARA DESENVOLVIMENTO LOCAL) ---
if __name__ == '__main__':
    app.run(debug=True)