import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from helper import load_data,generate_card, create_bar_chart, create_metric_chart,create_month_filter,create_title

dash.register_page(__name__, path='/contact', title='Contact Centre', order=2)

# Try to load data

df=load_data(r'S_CONTACT_CENTRE CSV.csv',segment='Contact Centre')

def safe_round_mean(series):
    series = pd.to_numeric(series, errors='coerce')
    mean_val = series.mean()  # Returns NaN if all values are NaN
    return 0 if pd.isna(mean_val) else round(mean_val)    



layout = html.Div([
    html.Div(id='contact-trigger', style={'display': 'none'}),

    create_month_filter(df, column_name='WAVE', id_prefix='contact-'),
    create_title("Direct Contact Centre Evaluation",'visit-count-cc'),
    # # Cards section
    html.Div(id='cards-container_cc', className='card-container'),
    
    # Charts section
    html.Div(id='charts-container_cc', className='chart-grid')
])

@callback(
    Output('visit-count-cc', 'children'),
    Input('contact-month-dropdown', 'value')
)
def update_visit_count_cc(month):
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]    
    # Get the count of records
    visit_count = len(filtered_df) if not filtered_df.empty else 0
    
    return f"Base: {visit_count} Visits"
    
    

# Callbacks for updating cards and charts based on filters
@callback(
    Output('cards-container_cc', 'children'),
    Input('contact-month-dropdown', 'value')
)
def update_cards_cc(month):
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]    
    
    
    
    overall_score = safe_round_mean(filtered_df['wOverallScore']) if not filtered_df.empty and 'wOverallScore' in filtered_df.columns else 0
    initial_greet_score =safe_round_mean(filtered_df['wGREETING']) if not filtered_df.empty and 'wGREETING' in filtered_df.columns else 0
    agent_greet_score =safe_round_mean(filtered_df['wAGENTGREETING']) if not filtered_df.empty and 'wAGENTGREETING' in filtered_df.columns else 0
    agent_ineraction_score =safe_round_mean(filtered_df['wINTERACTION']) if not filtered_df.empty and 'wINTERACTION' in filtered_df.columns else 0
    impression_score =safe_round_mean(filtered_df['wIMPRESSION']) if not filtered_df.empty and 'wIMPRESSION' in filtered_df.columns else 0

    
    # Create cards
    card1 = generate_card('OVERALL SCORE', overall_score, "fas fa-certificate")
    card2 = generate_card('INITIAL GREETING', initial_greet_score, "fas fa-handshake")
    card3 = generate_card('CALL AGENT GREETING', agent_greet_score, "fas fa-handshake")
    card4 = generate_card('SALES CONSULTANT INTERACTION', agent_ineraction_score, "fas fa-users")
    card5 = generate_card('OVERALL IMPRESSION', impression_score, "fas fa-crown")
    
    
    
    if not filtered_df.empty:
            return [card1, card2, card3, card4, card5]
    else:
            return[html.H1("No Data Available")]

@callback(
    Output('charts-container_cc', 'children'),
    Input('contact-month-dropdown', 'value')

)
def update_charts_cc(month):
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]   
    
    
    
    INITIAL_GREET_METRICS = {
        'iQ1a': 'Call attempts',
        'iQ1b': 'Call back time',
    }    


    # For impression metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INITIAL_GREET_METRICS,
    chart_title="INITIAL GREETING"
    )

    AGENT_GREET_METRICS = {
    'iQ2b': 'Background noise level',
    'iQ2c': 'Greeting quality',
    'iQ2d': 'Agent attentiveness',
    'iQ2e': 'Agent personalization.',
    'iQ2f': 'Agent manner',
    'iQ2g': "Agent communication clarity",
    'iQ2h':"Agent inquiries",
    'iQ2i_1':"Agent actions",
    'iQ2i_2':"Agent action recorded",
    'iQ2k_1':"Agent appointment confirmation",
    'iQ2l':"Appointment confirmation received",
    'iQ2m':"Average call duration",

    }


    # For initial greet metrics
    ch_agent_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=AGENT_GREET_METRICS,
    chart_title="CALL AGENT GREETING"
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
    chart_title="SALES CONSULTANT INTERACTION"
    )



    IMPRESSION_METRICS = {
    'iQ5a':"Follow-up call received.",
    'iQ5b':"Follow-up call timing.",
    'iQ5e':"Overall experience.",

        }

       
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=IMPRESSION_METRICS,
    chart_title="OVERALL IMPRESSION"
    )
    
    
    # Create charts
    charts = [ch_initial_greet,ch_agent_greet,ch_interaction,ch_impression]

    
    
    if not filtered_df.empty:
        return charts
    else:
        return[]