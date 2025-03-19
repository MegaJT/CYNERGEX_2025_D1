from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import os
from datetime import timedelta

# Initialize the app
app = Dash(__name__, 
    assets_folder='assets',
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'],
    suppress_callback_exceptions=True
)
server = app.server

# Set the secret key for Flask session
server.secret_key = os.environ.get('SECRET_KEY', 'Welcome101')  # Add this line


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
    '123456': 'user1',
    '654321': 'user2',
    '111111': 'user3',
}
server.config.update(
    PERMANENT_SESSION_LIFETIME=0,
    REMEMBER_COOKIE_DURATION=0
)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# NAVBAR
navbar = html.Div([
    html.Nav([
        html.Ul([
            html.Li([
                html.A("Branch", href="#branch", className="nav-link")
            ]),
            html.Li([
                html.A("Contact Centre", href="#contact", className="nav-link")
            ]),
            html.Li([
                html.A("Website", href="#website", className="nav-link")
            ]),
            html.Li([
                html.A("Social Media", href="#social", className="nav-link")
            ])
        ], className="nav-list")
    ], className="navbar")
], className="nav-container")

#CARDS
def generate_card(title, score,icon_type):
    return html.Div([
        html.I(className=f"{icon_type} card-bg-icon"),
        html.Div(title, className='card-title'),
        html.Hr(),
        html.Div(score,className='card-body'),
    ], className='card')

card1=generate_card('OVERALL' , '100',"fas fa-certificate")
card2=generate_card('IMPRESSION', '80',"fas fa-crown")
card3=generate_card('INITIAL GREET', '25',"fas fa-handshake")
card4=generate_card('INTERACTION', '60',"fas fa-users")
card5=generate_card('KNOWLEDGE', '45',"fas fa-brain")
card6=generate_card('CLOSING', '56',"fas fa-xmark")
card7=generate_card('FACILITY', '78',"fas fa-city")
card8=generate_card('FOLLOW UP', '62',"fas fa-phone")




# CHARTS
def create_horizontal_chart(title, values, labels):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=labels,
            x=values,
            orientation='h',
            marker=dict(
                #color='#4C9AFF',
                color='#9d3834',
                #line_color='#1212e0',
                line_color='#9d3834',
                line_width=4,
                opacity=0.4
            ),
            width=0.6,
            text=values,
            textposition='auto',
            textfont=dict(size=16)
        )
    )
    
    fig.update_layout(
        template='plotly_white',
        title=title,
        title_x=0.5,
        title_font_size=22,
        title_font_family="Jost, sans-serif",
        font_family="Jost, sans-serif",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True, 
            gridwidth=0.5, 
            gridcolor='#f0f0f0',
            range=[0, 100]
        ),
        yaxis=dict(showgrid=False),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dcc.Graph(figure=fig)
    ], className='chart-container')

# Usage example
horizontal_charts = html.Div([
    create_horizontal_chart(
        "IMPRESSION", 
        [75, 82, 90, 65], 
        ['Alambanx', 'creative', 'sudowdo', 'macintosh']

    ),
    create_horizontal_chart(
        "INITIAL GREET", 
        [85, 70, 95, 88], 
        ['Alambanx', 'creative', 'sudowdo', 'macintosh']
    ),
    create_horizontal_chart(
        "INTERACTION", 
        [92, 78, 85, 80,90,50,60,70],
        ['Alambanx', 'creative', 'sudowdo', 'macintosh','sdfds', 'crewerative', 'sudowdosdf', 'macinsdftosh'] 
      
    ),
    create_horizontal_chart(
        "KNOWLEDGE", 
        [88, 93, 75, 85], 
        ['Alambanx', 'creative', 'sudowdo', 'macintosh']
    ),
    create_horizontal_chart(
        "CLOSING", 
        [95, 82, 88, 90], 
        ['Alambanx', 'creative', 'sudowdo', 'macintosh']
    ),
    create_horizontal_chart(
        "FACILITY", 
        [70, 85, 92, 78], 
        ['Alambanx', 'creative', 'sudowdo', 'macintosh']
    )
], className='chart-grid')





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
                placeholder='Enter 6-digit code',
                maxLength=6,
                minLength=6,
                className='login-input'
            ),
            html.Button('Login', id='login-button', className='login-button'),
            html.Div(id='login-error', className='login-error',children='')
        ], className='login-form')
    ], className='login-container')
], className='login-page')


dashboard_layout  = html.Div([
    html.Div([
        html.Img(src='assets/logo2.png',style={'height':'100px'}),
        html.H1('Mystery Shopping Dashboard'),
         ], className='banner'),

    navbar,

    html.Div([
    card1, card2,    card3,    card4,    card5,    card6,    card7,    card8,   ], className='card-container'),

    horizontal_charts,
    
], className='container')



# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/login' or not current_user.is_authenticated:
        return login_layout
    else:
        return dashboard_layout

@app.callback(
    [Output('url', 'pathname'),
     Output('login-error', 'children')],
    Input('login-button', 'n_clicks'),
    State('access-code', 'value'),
    prevent_initial_call=True
)

def login_user_callback(n_clicks, access_code):
    if n_clicks is None:
        return '/login', ''
    
    if access_code in VALID_CODES:
        user_id = VALID_CODES[access_code]
        login_user(User(user_id),remember=False)
        return '/dashboard', ''
    else:
        return '/login', 'Invalid access code. Please try again.'
##########################################



if __name__ == '__main__':
    app.run(debug=True)
