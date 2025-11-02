from dash import dcc, html

# --- Layout da Aba 1: Home (MODIFICADO) ---
layout_home = html.Div(className='module-container', children=[
    html.H2('Bem-vindo ao ProtecView!'),
    html.P('Este é um conjunto de ferramentas de análise de sistemas elétricos de potência.'),
    html.P('Selecione uma das ferramentas nas abas acima para começar.'),

    # --- NOVO: Disclaimer ---
    html.Hr(),
    html.P(children=[
        html.Strong("Disclaimer: "),
        "Esta ferramenta foi desenvolvida por um engenheiro eletricista com o auxílio de inteligência artificial (Gemini) para fins educacionais e de demonstração."
    ]),
    html.P(children=[
        "Caso seja identificado algum bug ou inconsistência, por favor, informe pelo email: ",
        # Adiciona um link de email clicável
        html.A("protecview@eletrogrid.com.br", href="mailto:protecview@eletrogrid.com.br")
    ])
])
# --- FIM DA MODIFICAÇÃO ---
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

# --- [INÍCIO] Layout da Aba 3: Proteção de Distância (Revertido para Estático) ---
layout_dist = html.Div(className='module-container', children=[
    html.H2(children='Visualizador de Zonas de Proteção de Distância'),

    html.H4("Linha 1"),
    html.Label("Imp (Ω):"),
    dcc.Input(id='line1_imp', value='10', type='number', className='DashInput'),
    html.Label(" Âng (°):"),
    dcc.Input(id='line1_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),

    # --- Zona 1 (Fixa) ---
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
    html.Label(id='line1_z1_label1', children="Magnitude (Ω):"),
    dcc.Input(id='line1_z1_imp', value='8', type='number', className='DashInput'),
    html.Label(id='line1_z1_label2', children=" Ângulo (°):"),
    dcc.Input(id='line1_z1_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),

    # --- Zona 2 (Fixa) ---
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
    html.Label(id='line1_z2_label1', children="Magnitude (Ω):"),
    dcc.Input(id='line1_z2_imp', value='12', type='number', className='DashInput'),
    html.Label(id='line1_z2_label2', children=" Ângulo (°):"),
    dcc.Input(id='line1_z2_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Button('Plotar Zonas', id='btn_plot_zones', n_clicks=0, className='DashButton'),
    html.Hr(),
    dcc.Graph(id='distance-plot-graph')
])
# --- [FIM] Layout da Aba 3: Proteção de Distância (Revertido para Estático) ---

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

# --- [INÍCIO] NOVO Layout da Aba 4: Cálculo de Faltas ---
layout_fault_calc = html.Div(className='module-container', children=[
    html.H2(children='Calculadora de Curto-Circuito (Assimétrico)'),
    html.P(
        "Insira os valores das impedâncias de sequência e a tensão pré-falta no ponto da falta. Os valores são assumidos em p.u. (por unidade)."),

    # --- Entradas (Inputs) ---
    html.H4("Entradas (p.u.)"),

    html.Label("V Pré-Falta Mag (p.u.):"),
    dcc.Input(id='fault_v_mag', value='1.0', type='number', className='DashInput'),
    html.Label(" Âng (°):"),
    dcc.Input(id='fault_v_ang', value='0', type='number', className='DashInput', style={'width': 70}),
    html.Br(),

    html.Label("Z1 (Positiva) Mag (p.u.):"),
    dcc.Input(id='fault_z1_mag', value='0.2', type='number', className='DashInput'),
    html.Label(" Âng (°):"),
    dcc.Input(id='fault_z1_ang', value='85', type='number', className='DashInput', style={'width': 70}),
    html.Br(),

    html.Label("Z2 (Negativa) Mag (p.u.):"),
    dcc.Input(id='fault_z2_mag', value='0.2', type='number', className='DashInput'),
    html.Label(" Âng (°):"),
    dcc.Input(id='fault_z2_ang', value='85', type='number', className='DashInput', style={'width': 70}),
    html.Br(),

    html.Label("Z0 (Zero) Mag (p.u.):"),
    dcc.Input(id='fault_z0_mag', value='0.3', type='number', className='DashInput'),
    html.Label(" Âng (°):"),
    dcc.Input(id='fault_z0_ang', value='85', type='number', className='DashInput', style={'width': 70}),
    html.Br(), html.Br(),

    html.Button('Calcular Faltas', id='btn_calc_fault', n_clicks=0, className='DashButton'),
    html.Hr(),

    # --- Saídas (Outputs) ---
    html.H4("Resultados da Corrente de Falta (p.u.)"),

    html.Label("Corrente Trifásica (3PH): "),
    html.Div(id='out_fault_3ph', style={'display': 'inline-block', 'fontWeight': 'bold'}),
    html.Br(),

    html.Label("Corrente Fase-Terra (LG): "),
    html.Div(id='out_fault_lg', style={'display': 'inline-block', 'fontWeight': 'bold'}),
    html.Br(),

    html.Label("Corrente Fase-Fase (LL): "),
    html.Div(id='out_fault_ll', style={'display': 'inline-block', 'fontWeight': 'bold'}),
])
# --- [FIM] NOVO Layout da Aba 4 ---

# --- [INÍCIO] NOVO Layout da Aba 5: Ampacidade de Cabos ---
layout_ampacity = html.Div(className='module-container', children=[
    html.H2(children='Calculadora de Ampacidade de Cabos'),
    html.P(
        "Calcula a capacidade de condução de corrente de um cabo com base em fatores de correção (Baseado em tabelas IEC 60364-5-52)."),

    # --- Entradas (Inputs) ---
    html.H4("Dados de Entrada"),

    html.Label("Corrente Nominal do Cabo (A):"),
    html.P("Corrente base do cabo em condições ideais (ex: 30°C, ao ar)."),
    dcc.Input(id='amp_base_current', value='100', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Tipo de Isolamento:"),
    dcc.Dropdown(
        id='amp_insulation_type',
        options=[
            {'label': 'PVC (70°C)', 'value': 'pvc'},
            {'label': 'XLPE / EPR (90°C)', 'value': 'xlpe_epr'},
        ],
        value='xlpe_epr',
        clearable=False,
        className='DashDropdown'
    ),
    html.Br(),

    html.Label("Temperatura Ambiente (°C):"),
    dcc.Input(id='amp_ambient_temp', value='40', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Método de Instalação (Agrupamento):"),
    dcc.Dropdown(
        id='amp_grouping_type',
        options=[
            {'label': 'Sem agrupamento (1 circuito)', 'value': 1},
            {'label': 'Agrupado (2 circuitos)', 'value': 2},
            {'label': 'Agrupado (3 circuitos)', 'value': 3},
            {'label': 'Agrupado (4 circuitos)', 'value': 4},
        ],
        value=1,
        clearable=False,
        className='DashDropdown'
    ),
    html.Br(),

    html.Button('Calcular Ampacidade', id='btn_calc_ampacity', n_clicks=0, className='DashButton'),
    html.Hr(),

    # --- Saídas (Outputs) ---
    html.H4("Resultados"),

    html.Label("Fator de Correção de Temperatura (F_temp): "),
    html.Div(id='out_amp_f_temp', style={'display': 'inline-block', 'fontWeight': 'bold', 'color': '#00dd00'}),
    html.Br(),

    html.Label("Fator de Correção de Agrupamento (F_group): "),
    html.Div(id='out_amp_f_group', style={'display': 'inline-block', 'fontWeight': 'bold', 'color': '#00dd00'}),
    html.Br(),

    html.H3("Ampacidade Corrigida (A): "),
    html.Div(id='out_amp_corrected',
             style={'display': 'inline-block', 'fontWeight': 'bold', 'fontSize': '1.5em', 'color': '#00aaff'}),
])
# --- [FIM] NOVO Layout da Aba 5 ---

# --- [INÍCIO] Layout da Aba 6: Saturação de TC (Com Gráfico) ---
layout_ct_saturation = html.Div(className='module-container', children=[
    html.H2(children='Calculadora de Saturação de TC (ANSI/IEEE)'),
    html.P("Verifica se um TC irá saturar com base na corrente de falta e na carga (burden)."),

    # --- Entradas (Inputs) ---
    html.H4("Dados do Sistema e Falta"),
    html.Label("Corrente de Falta Primária (A):"),
    html.P(
        "A corrente de falta simétrica no ponto do TC. (Pode vir do Módulo 'Cálculo de Faltas', após converter de p.u.)"),
    dcc.Input(id='ctsat_if_primary', value='10000', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Relação X/R do Sistema:"),
    dcc.Input(id='ctsat_xr_ratio', value='15', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.H4("Dados do Transformador de Corrente (TC)"),
    html.Label("Rácio do TC (ex: 600/5):"),
    dcc.Input(id='ctsat_ratio_num', value='600', type='number', className='DashInput', style={'width': 100}),
    html.Label(" / 5 A"),
    html.Br(), html.Br(),

    html.Label("Classe de Saturação (ex: C400):"),
    html.P("O número da classe (ex: 400) é a tensão de kneepoint (Vk) real."),
    dcc.Input(id='ctsat_vk_actual', value='400', type='number', className='DashInput'),
    html.Label(" V (Kneepoint)"),
    html.Br(), html.Br(),

    html.Label("Resistência Secundária do TC (Rct) (Ω):"),
    dcc.Input(id='ctsat_rct', value='0.5', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Resistência do Burden (Relé + Fios) (Rb) (Ω):"),
    dcc.Input(id='ctsat_rb', value='2.0', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Button('Verificar Saturação', id='btn_calc_ctsat', n_clicks=0, className='DashButton'),
    html.Hr(),

    # --- Saídas (Outputs) ---
    html.H4("Resultados da Análise"),

    html.Label("Corrente de Falta Secundária (If,sec): "),
    html.Div(id='out_ctsat_if_sec', style={'display': 'inline-block', 'fontWeight': 'bold', 'color': '#00dd00'}),
    html.Br(),

    html.Label("Tensão de Kneepoint REQUERIDA (Vk,req): "),
    html.Div(id='out_ctsat_vk_req', style={'display': 'inline-block', 'fontWeight': 'bold', 'color': '#00dd00'}),
    html.Br(),

    html.H3("Resultado:"),
    html.Div(id='out_ctsat_result',
             style={'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px'}),

    # --- [NOVO] Gráfico de Saturação ---
    dcc.Graph(id='ctsat_graph')
])
# --- [FIM] NOVO Layout da Aba 6 ---

# --- [INÍCIO] Layout da Aba 7: Proteção Diferencial (MODIFICADO) ---
layout_diff = html.Div(className='module-container', children=[
    html.H2(children='Visualizador de Proteção Diferencial (ANSI 87)'),
    html.P("Plota a curva de restrição (slope) de um relé diferencial e pontos de operação de teste."),

    # --- Coluna da Esquerda: Definições ---
    html.Div(style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}, children=[
        html.H4("Definições do Relé Diferencial (em p.u.)"),

        html.Label("Pickup Mínimo (Idif >):"),
        dcc.Input(id='diff_pickup', value='0.3', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Label("Breakpoint 1 (Ir >):"),
        dcc.Input(id='diff_bp1', value='0.0', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Label("Inclinação (Slope) 1 (%):"),
        dcc.Input(id='diff_slope1', value='25', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Label("Breakpoint 2 (Ir >):"),
        dcc.Input(id='diff_bp2', value='2.0', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Label("Inclinação (Slope) 2 (%):"),
        dcc.Input(id='diff_slope2', value='80', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Label("Pickup Não Restrito (Idiff >>):"),
        dcc.Input(id='diff_unrestrained', value='8.0', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.H4("Ponto de Teste (em p.u.)"),

        html.Label("Corrente de Operação (Iop):"),
        dcc.Input(id='diff_test_iop', value='0.8', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Label("Corrente de Restrição (Ir):"),
        dcc.Input(id='diff_test_ir', value='1.5', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.Button('Plotar Curva Diferencial', id='btn_plot_diff', n_clicks=0, className='DashButton'),
    ]),

    # --- Coluna da Direita: Gráfico ---
    html.Div(style={'width': '53%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[
        html.H4("Curva de Operação (Iop vs Ir)"),
        dcc.Graph(id='diff_graph')
    ])
])
# --- [FIM] NOVO Layout da Aba 7 ---