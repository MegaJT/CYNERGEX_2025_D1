import dash
from dash import html

dash.register_page(__name__, path='/social', title='Social Media', order=4)

layout = html.Div([
    html.H1("Social Media Dashboard"),
    html.P("This page is under development. Content for Social Media will be displayed here.")
])
