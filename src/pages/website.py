import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from helper import load_data,generate_card, create_bar_chart, create_metric_chart,create_month_filter,create_title
import numpy as np

dash.register_page(__name__, path='/website', title='Website', order=3)


# Try to load data
df=load_data(r'S_WEBSITE_EVAL CSV.csv',segment='Website')



def safe_round_mean(series):
    series = pd.to_numeric(series, errors='coerce')
    mean_val = series.mean()  # Returns NaN if all values are NaN
    return 0 if pd.isna(mean_val) else round(mean_val)


layout = html.Div([
    
    html.Div(id='website-trigger', style={'display': 'none'}),

    create_month_filter(df, column_name='WAVE', id_prefix='website-'),
    create_title("Website Evaluation","visit-count-wb"),
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
    card1 = generate_card('OVERALL WEBSITE EVALUATION', overall_score, "fas fa-certificate")
    card2 = generate_card('1️ WEBSITE FUNCTIONALITY AND DIGITAL RESPONSE', registeringquery_score, "fas fa-file-signature")
    card3 = generate_card('2️ CALL AGENT GREETING', greet_score, "fas fa-handshake")
    card4 = generate_card('3️ SALES CONSULTANT INTERACTION', ineraction_score, "fas fa-users")
    card5 = generate_card('4️ OVERALL IMPRESSION (WEBSITE)', impression_score, "fas fa-crown")
    
    
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
    "iQ1":"Q1.Was Website Functional?",
    "iQ2":"Q2.Features available?",
    "iQ3":"Q3.Enough Information about contacts & locations?",
    "iQ4":"Q4.Section for Brochures/Test Drive /  Quotation",
    "iQ5":"Q5.Request sent successfully?",
    "iQ6":"Q6.Did dealrship contact for test drive?",
    "iQ6_4":"Q6_4.Test Drive Confirmed?",
    "iQ7":"Q7.Brochure download",
    "iQ8":"Q8.Call for quotation?",

    }    


    # For impression metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=REGISTRATION_METRICS,
    chart_title="1️ WEBSITE FUNCTIONALITY AND DIGITAL RESPONSE"
    )

    AGENT_GREET_METRICS = {
    "iQ9b":"Q9b.Backgrpound Noise on Call",
    "iQ9c":"Q9c.Was call agent polite and assisting?",
    "iQ9d":"Q9d.Call Agent Attentiveness",
    "iQ9e":"Q9e.Did Call Agent Personalize Interaction?",
    "iQ9f":"Q9f.Call Agent's Manners",
    "iQ9g":"Q9g.Clarity of Call Agent's communication",
    "iQ9h":"Q9h.Did Call Agent asked relevant information?",
    "iQ9i":"Q9i.Did Call Agent give right information?",
    "iQ9j":"Q9j.Did Call Agent Confirms Appointment?",
    "iQ9k":"Q9k.Did Call Agent asked if appointment date is fine?",
    "iQ2l":"Q2l.Did customer get a confirmation on appointment?",
    "iQ9m":"Q9m.Average time spent on call?",


    }


    # For initial greet metrics
    ch_agent_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=AGENT_GREET_METRICS,
    chart_title="2️ CALL AGENT GREETING"
    )


    INTERACTION_METRICS = {
    "iQ10a":"Q10a.Followup call prior to branch visit",
    "iQ10b":"Q10b.Time taken for followup-call",
    "iQ10d":"Q10d.Did Call Agent give right information?",
    "iQ10e":"Q10e.SC's attentiveness",
    "iQ10f":"Q10f.Did SC summarize the need?",
    "iQ19g":"Q19g.Did SC Personalize the conversation?",
    "iQ10h":"Q10h.SC's manners throughout the interaction",
    "iQ10i":"Q10i.Clarity of SC's communication",

    }


    ch_interaction = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INTERACTION_METRICS,
    chart_title="3️ SALES CONSULTANT INTERACTION"
    )



    IMPRESSION_METRICS = {
    "iQ11a":"Q11a.Follow up prior to branch visit?",
    "iQ11b":"Q11b.Time taken for followup call",
    "iQ11_1":"Q11_1.Was website easy or inconvenient?",
    "iQ11_2":"Q11_2.Overall Experience with Website",


        }

       
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=IMPRESSION_METRICS,
    chart_title="4️ OVERALL IMPRESSION (WEBSITE)"
    )
    
    
    # Create charts
    charts = [ch_initial_greet,ch_agent_greet,ch_interaction,ch_impression]
    
    if not filtered_df.empty:
        return charts
    else:
        return[]