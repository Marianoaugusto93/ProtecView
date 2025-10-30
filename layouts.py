from dash import dcc, html

# --- Layout da Aba 1: Home ---
layout_home = html.Div(className='module-container', children=[
    html.H2('Bem-vindo ao ProtecView!'),
    html.P('Este é um conjunto de ferramentas de análise de sistemas elétricos de potência.'),
    html.P('Selecione uma das ferramentas nas abas acima para começar.')
])
# --- [INÍCIO] Layout da Aba 2: Componentes Simétricos (MODIFICADO) ---

layout_sym = html.Div(className='module-container', children=[
    html.H2(children='Calculador de Componentes Simétricos'),

    # --- NOVO: Seletor de Direção ---
    html.Label("Direção da Conversão:"),
    dcc.Dropdown(
        id='sym-direction-dropdown',
        options=[
            {'label': 'Fase para Simétrico', 'value': 'phase-to-sym'},
            {'label': 'Simétrico para Fase', 'value': 'sym-to-phase'},
        ],
        value='phase-to-sym',  # Valor padrão
        clearable=False,
        className='DashDropdown'
    ),
    html.Br(),

    # --- Entradas (Inputs) Generalizadas ---
    html.Div(children=[
        html.H4("Entrada"),

        # Entrada 1
        html.Label(id='sym_label_in_1', children="Fase A Mag:"),
        dcc.Input(id='sym_in_mag_1', value='2.50', type='number', className='DashInput'),
        html.Label(" Âng:"),
        dcc.Input(id='sym_in_ang_1', value='0', type='number', className='DashInput', style={'width': 70}),
        html.Br(),

        # Entrada 2
        html.Label(id='sym_label_in_2', children="Fase B Mag:"),
        dcc.Input(id='sym_in_mag_2', value='3.50', type='number', className='DashInput'),
        html.Label(" Âng:"),
        dcc.Input(id='sym_in_ang_2', value='-150', type='number', className='DashInput', style={'width': 70}),
        html.Br(),

        # Entrada 3
        html.Label(id='sym_label_in_3', children="Fase C Mag:"),
        dcc.Input(id='sym_in_mag_3', value='5.00', type='number', className='DashInput'),
        html.Label(" Âng:"),
        dcc.Input(id='sym_in_ang_3', value='-177', type='number', className='DashInput', style={'width': 70}),
        html.Br(), html.Br(),

        html.Button('Calcular Componentes', id='btn_calcular_sym', n_clicks=0, className='DashButton')
    ]),

    html.Hr(),

    # --- Saídas (Outputs) Generalizadas ---
    html.Div(children=[
        html.H4("Saída"),
        html.Label(id='sym_label_out_1', children="Sequência Zero (V0): "),
        html.Div(id='sym_out_1'),  # ID antigo era 'out_v0'
        html.Br(),

        html.Label(id='sym_label_out_2', children="Sequência Positiva (V1): "),
        html.Div(id='sym_out_2'),  # ID antigo era 'out_v1'
        html.Br(),

        html.Label(id='sym_label_out_3', children="Sequência Negativa (V2): "),
        html.Div(id='sym_out_3')  # ID antigo era 'out_v2'
    ]),

    html.Hr(),

    # --- Gráficos Generalizados ---
    html.H4(id='sym_graph_title_in', children="Visualização de Fasores (Entrada)"),
    html.H4(id='sym_graph_title_out', children="Visualização de Fasores (Saída)", style={'textAlign': 'right'}),

    html.Div(children=[
        # ID antigo era 'phasor-graph-phase'
        html.Div(children=[dcc.Graph(id='sym_graph_in')], style={'width': '49%', 'display': 'inline-block'}),

        # ID antigo era 'phasor-graph-symmetrical'
        html.Div(children=[dcc.Graph(id='sym_graph_out')], style={'width': '49%', 'display': 'inline-block'})
    ])
])
# --- [FIM] Layout da Aba 2: Componentes Simétricos (MODIFICADO) ---

