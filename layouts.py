from dash import dcc, html

# --- Layout da Aba 1: Home ---
layout_home = html.Div(className='module-container', children=[
    html.H2('Bem-vindo ao ProtecView!'),
    html.P('Este é um conjunto de ferramentas de análise de sistemas elétricos de potência.'),
    html.P('Selecione uma das ferramentas nas abas acima para começar.')
])

# --- Layout da Aba 2: Componentes Simétricos ---
layout_sym = html.Div(className='module-container', children=[
    html.H2(children='Calculador de Componentes Simétricos'),
    html.Div(children=[
        html.H4("Entrada: Componentes de Fase"),
        html.Label("Fase A Mag:"), dcc.Input(id='mag_a', value='2.50', type='number', className='DashInput'),
        html.Label(" Âng:"), dcc.Input(id='ang_a', value='0', type='number', className='DashInput', style={'width': 70}),
        html.Br(),
        html.Label("Fase B Mag:"), dcc.Input(id='mag_b', value='3.50', type='number', className='DashInput'),
        html.Label(" Âng:"), dcc.Input(id='ang_b', value='-150', type='number', className='DashInput', style={'width': 70}),
        html.Br(),
        html.Label("Fase C Mag:"), dcc.Input(id='mag_c', value='5.00', type='number', className='DashInput'),
        html.Label(" Âng:"), dcc.Input(id='ang_c', value='-177', type='number', className='DashInput', style={'width': 70}),
        html.Br(), html.Br(),
        html.Button('Calcular Componentes', id='btn_calcular_sym', n_clicks=0, className='DashButton')
    ]),
    html.Hr(),
    html.Div(children=[
        html.H4("Saída: Componentes Simétricos"),
        html.Label("Sequência Zero (V0): "), html.Div(id='out_v0'), html.Br(),
        html.Label("Sequência Positiva (V1): "), html.Div(id='out_v1'), html.Br(),
        html.Label("Sequência Negativa (V2): "), html.Div(id='out_v2')
    ]),
    html.Hr(),
    html.H4("Visualização de Fasores"),
    html.Div(children=[
        html.Div(children=[dcc.Graph(id='phasor-graph-phase')], style={'width': '49%', 'display': 'inline-block'}),
        html.Div(children=[dcc.Graph(id='phasor-graph-symmetrical')], style={'width': '49%', 'display': 'inline-block'})
    ])
])

# --- Layout da Aba 3: Proteção de Distância ---
layout_dist = html.Div(className='module-container', children=[
    html.H2(children='Visualizador de Zonas de Proteção de Distância'),
    html.H4("Linha 1"),
    html.Label("Imp (Ω):"), dcc.Input(id='line1_imp', value='10', type='number', className='DashInput'),
    html.Label(" Âng (°):"), dcc.Input(id='line1_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),
    html.Label("Zona 1 - Mag (Ω):"), dcc.Input(id='line1_z1_imp', value='8', type='number', className='DashInput'),
    html.Label(" Âng (°):"), dcc.Input(id='line1_z1_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),
    html.Label("Zona 2 - Mag (Ω):"), dcc.Input(id='line1_z2_imp', value='12', type='number', className='DashInput'),
    html.Label(" Âng (°):"), dcc.Input(id='line1_z2_ang', value='80', type='number', className='DashInput'),
    html.Br(), html.Br(),
    html.Button('Plotar Zonas', id='btn_plot_zones', n_clicks=0, className='DashButton'),
    html.Hr(),
    dcc.Graph(id='distance-plot-graph')
])

# --- Layout da Aba 4: Curvas TCC ---
layout_tcc = html.Div(className='module-container', children=[
    html.H2(children='Curvas de Característica Tempo-Corrente (TCC)'),
    html.P("Nota: As curvas SEL U3/U4 da imagem são proprietárias. Usamos curvas IEC como exemplo."),
    html.H4("Relé 1 (Montante)"),
    html.Label("Tipo de Curva:"),
    dcc.Dropdown(id='tcc_r1_type', options=['IEC Standard Inverse', 'IEC Very Inverse', 'IEC Extremely Inverse'], value='IEC Standard Inverse', className='DashDropdown'),
    html.Br(),
    html.Label("Pickup (A):"),
    dcc.Input(id='tcc_r1_pickup', value='5', type='number', className='DashInput'),
    html.Label("Time Dial (TDS):"),
    dcc.Input(id='tcc_r1_tds', value='7.37', type='number', className='DashInput'),
    html.Br(),
    html.H4("Relé 2 (Jusante)"),
    html.Label("Tipo de Curva:"),
    dcc.Dropdown(id='tcc_r2_type', options=['IEC Standard Inverse', 'IEC Very Inverse', 'IEC Extremely Inverse'], value='IEC Very Inverse', className='DashDropdown'),
    html.Br(),
    html.Label("Pickup (A):"),
    dcc.Input(id='tcc_r2_pickup', value='5', type='number', className='DashInput'),
    html.Label("Time Dial (TDS):"),
    dcc.Input(id='tcc_r2_tds', value='7.75', type='number', className='DashInput'),
    html.Br(), html.Br(),
    html.Label("Corrente de Falta para CTI (A):"),
    dcc.Input(id='tcc_fault_current', value='12.21', type='number', className='DashInput'),
    html.Br(), html.Br(),
    html.Button('Plotar Curvas TCC', id='btn_plot_tcc', n_clicks=0, className='DashButton'),
    html.Hr(),
    html.H4(id='tcc-cti-output'),
    dcc.Graph(id='tcc-graph')
])