from dash import dcc, html

# --- Layout da Aba 1: Home ---
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
# --- [FIM] Layout da Aba 1: Home ---

# --- Layout da Aba 2: Componentes Simétricos ---
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
# --- [FIM] Layout da Aba 2: Componentes Simétricos ---

# --- Layout da Aba 3: Proteção de Distância (Dinâmico) ---
layout_dist = html.Div(className='module-container', children=[
    dcc.Store(id='dist_zone_storage', data={'zones': {}, 'next_id': 1}),

    html.H2(children='Visualizador de Zonas de Proteção de Distância'),

    # Coluna Esquerda
    html.Div(style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}, children=[
        html.H4("Dados da Linha"),
        html.Label("Impedância (Ω):"),
        dcc.Input(id='line1_imp', value='10', type='number', className='DashInput'),
        html.Label(" Ângulo (°):"),
        dcc.Input(id='line1_ang', value='80', type='number', className='DashInput'),
        html.Br(), html.Br(),

        html.H4("Controles"),
        html.Button('Adicionar Zona', id='btn_add_dist_zone', n_clicks=0, className='DashButton'),
        html.Button('Plotar Zonas', id='btn_plot_zones', n_clicks=0, className='DashButton', style={'marginLeft': '10px', 'backgroundColor': '#28a745'}),
        html.Hr(),

        html.Div(id='dynamic_dist_zone_container', children=[]),
    ]),

    # Coluna Direita
    html.Div(style={'width': '53%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[
        dcc.Graph(id='distance-plot-graph')
    ])
])
# --- [FIM] Layout da Aba 3:  ---

# --- Layout da Aba 4: Curvas TCC ---
tcc_curve_options = [
    {'label': 'IEC Standard Inverse', 'value': 'IEC Standard Inverse'},
    {'label': 'IEC Very Inverse', 'value': 'IEC Very Inverse'},
    {'label': 'IEC Extremely Inverse', 'value': 'IEC Extremely Inverse'},
    {'label': 'IEEE Moderately Inverse (MI)', 'value': 'IEEE Moderately Inverse'},
    {'label': 'IEEE Very Inverse (VI)', 'value': 'IEEE Very Inverse'},
    {'label': 'IEEE Extremely Inverse (EI)', 'value': 'IEEE Extremely Inverse'},
]
# --- Layout da Aba 4: Curvas TCC (Dinâmico) ---
layout_tcc = html.Div(className='module-container', children=[
    dcc.Store(id='tcc_curve_storage', data={'curves': {}, 'next_id': 1}),

    html.H2(children='Curvas de Característica Tempo-Corrente (TCC)'),
    html.P("Coordene dispositivos de proteção e analise a partida de motores."),

    # --- Coluna da Esquerda: Definições ---
    html.Div(style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}, children=[

        html.H4("Controles"),
        html.Button('Adicionar Relé', id='btn_add_tcc_curve', n_clicks=0, className='DashButton'),
        html.Button('Plotar Curvas TCC', id='btn_plot_tcc', n_clicks=0, className='DashButton', style={'marginLeft': '10px', 'backgroundColor': '#28a745'}),
        html.Hr(),

        html.Div(id='dynamic_tcc_curve_container', children=[]),
        html.Hr(),

        # --- Seção de Partida de Motor ---
        html.H4("Análise de Partida de Motor (Opcional)"),
        dcc.Checklist(
            options=[{'label': ' Plotar Curvas do Motor', 'value': 'plot_motor'}],
            value=[], id='tcc_motor_enable'
        ),
        html.Br(),
        html.Label("Corrente Nominal (In) (A):"),
        dcc.Input(id='tcc_motor_in', value='100', type='number', className='DashInput'),
        html.Label("Corrente de Partida (Ip) / In:"),
        dcc.Input(id='tcc_motor_ip_in', value='6', type='number', className='DashInput'),
        html.Label("Tempo de Partida (s):"),
        dcc.Input(id='tcc_motor_t_start', value='5', type='number', className='DashInput'),
        html.Label("Tempo de Rotor Bloqueado (s):"),
        dcc.Input(id='tcc_motor_t_locked', value='20', type='number', className='DashInput'),
        html.Hr(),

        # -- Inputs CTI --
        html.Label("Corrente de Falta para CTI (A):"),
        dcc.Input(id='tcc_fault_current', value='500', type='number', className='DashInput'),
    ]),

    # --- Coluna da Direita: Gráfico e Resultados ---
    html.Div(style={'width': '53%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[
        html.H4(id='tcc-cti-output'),
        dcc.Graph(id='tcc-graph')
    ])
])
# --- [FIM] Layout da Aba 4 ---

