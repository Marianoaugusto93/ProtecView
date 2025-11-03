# Ficheiro: app.py
# (Corrigido)

from dash import Dash

# Dash carregará automaticamente qualquer ficheiro .css na pasta 'assets'
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap']

app = Dash(__name__, external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
           # A linha 'html_classes' foi removida
        )

server = app.server