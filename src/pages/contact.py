import dash
from dash import html

dash.register_page(__name__, path='/contact', title='Contact Centre', order=2)

layout = html.Div([
    html.H1("Contact Centre Dashboard"),
    html.P("This page is under development. Content for Contact Centre will be displayed here.")
])
