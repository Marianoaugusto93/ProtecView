# Ficheiro: run.py
# (Adicionado o novo layout de Cálculo de Inrush)

from dash import dcc, html

# Importa a app principal do app.py
from app import app



server = app.server
# Importa as variáveis de layout do layouts.py
from layouts import layout_home, layout_sym, layout_dist, layout_tcc, layout_fault_calc, layout_ampacity, \
    layout_ct_saturation, layout_diff, layout_inrush  # <-- ADICIONE O NOVO LAYOUT
# Importa os callbacks
import callbacks.callbacks_sym
import callbacks.callbacks_dist
import callbacks.callbacks_tcc
import callbacks.callbacks_fault
import callbacks.callbacks_amp
import callbacks.callbacks_ct
import callbacks.callbacks_diff
import callbacks.callbacks_inrush

# --- Definir Estilos das Abas com o método 'colors' ---
TAB_COLORS = {
    "background": "#2a2a2a",  # Cor de fundo da aba NÃO selecionada
    "primary": "#00aaff",  # Cor do texto da aba SELECIONADA
    "border": "#4a4a4a"  # Cor da borda inferior
}

# --- 2. Definir o Layout da Aplicação ---
app.layout = html.Div(children=[

    # O dcc.Store(id='zone-storage') foi REMOVIDO no rollback

    html.H1(children='ProtecView: Ferramentas de Análise de Sistemas Elétricos'),

    # --- Container Principal de Abas ---
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

        # --- Aba 4: Cálculo de Faltas ---
        dcc.Tab(label='Cálculo de Faltas', children=[
            layout_fault_calc
        ], value='tab-fault'),

        # --- Aba 5: Curvas TCC ---
        dcc.Tab(label='Curvas TCC', children=[
            layout_tcc
        ], value='tab-tcc'),

        # --- Aba 6: Ampacidade ---
        dcc.Tab(label='Ampacidade de Cabos', children=[
            layout_ampacity
        ], value='tab-amp'),

        # --- Aba 7: Saturação de TC ---
        dcc.Tab(label='Saturação de TC', children=[
            layout_ct_saturation
        ], value='tab-ctsat'),

        # --- Aba 8: Proteção Diferencial ---
        dcc.Tab(label='Proteção Diferencial (87)', children=[
            layout_diff
        ], value='tab-diff'),

        # --- [NOVO] Aba 9: Cálculo de Inrush ---
        dcc.Tab(label='Cálculo de Inrush', children=[
            layout_inrush  # <-- ADICIONE ESTA LINHA
        ], value='tab-inrush'),

    ],
             value='tab-home',
             colors=TAB_COLORS
             ),

])  # Fim do Layout

# --- 4. Executar o Servidor (PARA DESENVOLVIMENTO LOCAL) ---
if __name__ == '__main__':
    app.run(debug=False)