# --- [INÍCIO] Layout da Aba 3: Proteção de Distância (MODIFICADO) ---
layout_dist = html.Div(className='module-container', children=[
    html.H2(children='Visualizador de Zonas de Proteção de Distância'),

    html.H4("Linha 1"),
    html.Label("Imp (Ω):"),
    dcc.Input(id='line1_imp', value='10', type='number', className='DashInput'),
    html.Label(" Âng (°):"),
    dcc.Input(id='line1_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),

    # --- Zona 1 (Modificada) ---
    html.H4("Zona 1"),
    html.Label("Tipo de Zona:"),
    dcc.Dropdown(
        id='line1_z1_type',
        options=[
            {'label': 'Mho (Círculo)', 'value': 'mho'},
            {'label': 'Quadrilateral (Polígono)', 'value': 'quad'},
        ],
        value='mho',  # Padrão
        clearable=False,
        className='DashDropdown'
    ),
    html.Br(),
    # Rótulos (labels) agora têm IDs
    html.Label(id='line1_z1_label1', children="Magnitude (Ω):"),
    dcc.Input(id='line1_z1_imp', value='8', type='number', className='DashInput'),
    html.Label(id='line1_z1_label2', children=" Ângulo (°):"),
    dcc.Input(id='line1_z1_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),

    # --- Zona 2 (Modificada) ---
    html.H4("Zona 2"),
    html.Label("Tipo de Zona:"),
    dcc.Dropdown(
        id='line1_z2_type',
        options=[
            {'label': 'Mho (Círculo)', 'value': 'mho'},
            {'label': 'Quadrilateral (Polígono)', 'value': 'quad'},
        ],
        value='mho',  # Padrão
        clearable=False,
        className='DashDropdown'
    ),
    html.Br(),
    # Rótulos (labels) agora têm IDs
    html.Label(id='line1_z2_label1', children="Magnitude (Ω):"),
    dcc.Input(id='line1_z2_imp', value='12', type='number', className='DashInput'),
    html.Label(id='line1_z2_label2', children=" Ângulo (°):"),
    dcc.Input(id='line1_z2_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Button('Plotar Zonas', id='btn_plot_zones', n_clicks=0, className='DashButton'),
    html.Hr(),
    dcc.Graph(id='distance-plot-graph')
])
# --- [FIM] Layout da Aba 3: Proteção de Distância (MODIFICADO) ---


# --- Layout da Aba 4: Curvas TCC ---
# --- [INÍCIO] Layout da Aba 4: Curvas TCC (MODIFICADO) ---

# NOVO: Lista de opções de curva, incluindo IEC e IEEE
tcc_curve_options = [
    {'label': 'IEC Standard Inverse', 'value': 'IEC Standard Inverse'},
    {'label': 'IEC Very Inverse', 'value': 'IEC Very Inverse'},
    {'label': 'IEC Extremely Inverse', 'value': 'IEC Extremely Inverse'},
    {'label': 'IEEE Moderately Inverse (MI)', 'value': 'IEEE Moderately Inverse'},
    {'label': 'IEEE Very Inverse (VI)', 'value': 'IEEE Very Inverse'},
    {'label': 'IEEE Extremely Inverse (EI)', 'value': 'IEEE Extremely Inverse'},
]

layout_tcc = html.Div(className='module-container', children=[
    html.H2(children='Curvas de Característica Tempo-Corrente (TCC)'),
    html.P("Nota: As curvas SEL U3/U4 da imagem são proprietárias. Usamos curvas IEC/IEEE como exemplo."),

    # -- Inputs Relé 1 (Montante) --
    html.H4("Relé 1 (Montante)"),
    html.Label("Tipo de Curva:"),
    dcc.Dropdown(
        id='tcc_r1_type',
        options=tcc_curve_options,  # <-- USA A NOVA LISTA
        value='IEEE Moderately Inverse',  # <-- Mudei o valor padrão
        className='DashDropdown'
    ),
    html.Br(),
    html.Label("Pickup (A):"),
    dcc.Input(id='tcc_r1_pickup', value='5', type='number', className='DashInput'),
    html.Label("Time Dial (TDS):"),
    dcc.Input(id='tcc_r1_tds', value='7.37', type='number', className='DashInput'),
    html.Br(),

    # -- Inputs Relé 2 (Jusante) --
    html.H4("Relé 2 (Jusante)"),
    html.Label("Tipo de Curva:"),
    dcc.Dropdown(
        id='tcc_r2_type',
        options=tcc_curve_options,  # <-- USA A NOVA LISTA
        value='IEEE Very Inverse',  # <-- Mudei o valor padrão
        className='DashDropdown'
    ),
    html.Br(),
    html.Label("Pickup (A):"),
    dcc.Input(id='tcc_r2_pickup', value='5', type='number', className='DashInput'),
    html.Label("Time Dial (TDS):"),
    dcc.Input(id='tcc_r2_tds', value='7.75', type='number', className='DashInput'),
    html.Br(), html.Br(),

    # -- Inputs CTI --
    html.Label("Corrente de Falta para CTI (A):"),
    dcc.Input(id='tcc_fault_current', value='12.21', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Button('Plotar Curvas TCC', id='btn_plot_tcc', n_clicks=0, className='DashButton'),
    html.Hr(),

    # -- Saída CTI --
    html.H4(id='tcc-cti-output'),  # Saída de texto para o CTI

    # -- Gráfico TCC --
    dcc.Graph(id='tcc-graph')

])
# --- [FIM] Layout da Aba 4: Curvas TCC (MODIFICADO) ---