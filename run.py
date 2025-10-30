from dash import dcc, html

# Importa a app principal do app.py
from app import app

server = app.server
# Importa as variáveis de layout do layouts.py
from layouts import layout_home, layout_sym, layout_dist, layout_tcc
# Importa os callbacks
import callbacks

# --- [NOVA ABORDAGEM] Definir Estilos das Abas em Python ---

# Estilo para as abas NÃO selecionadas
TAB_STYLE = {
    'backgroundColor': '#2a2a2a',
    'color': '#f0f0f0',
    'border': '1px solid #444',
    'borderBottom': 'none',
    'padding': '12px 18px',
    'borderRadius': '8px 8px 0 0',
    'fontWeight': 'bold'
}

# Estilo para a aba SELECIONADA
# Começamos com uma cópia do estilo base
SELECTED_TAB_STYLE = TAB_STYLE.copy()
# E agora alteramos apenas o que é diferente
SELECTED_TAB_STYLE['color'] = '#00aaff'
SELECTED_TAB_STYLE['borderTop'] = '3px solid #00aaff'
SELECTED_TAB_STYLE['borderBottom'] = '1px solid #2a2a2a'  # Para "fundir" com o conteúdo
# --- [FIM DA NOVA ABORDAGEM] ---


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
             # Removemos o 'className="Tabs"'
             # E adicionamos os estilos inline que acabámos de definir:
             style={'height': '50px'},  # Altura para a barra de abas
             tab_style=TAB_STYLE,
             selected_tab_style=SELECTED_TAB_STYLE
             ),

])  # Fim do Layout

# --- 4. Executar o Servidor (PARA DESENVOLVIMENTO LOCAL) ---
if __name__ == '__main__':
    app.run(debug=True)