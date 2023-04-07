import dash
import dash_bootstrap_components as dbc


# Import of styles and sources
estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons",'https://use.fontawesome.com/releases/v5.10.2/css/all.css', dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

# App initialization 
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])

# App config
app.config['suppress_callback_exceptions'] = True

# App server initialization 
app.scripts.config.serve_locally = True
server = app.server


# Glass of wine -> "fa-solid fa-wine-glass"
# Bottle of wine -> "fa-solid fa-wine-bottle"
# Factory of wine -> "fa-regular fa-industry-windows"