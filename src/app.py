# https://cynergex-2025-d1.onrender.com
# https://api.render.com/deploy/srv-cvdd8q5rie7s739nu5cg?key=m_pjHYUdBEs

from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import os
from datetime import timedelta
import dash
from dash.exceptions import PreventUpdate

pd.set_option('future.no_silent_downcasting', True)


# Initialize the app
app = Dash(__name__, 
    assets_folder='assets',
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'],
    suppress_callback_exceptions=True,
    use_pages=True,  # Enable pages
    
)

server = app.server

# Set the secret key for Flask session
server.secret_key = os.environ.get('SECRET_KEY', 'Welcome101')

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Valid access codes (in a real app, store these securely in a database)
VALID_CODES = {
    '5823': 'Admin',
    '1947': 'Dubai',
    '7365': 'Sharjah',
    '4091': 'Abudhabi',
}

server.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),  # Increase session lifetime
    REMEMBER_COOKIE_DURATION=timedelta(days=1)
)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login layout
login_layout = html.Div([
    html.Div([
        html.Img(src='assets/logo.png', style={'height': '100px'}),
        html.H1('Mystery Shopping Dashboard Login'),
        
    ], className='login-banner'),
    
    html.Div([
        html.Div([
            html.H2('Enter Access Code'),
            dcc.Input(
                id='access-code',
                type='password',
                placeholder='Enter 4-digit code',
                maxLength=4,
                minLength=4,
                className='login-input'
            ),
            html.Button('Login', id='login-button', className='login-button'),
            html.Div(id='login-error', className='login-error',children='')
        ], className='login-form')
    ], className='login-container')
], className='login-page')

# NAVBAR
navbar = html.Div([
    html.Nav([
        html.Ul([
            html.Li([
                dcc.Link("Branch", href="/branch", className="nav-link")
            ]),
            html.Li([
                dcc.Link("Direct Contact Centre", href="/contact", className="nav-link")
            ]),
            html.Li([
                dcc.Link("Website", href="/website", className="nav-link")
            ]),
            html.Li([
                dcc.Link("Social Media", href="/social", className="nav-link")
            ]),
            html.Li([
                html.Button('Logout', id='logout-button', className='logout-button')
            ], style={'marginLeft': 'auto'})
        ], className="nav-list")
    ], className="navbar")
], className="nav-container")

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),  # Changed to refresh=True for better auth handling
    html.Div(id='page-content')
])

# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return login_layout
    
    # User is authenticated, show the requested page
    return html.Div([
        html.Div([
            html.Img(src='assets/logo0.png', style={'height': '100px'}),
            html.H1('Mystery Shopping Dashboard'),
            html.Img(src='assets/CYN_Logo1.png', style={'height': '100px'}),
        ], className='banner'),
        navbar,
        dash.page_container
    ])

@app.callback(
    [Output('url', 'pathname'),
     Output('login-error', 'children')],
    Input('login-button', 'n_clicks'),
    State('access-code', 'value'),
    prevent_initial_call=True
)
def login_user_callback(n_clicks, access_code):
    if n_clicks is None:
        raise PreventUpdate
    
    if access_code in VALID_CODES:
        user_id = VALID_CODES[access_code]
        login_user(User(user_id), remember=True)  # Set remember=True
        return '/branch', ''
    else:
        return '/login', 'Invalid access code. Please try again.'

@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('logout-button', 'n_clicks'),
    prevent_initial_call=True
)
def logout_user_callback(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    
    logout_user()
    return '/login'

if __name__ == '__main__':
    app.run(debug=True)


