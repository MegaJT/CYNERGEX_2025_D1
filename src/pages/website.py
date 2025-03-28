import dash
from dash import html

dash.register_page(__name__, path='/website', title='Website', order=3)

layout = html.Div([
    html.H1("Website Dashboard"),
    html.P("This page is under development. Content for Website will be displayed here.")
])