# --- Layout da Aba 5: Cálculo de Faltas ---
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
# --- [FIM] Layout da Aba 5 ---

# --- Layout da Aba 6: Ampacidade de Cabos  ---
layout_ampacity = html.Div(className='module-container', children=[
    html.H2(children='Dimensionamento de Cabos (Ampacidade, VD, I²t)'),

    # --- Coluna da Esquerda: Entradas ---
    html.Div(style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}, children=[

        # --- Seção 1: Ampacidade ---
        html.H4("Critério 1: Ampacidade"),
        html.Label("Corrente Nominal Base (A):"),
        dcc.Input(id='amp_base_current', value='100', type='number', className='DashInput'),
        html.Br(),
        html.Label("Tipo de Isolamento:"),
        dcc.Dropdown(
            id='amp_insulation_type',
            options=[
                {'label': 'PVC (70°C)', 'value': 'pvc'},
                {'label': 'XLPE / EPR (90°C)', 'value': 'xlpe_epr'},
            ],
            value='xlpe_epr', clearable=False, className='DashDropdown'
        ),
        html.Br(),
        html.Label("Temperatura Ambiente (°C):"),
        dcc.Input(id='amp_ambient_temp', value='40', type='number', className='DashInput'),
        html.Br(),
        html.Label("Agrupamento (Nº de Circuitos):"),
        dcc.Dropdown(
            id='amp_grouping_type',
            options=[{'label': f'{i} circuito(s)', 'value': i} for i in range(1, 10)],
            value=1, clearable=False, className='DashDropdown'
        ),
        html.Br(),

        # --- Seção 2: Queda de Tensão (VD) ---
        html.H4("Critério 2: Queda de Tensão (VD)"),
        html.Label("Corrente de Carga (A):"),
        dcc.Input(id='vd_load_current', value='80', type='number', className='DashInput'),
        html.Br(),
        html.Label("Comprimento do Cabo (km):"),
        dcc.Input(id='vd_length_km', value='0.15', type='number', className='DashInput'),
        html.Br(),
        html.Label("Tensão de Linha do Sistema (V):"),
        dcc.Input(id='vd_system_voltage_v', value='380', type='number', className='DashInput'),
        html.Br(),
        html.Label("Resistência do Cabo (R) (Ω/km):"),
        dcc.Input(id='vd_cable_r_ohm_km', value='0.25', type='number', className='DashInput'),
        html.Br(),
        html.Label("Reatância do Cabo (X) (Ω/km):"),
        dcc.Input(id='vd_cable_x_ohm_km', value='0.08', type='number', className='DashInput'),
        html.Br(),
        html.Label("Fator de Potência da Carga (cos φ):"),
        dcc.Input(id='vd_cos_phi', value='0.92', type='number', className='DashInput'),
        html.Br(),
        html.Label("Limite de Queda de Tensão (%):"),
        dcc.Input(id='vd_limit_percent', value='4.0', type='number', className='DashInput'),
        html.Br(), html.Br(),

        # --- Seção 3: Suportabilidade de Curto-Circuito (I²t) ---
        html.H4("Critério 3: Suportabilidade (I²t)"),
        html.P("Use os Módulos 4 (Faltas) e 5 (TCC) para obter estes valores."),
        html.Label("Corrente de Curto-Circuito (A):"),
        dcc.Input(id='sc_fault_current_a', value='5000', type='number', className='DashInput'),
        html.Br(),
        html.Label("Tempo de Atuação da Proteção (s):"),
        dcc.Input(id='sc_fault_time_s', value='0.1', type='number', className='DashInput'),
        html.Br(),
        html.Label("Secção Transversal (Bitola) (mm²):"),
        dcc.Input(id='sc_cable_cross_section_mm2', value='35', type='number', className='DashInput'),
        html.Br(),
        html.Label("Constante do Material (K):"),
        dcc.Dropdown(
            id='sc_material_constant_k',
            options=[
                {'label': 'Cobre / XLPE (K=143)', 'value': 143},
                {'label': 'Cobre / PVC (K=115)', 'value': 115},
                {'label': 'Alumínio / XLPE (K=94)', 'value': 94},
                {'label': 'Alumínio / PVC (K=76)', 'value': 76},
            ],
            value=143, clearable=False, className='DashDropdown'
        ),
        html.Br(),

        html.Button('Dimensionar Cabo', id='btn_calc_ampacity', n_clicks=0, className='DashButton',
                    style={'marginTop': '20px'}),
    ]),

    # --- Coluna da Direita: Resultados ---
    html.Div(style={'width': '53%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[

        # --- Resultados Ampacidade ---
        html.H4("Resultados: Ampacidade"),
        html.Label("Ampacidade Corrigida (A): "),
        html.Div(id='out_amp_corrected', style={'display': 'inline-block', 'fontWeight': 'bold', 'fontSize': '1.2em'}),
        html.Div(id='out_amp_result',
                 style={'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px'}),
        html.Hr(),

        # --- Resultados Queda de Tensão ---
        html.H4("Resultados: Queda de Tensão"),
        html.Label("Queda de Tensão (V): "),
        html.Div(id='out_vd_volts', style={'display': 'inline-block', 'fontWeight': 'bold'}),
        html.Br(),
        html.Label("Queda de Tensão (%): "),
        html.Div(id='out_vd_percent', style={'display': 'inline-block', 'fontWeight': 'bold'}),
        html.Div(id='out_vd_result',
                 style={'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px',
                        'marginTop': '10px'}),
        html.Hr(),

        # --- Resultados Curto-Circuito ---
        html.H4("Resultados: Suportabilidade (I²t)"),
        html.Label("Energia do Curto-Circuito (I²t Falta): "),
        html.Div(id='out_sc_fault_energy_a2s', style={'display': 'inline-block', 'fontWeight': 'bold'}),
        html.Br(),
        html.Label("Suportabilidade do Cabo (K²S²): "),
        html.Div(id='out_sc_cable_withstand_a2s', style={'display': 'inline-block', 'fontWeight': 'bold'}),
        html.Div(id='out_sc_result',
                 style={'fontWeight': 'bold', 'fontSize': '1.5em', 'padding': '10px', 'borderRadius': '5px',
                        'marginTop': '10px'}),

    ])
])
# --- [FIM] Layout da Aba 6 ---

