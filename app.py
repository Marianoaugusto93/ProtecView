# Ficheiro: app.py

import dash

# 1. Inicializa a aplicação
app = dash.Dash(__name__)

# 2. CONFIGURAÇÃO CRÍTICA
# Esta linha diz ao Dash para não verificar os IDs dos callbacks
# no momento em que os ficheiros são importados.
# Isto é essencial para aplicações com múltiplos ficheiros (como a nossa),
# onde o layout é definido num ficheiro e os callbacks noutro.
app.config.suppress_callback_exceptions = True