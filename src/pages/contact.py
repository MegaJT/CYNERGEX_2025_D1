import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from helper import generate_card, create_bar_chart, create_metric_chart

dash.register_page(__name__, path='/contact', title='Contact Centre', order=2)

# Try to load data
try:
    df = pd.read_csv(r'S_CONTACT_CENTRE CSV.csv',index_col=False)
except:
    df = pd.DataFrame()  # Create empty dataframe if file not found



layout = html.Div([
    # html.H1("Contact Centre Dashboard"),
    # html.P("This page is under development. Content for Contact Centre will be displayed here."),
    html.Div(id='contact-trigger', style={'display': 'none'}),
    # # Cards section
    html.Div(id='cards-container_cc', className='card-container'),
    
    # Charts section
    html.Div(id='charts-container_cc', className='chart-grid')
])

# Callbacks for updating cards and charts based on filters
@callback(
    Output('cards-container_cc', 'children'),
    Input('contact-trigger', 'children')
)
def update_cards_cc(_):
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    
    # Example: overall_score = filtered_df['OVERALL_SCORE'].mean()
    overall_score = round(filtered_df['wOverallScore'].mean()) if not filtered_df.empty else 0
    initial_greet_score =round(filtered_df['wGREETING'].mean()) if not filtered_df.empty else 0
    agent_greet_score =round(filtered_df['wAGENTGREETING'].mean()) if not filtered_df.empty else 0
    agent_ineraction_score =round(filtered_df['wINTERACTION'].mean()) if not filtered_df.empty else 0
    impression_score =round(filtered_df['wIMPRESSION'].mean()) if not filtered_df.empty else 0
    
    # Create cards
    card1 = generate_card('OVERALL', overall_score, "fas fa-certificate")
    card2 = generate_card('INITIAL GREET', initial_greet_score, "fas fa-handshake")
    card3 = generate_card('AGENT GREET', agent_greet_score, "fas fa-handshake")
    card4 = generate_card('INTERACTION', agent_ineraction_score, "fas fa-users")
    card5 = generate_card('IMPRESSION', impression_score, "fas fa-crown")
    
    
    return [card1, card2, card3, card4, card5]

@callback(
    Output('charts-container_cc', 'children'),
    Input('contact-trigger', 'children')
)
def update_charts_cc(_):
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    
    
    
    INITIAL_GREET_METRICS = {
        'iQ1a': 'Call attempts',
        'iQ1b': 'Call back time',
    }    


    # For impression metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INITIAL_GREET_METRICS,
    chart_title="INITIAL GREET"
    )

    AGENT_GREET_METRICS = {
    'iQ2b': 'Background noise level',
    'iQ2c': 'Greeting quality',
    'iQ2d': 'Agent attentiveness',
    'iQ2e': 'Agent personalization.',
    'iQ2f': 'Agent manner',
    'iQ2g': "Agent communication clarity",
    'iQ2h':"Agent inquiries.",
    'iQ2i_1':"Agent actions.",
    'iQ2i_2':"Agent action recorded.",
    'iQ2k_1':"Agent appointment confirmation.",
    'iQ2l':"Appointment confirmation received.",
    'iQ2m':"Average call duration.",

    }


    # For initial greet metrics
    ch_agent_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=AGENT_GREET_METRICS,
    chart_title="AGENT GREET"
    )


    INTERACTION_METRICS = {
    'iQ3a':"Sales consultant call received.",
    'iQ3b':"Sales consultant contact time.",
    'iQ3d':"Sales consultant actions.",
    'iQ3e':"Sales consultant attentiveness.",
    'iQ3f':"Sales consultant recommendation.",
    'iQ3g':"Sales consultant personalization.",
    'iQ3h':"Sales consultant manner.",
    'iQ3i':"Sales consultant communication clarity.",

    }


    ch_interaction = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INTERACTION_METRICS,
    chart_title="INTERACTION"
    )



    IMPRESSION_METRICS = {
    'iQ5a':"Follow-up call received.",
    'iQ5b':"Follow-up call timing.",
    'iQ5e':"Overall experience.",

        }

       
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=IMPRESSION_METRICS,
    chart_title="IMPRESSION"
    )
    
    
    # Create charts
    charts = [ch_initial_greet,ch_agent_greet,ch_interaction,ch_impression]

    
    
    return charts