# --- Layout da Aba 6: Saturação de TC (Com Gráfico) ---
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
    html.Br(),

    # --- NOVO INPUT ---
    html.Label("Corrente de Excitação em Vk (Ik) (A):"),
    html.P("Corrente de excitação medida no ponto de kneepoint. Se não souber, use 0.1A como estimativa."),
    dcc.Input(id='ctsat_ik_actual', value='0.1', type='number', className='DashInput'),
    html.Br(), html.Br(),
    # --- FIM NOVO INPUT ---

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
# --- [FIM] Layout da Aba 6 ---

# --- Layout da Aba 7: Proteção Diferencial ---
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
# --- [FIM] Layout da Aba 7 ---

# --- Layout da Aba 8: Cálculo de Inrush ---
layout_inrush = html.Div(className='module-container', children=[
    html.H2(children='Estimativa de Corrente de Inrush de Transformador'),
    html.P("Calcula a corrente de magnetização (inrush) e o ponto (Iop, Ir) para análise no Módulo Diferencial (87)."),

    # --- Entradas (Inputs) ---
    html.H4("Dados do Transformador"),

    html.Label("Potência do Transformador (kVA):"),
    dcc.Input(id='inrush_kva', value='1000', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Tensão (kV - Lado da Energização):"),
    dcc.Input(id='inrush_kv', value='13.8', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Múltiplo de Inrush (ex: 8 a 12):"),
    dcc.Input(id='inrush_multiplier', value='10', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Label("Fator de Restrição (ex: 0.5 para 2º Harmónico):"),
    dcc.Input(id='inrush_restraint_factor', value='0.5', type='number', className='DashInput'),
    html.Br(), html.Br(),

    html.Button('Calcular Inrush', id='btn_calc_inrush', n_clicks=0, className='DashButton'),
    html.Hr(),

    # --- Saídas (Outputs) ---
    html.H4("Resultados (Valores em p.u. da Corrente Nominal do Trafo)"),

    html.Label("Corrente Nominal (In): "),
    html.Div(id='out_inrush_in', style={'display': 'inline-block', 'fontWeight': 'bold', 'color': '#00dd00'}),
    html.Br(),

    html.Label("Corrente de Inrush de Pico (Ipeak): "),
    html.Div(id='out_inrush_ipeak', style={'display': 'inline-block', 'fontWeight': 'bold', 'color': '#00dd00'}),
    html.Br(),

    html.H3("Ponto de Teste para o Módulo Diferencial (87):"),
    html.Label("Corrente de Operação (Iop): "),
    html.Div(id='out_inrush_iop',
             style={'display': 'inline-block', 'fontWeight': 'bold', 'fontSize': '1.2em', 'color': '#00aaff'}),
    html.Br(),

    html.Label("Corrente de Restrição (Ir): "),
    html.Div(id='out_inrush_ir',
             style={'display': 'inline-block', 'fontWeight': 'bold', 'fontSize': '1.2em', 'color': '#00aaff'}),
])
# --- [FIM] Layout da Aba 8 ---

# --- Layout da Aba 9: Proteção de Distribuição  ---
layout_dist_protection = html.Div(className='module-container', children=[
    html.H2(children='Coordenação de Proteção de Distribuição (Fusíveis/Religadores)'),
    html.P("Adicione e coordene curvas de fusíveis (IEC/ANSI K, T) e sequências de religadores."),

    # Armazenamento de Estado (Div Oculto)
    html.Div(id='dist_curve_storage', children='[]', style={'display': 'none'}),  # Guarda um JSON

    # --- Coluna da Esquerda: Adicionar Curvas ---
    html.Div(style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}, children=[

        html.H4("Adicionar Dispositivo"),
        html.Label("Tipo de Dispositivo:"),
        dcc.Dropdown(
            id='dist_add_type_dropdown',
            options=[
                {'label': 'Fusível (Ex: Tipo K, T)', 'value': 'fuse'},
                {'label': 'Religador (Curva IEC/IEEE)', 'value': 'recloser'},
            ],
            value='fuse',
            clearable=False,
            className='DashDropdown'
        ),
        html.Br(),
        html.Button('Adicionar Curva', id='btn_add_dist_curve', n_clicks=0, className='DashButton'),

        # --- [NOVO] Botão de Plotar ---
        html.Button('Plotar Gráfico', id='btn_plot_dist_curves', n_clicks=0, className='DashButton',
                    style={'marginLeft': '10px', 'backgroundColor': '#28a745'}),
        html.Hr(),

        # --- Container onde as curvas dinâmicas irão aparecer ---
        html.H4("Dispositivos no Gráfico:"),
        html.Div(id='dynamic_dist_curve_container', children=[]),

    ]),

    # --- Coluna da Direita: Gráfico ---
    html.Div(style={'width': '53%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[
        html.H4("Gráfico de Coordenação (TCC)"),
        dcc.Graph(id='dist_tcc_graph')
    ])
])
# --- [FIM] Layout da Aba 9 ---