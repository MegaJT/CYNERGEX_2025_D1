import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from helper import load_data,generate_card, create_bar_chart, create_metric_chart,create_month_filter,create_title
import numpy as np



dash.register_page(__name__, path='/social', title='Social Media', order=4)




# Try to load data

df=load_data(r'S_SM_EVAL CSV.csv',segment='Social Media')


def safe_round_mean(series):
    series = pd.to_numeric(series, errors='coerce')
    mean_val = series.mean()  # Returns NaN if all values are NaN
    return 0 if pd.isna(mean_val) else round(mean_val)

layout = html.Div([
    
    html.Div(id='social-trigger', style={'display': 'none'}),


    create_month_filter(df, column_name='WAVE', id_prefix='social-'),
    create_title("Social Media Evaluation",'visit-count-sm'),
# # Cards section
    html.Div(id='cards-container_sm', className='card-container'),
    
    # Charts section
    html.Div(id='charts-container_sm', className='chart-grid')
])

@callback(
    Output('visit-count-sm', 'children'),
    Input('social-month-dropdown', 'value')
)
def update_visit_count_sm(month):
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
    Output('cards-container_sm', 'children'),
    [Input('social-month-dropdown', 'value')]
)
def update_cards_cc(month):
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    # Filter data based on selections
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]    
    
    # Example: overall_score = filtered_df['OVERALL_SCORE'].mean()
    overall_score = safe_round_mean(filtered_df['wOverallScore']) if not filtered_df.empty and 'wOverallScore' in filtered_df.columns else 0
    agent_score = safe_round_mean(filtered_df['wSMAGENTEVAL']) if not filtered_df.empty and 'wSMAGENTEVAL' in filtered_df.columns else 0
    greet_score = safe_round_mean(filtered_df['wGREETING']) if not filtered_df.empty and 'wGREETING' in filtered_df.columns else 0
    interaction_score = safe_round_mean(filtered_df['wINTERACTION']) if not filtered_df.empty and 'wINTERACTION' in filtered_df.columns else 0
    overall_eval_score = safe_round_mean(filtered_df['wOVERALLEVALUATION']) if not filtered_df.empty and 'wOVERALLEVALUATION' in filtered_df.columns else 0
    
    # Create cards
    card1 = generate_card('OVERALL SCORE', overall_score, "fas fa-certificate")
    card2 = generate_card('SOCIAL MEDIA AGENT EVALUATION', agent_score, "fas fa-handshake")
    card3 = generate_card('CALL AGENT GREETING', greet_score, "fas fa-handshake")
    card4 = generate_card('SALES CONSULTANT INTERACTION ', interaction_score, "fas fa-users")
    card5 = generate_card('OVERALL EVALUATION', overall_eval_score, "fas fa-crown")
    
    
    if not filtered_df.empty:
            return [card1, card2, card3, card4, card5]
    else:
            return[html.H1("No Data Available")]

@callback(
    Output('charts-container_sm', 'children'),
    [Input('social-month-dropdown', 'value')]

)
def update_charts_cc(month):
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]    
    

    
    AGENT_METRICS = {
        'iQ1':"Response time DM",
        'iQ2 ':"Public response time",
        'iQ2a':"First response mode",
        'iQ3':"First response type",
        'iQ4':"Agent's response type",
        'iQ5':"Communication clarity",
        'iQ6':"Agent's inquiries",
        'iQ9':"Conversation closure type",
        'iQ9a':"Test drive call received",
    }    


    # For impression metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=AGENT_METRICS,
    chart_title="SOCIAL MEDIA AGENT EVALUATION"
    )

    AGENT_GREET_METRICS = {
    'iQ10b':"Background noise level",
    'iQ10c':"Call greeting type",
    'iQ10d ':"Agent attentiveness level",
    'iQ10e':"Agent personalization actions",
    'iQ10f':"Agent's interaction manner",
    'iQ10g':"Agent's communication clarity",
    'iQ10h':"Agent's questions asked",
    'iQ10i':"Agent's actions taken",
    'iQ10i_1':"Agent's response action",
    'iQ10k':"Agent's appointment confirmation",
    'iQ10l ':"Appointment confirmation received",
    'iQ10m':"Average call duration",


    }


    # For initial greet metrics
    ch_agent_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=AGENT_GREET_METRICS,
    chart_title="CALL AGENT GREETING"
    )


    INTERACTION_METRICS = {
    'iQ11a':"Sales consultant call received",
    'iQ11b':"Time to contact by consultant",
    'iQ11d':"Consultant's actions taken",
    'iQ11e':"Consultant's attentiveness level",
    'iQ11f':"Consultant's vehicle recommendation",
    'iQ11g':"Consultant's personalization actions",
    'iQ11h':"Consultant's interaction manner",
    'iQ11i':"Consultant's communication clarity",


    }


    ch_interaction = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INTERACTION_METRICS,
    chart_title="SALES CONSULTANT INTERACTION"
    )



    OVERALL_METRICS = {
    'iQ12a':"Follow-up call received",
    'iQ12b':"Follow-up call timing",
    'iQ13':"Social media interaction experience",


        }

       
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=OVERALL_METRICS,
    chart_title="OVERALL EVALUATION"
    )
    
    
    # Create charts
    charts = [ch_initial_greet,ch_agent_greet,ch_interaction,ch_impression]

    
    
    if not filtered_df.empty:
        return charts
    else:
        return []
