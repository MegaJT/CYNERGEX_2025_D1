import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from helper import load_data,generate_card, create_bar_chart, create_metric_chart,create_month_filter
import numpy as np

dash.register_page(__name__, path='/website', title='Website', order=3)


# Try to load data
df=load_data(r'S_WEBSITE_EVAL CSV.csv',segment='Website')



def safe_round_mean(series):
    series = pd.to_numeric(series, errors='coerce')
    mean_val = series.mean()  # Returns NaN if all values are NaN
    return 0 if pd.isna(mean_val) else round(mean_val)


layout = html.Div([
    html.Div([
        html.H2("Website Evaluation"),
        html.Div(id='visit-count-wb') 
        ], className="title"),

    html.Div(id='website-trigger', style={'display': 'none'}),

    create_month_filter(df, column_name='WAVE', id_prefix='website-'),
    # # Cards section
    html.Div(id='cards-container_ws', className='card-container'),
    
    # Charts section
    html.Div(id='charts-container_ws', className='chart-grid')
])

@callback(
    Output('visit-count-wb', 'children'),
    Input('website-month-dropdown', 'value')
)
def update_visit_count_wb(month):
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
    Output('cards-container_ws', 'children'),
    Input('website-month-dropdown', 'value')
)
def update_cards_ws(month):
    # Filter data based on selections
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]  
    
    
    overall_score = safe_round_mean(filtered_df['wOverallScore']) if not filtered_df.empty and 'wOverallScore' in filtered_df.columns else 0
    registeringquery_score =safe_round_mean(filtered_df['wREGISTERINGQUERY']) if not filtered_df.empty and 'wREGISTERINGQUERY' in filtered_df.columns else 0
    greet_score = safe_round_mean(filtered_df['wGREETING']) if not filtered_df.empty and 'wGREETING' in filtered_df.columns else 0
    ineraction_score =safe_round_mean(filtered_df['wINTERACTION']) if not filtered_df.empty and 'wINTERACTION' in filtered_df.columns else 0
    impression_score =safe_round_mean(filtered_df['wOVERALLIMPRESSION']) if not filtered_df.empty and 'wOVERALLIMPRESSION' in filtered_df.columns else 0
    
    # Create cards
    card1 = generate_card('OVERALL SCORE', overall_score, "fas fa-certificate")
    card2 = generate_card('WEBSITE VISIT AND REGISTERING QUERY', registeringquery_score, "fas fa-file-signature")
    card3 = generate_card('CALL AGENT GREETING', greet_score, "fas fa-handshake")
    card4 = generate_card('SALES CONSULTANT INTERACTION', ineraction_score, "fas fa-users")
    card5 = generate_card('OVERALL IMPRESSION (WEBSITE)', impression_score, "fas fa-crown")
    
    
    if not filtered_df.empty:
            return [card1, card2, card3, card4, card5]
    else:
            return[html.H1("No Data Available")]

@callback(
    Output('charts-container_ws', 'children'),
    Input('website-month-dropdown', 'value')
)
def update_charts_ws(month):
    # Filter data based on selections
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]  
    
    
    
    
    REGISTRATION_METRICS = {
    'iQ1': 'Website navigation',
    'iQ2': 'Functionality checklist',
    'iQ3': 'Website information completeness',
    'iQ4': 'Model availability',
    'iQ5': 'Successful Brochure request',
    'iQ6': 'Response recieved?',
    'iQ6_3': 'Mode of response',
    'iQ6_4': 'Confirm the test drive',
    'iQ7': 'Brochure download',
    'iQ8': 'Quote callback',
    }    


    # For impression metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=REGISTRATION_METRICS,
    chart_title="WEBSITE VISIT AND REGISTERING QUERY"
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
    chart_title="CALL AGENT GREETING"
    )


    INTERACTION_METRICS = {
    'iQ10a':"Sales consultant call received",
    'iQ10b':"Time taken to contact by consultant",
    'iQ10d':"Consultant's actions during interaction",
    'iQ10e':"Consultant's attentiveness level",
    'iQ10f':"Consultant's vehicle recommendation approach",
    'iQ19g':"Consultant's personalization actions",
    'iQ10h':"Consultant's interaction manner",
    'iQ10i':"Consultant's communication clarity",
    }


    ch_interaction = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INTERACTION_METRICS,
    chart_title="SALES CONSULTANT INTERACTION"
    )



    IMPRESSION_METRICS = {
    'iQ11a':"Follow-up call received before appointment",
    'iQ11b':"Follow-up call timing before appointment",
    'iQ11_1':"Website ease of use and navigation",
    'iQ11_2':"Website experience with dealership/brand",

        }

       
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=IMPRESSION_METRICS,
    chart_title="OVERALL IMPRESSION (WEBSITE)"
    )
    
    
    # Create charts
    charts = [ch_initial_greet,ch_agent_greet,ch_interaction,ch_impression]
    
    if not filtered_df.empty:
        return charts
    else:
        return[]