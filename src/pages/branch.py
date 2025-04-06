import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from helper import load_data,generate_card, create_bar_chart, create_metric_chart,Month_Dict,create_month_filter,create_title
from flask_login import current_user


# Register the page
dash.register_page(__name__, path='/branch', title='Branch', order=1)



# Try to load data
df=load_data(r'S_BRANCH_EVAL CSV.csv',segment='Branch')


# Create a function to get filtered dataframe based on user
def get_user_filtered_df():
    
    filtered_df = df.copy() if not df.empty else pd.DataFrame()
    
    if not filtered_df.empty and current_user.is_authenticated:
        if current_user.id == 'Admin':
            filtered_df = filtered_df
        elif current_user.id == 'Dubai':
            filtered_df = filtered_df[filtered_df['Branch'] == 'Dubai']
        elif current_user.id == 'Sharjah':
            filtered_df = filtered_df[filtered_df['Branch'] == 'Sharjah']
        elif current_user.id == 'Abudhabi':
            filtered_df = filtered_df[filtered_df['Branch'] == 'Abu Dhabi']
    
    return filtered_df

# Layout
def layout():
    user_df = get_user_filtered_df()
    return html.Div([
        # Add this to your branch.py layout, right after the filters-container div
            
        html.Div(id='branch-trigger', style={'display': 'none'}),
        
        html.Div([
            create_month_filter(user_df, column_name='WAVE', id_prefix='branch-'),

            html.Div([
                html.Label("Appointment Type"),
                dcc.Dropdown(
                    id='appointment-type-dropdown',
                    options=[{'label': 'Overall', 'value': 'Overall'}] + 
                            [{'label': val, 'value': val} for val in user_df['Q1_1'].unique() if pd.notna(val)] if not user_df.empty else [],
                    value='Overall',
                    clearable=False
                )
            ], className='filter-item'),
            
            html.Div([
                html.Label("Branch Name"),
                dcc.Dropdown(
                    id='branch-name-dropdown',
                    options=[{'label': 'Overall', 'value': 'Overall'}] + 
                            [{'label': val, 'value': val} for val in user_df['Branch'].unique() if pd.notna(val)] if not user_df.empty else [],
                    value='Overall',
                    clearable=False
                )
            ], className='filter-item'),
            
            html.Div([
                html.Label("MS Nationality"),
                dcc.Dropdown(
                    id='nationality-dropdown',
                    options=[{'label': 'Overall', 'value': 'Overall'}] + 
                            [{'label': val, 'value': val} for val in user_df['NATIONALITY'].unique() if pd.notna(val)] if not user_df.empty else [],
                    value='Overall',
                    clearable=False
                )
            ], className='filter-item'),
        ], className='filters-container'),

        create_title("Branch Evaluation","visit-count-br"),

        # Cards section
        html.Div(id='cards-container_b', className='card-container'),
        
        # Charts section
        html.Div(id='charts-container_b', className='chart-grid')
    ])


@callback(
    Output('visit-count-br', 'children'),
    [Input('appointment-type-dropdown', 'value'),
     Input('branch-name-dropdown', 'value'),
     Input('nationality-dropdown', 'value'),
     Input('branch-month-dropdown', 'value')])

def update_visit_count(appointment_type, branch_name, nationality, month):
    # Filter data based on selections
    filtered_df = get_user_filtered_df()
    
    if not filtered_df.empty:
        if appointment_type != 'Overall':
            filtered_df = filtered_df[filtered_df['Q1_1'] == appointment_type]
            
        if branch_name != 'Overall':
            filtered_df = filtered_df[filtered_df['Branch'] == branch_name]
            
        if nationality != 'Overall':
            filtered_df = filtered_df[filtered_df['NATIONALITY'] == nationality]
            
        if month != 'Overall':
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
    Output('cards-container_b', 'children'),
    [Input('appointment-type-dropdown', 'value'),
     Input('branch-name-dropdown', 'value'),
     Input('nationality-dropdown', 'value'),
     Input('branch-month-dropdown', 'value') ]
)
def update_cards(appointment_type, branch_name, nationality,month):
    # Filter data based on selections
    filtered_df = get_user_filtered_df()
    
    if not df.empty:
        if appointment_type != 'Overall':
            filtered_df = filtered_df[filtered_df['Q1_1'] == appointment_type]
        
        if branch_name != 'Overall':
            filtered_df = filtered_df[filtered_df['Branch'] == branch_name]
        
        if nationality != 'Overall':
            filtered_df = filtered_df[filtered_df['NATIONALITY'] == nationality]
        
        if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]    
    
    
    
    overall_score = round(filtered_df['wOverallScore'].mean()) if not filtered_df.empty else 0
    impression_score = round(filtered_df['wOverallImpression'].mean()) if not filtered_df.empty else 0
    initial_greet_score =round(filtered_df['wInitialgreet'].mean()) if not filtered_df.empty else 0
    interaction_score =round(filtered_df['wCONSULTANTINTERACTION'].mean()) if not filtered_df.empty else 0
    knowledge_score =round(filtered_df['wCONSULTANTKNOWLEDGE'].mean()) if not filtered_df.empty else 0
    closing_score =round(filtered_df['wClosing'].mean()) if not filtered_df.empty else 0
    facility_score =round(filtered_df['wFacilityEnvironment'].mean()) if not filtered_df.empty else 0
    follow_up_score =round(filtered_df['wFollowup'].mean()) if not filtered_df.empty else 0
    
    # Create cards
    card1 = generate_card('OVERALL SCORE', overall_score, "fas fa-certificate")
    card2 = generate_card('OVERALL IMPRESSION', impression_score, "fas fa-crown")
    card3 = generate_card('INITIAL GREET', initial_greet_score, "fas fa-handshake")
    card4 = generate_card('SALES CONSULTANT INTERACTION', interaction_score, "fas fa-users")
    card5 = generate_card('SALES CONSULTANT’S KNOWLEDGE', knowledge_score, "fas fa-brain")
    card6 = generate_card('CLOSING / FINANCE PROCESS / DOCUMENTATION ', closing_score, "fas fa-xmark")
    card7 = generate_card('FACILITY AROUND THE SHOWROOM', facility_score, "fas fa-city")
    card8 = generate_card('POST VISIT COMMUNICATION/FOLLOW UP', follow_up_score, "fas fa-phone")
    
    if not filtered_df.empty:
        return [card1, card2, card3, card4, card5, card6, card7, card8]
    else:
        return[html.H1("No Data Available")]

@callback(
    Output('charts-container_b', 'children'),
    [Input('appointment-type-dropdown', 'value'),
     Input('branch-name-dropdown', 'value'),
     Input('nationality-dropdown', 'value'),
     Input('branch-month-dropdown', 'value') ]
)
def update_charts(appointment_type, branch_name, nationality,month):
    # Filter data based on selections
    filtered_df = get_user_filtered_df()
    
    if not df.empty:
        if appointment_type != 'Overall':
            filtered_df = filtered_df[filtered_df['Q1_1'] == appointment_type]
        
        if branch_name != 'Overall':
            filtered_df = filtered_df[filtered_df['Branch'] == branch_name]
        
        if nationality != 'Overall':
            filtered_df = filtered_df[filtered_df['NATIONALITY'] == nationality]
        
        if month!= 'Overall':
            if isinstance(month, list):
                if 'Overall' not in month:
                    filtered_df = filtered_df[filtered_df['WAVE'].isin(month)]
            else:
                filtered_df = filtered_df[filtered_df['WAVE'] == month]    

    
    IMPRESSION_METRICS = {
        'iQ7a': 'Overall experience description',
        'iQ7c': 'Sales process handling',
        'iQ7d': 'Sales consultant impression',
        'iQ7f': 'Likelihood to return',
        'iQ7g': 'Positive aspects, experience-based',
        'iQ7h': 'Dealership dislikes, experience-based'
    }


    # For impression metrics
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=IMPRESSION_METRICS,
    chart_title="OVERALL IMPRESSION"
    )

    INITIAL_GREET_METRICS = {
    'iQ2a': 'Person at reception desk?',
    'iQ2b': 'Time before greeting?',
    'iQ2c': 'Reason for delay over 5 minutes?',
    'iQ2d': 'Initial greeter',
    'iQ2e': 'Greeting style',
    'iQ2f': "Consultant's appearance"
    }


    # For initial greet metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INITIAL_GREET_METRICS,
    chart_title="INITIAL GREET"
    )


    INTERACTION_METRICS = {
    'iQ3a':"Consultant's demeanor",
    'iQ3b':"Personal information check",
    'iQ3c':"Personal information inquiry",
    'iQ3d':" Personalized discussion actions",
    'iQ3d_1':"Source of information inquiry",
    'iQ3e':"Consultant's actions during interaction",
    'iQ3f':"Consultant's checks during interaction",
    'iQ3g':"Beverage offer",
    'iQ3h':"Information confirmation",
    'iQ3i':"Consultant's attentiveness level",
    'iQ3j':"Consultant's response to delay",
    'iQ3k':"Asked spouse’s preference",
    'iQ3l':"Consultant's vehicle recommendation",
    'iQ3m':"Consultant's friendliness level",
    'iQ3n':"Consultant's business card",
    }


    ch_interaction = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INTERACTION_METRICS,
    chart_title="SALES CONSULTANT INTERACTION'"
    )



    KNOWLEDGE_METRICS = {
    'iQ4a':"Consultant's model comparison",
    'iQ4b':"Consultant's response style",
    'iQ4c':"Consultant's vehicle discussion",
    'iQ4d':"Trust and credibility",
    'iQ4e':"Reasoning for purchase",
    'iQ4f':"Test drive offer",
    'iQ4g':"Consultant's actions",
    'iQ4h':"Consultant's booking response",
    'iQ4i':"Booking assistance provided",
        }

       
    ch_knowledge = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=KNOWLEDGE_METRICS,
    chart_title="SALES CONSULTANT’S KNOWLEDGE"
    )
    
    
    CLOSING_METRICS = {
    'iQ5a':"Service promotion approach",
    'iQ5b':"Pricing information provided",
    'iQ5c':"Consultant's actions",
    'iQ5d':"Eligibility information",
    'iQ5e':"Finance and lease options",
    'iQ5f':"Consultant's objection response",
    'iQ5g':"Sales consultant actions",
    'iQ5h':"Sales area appearance",
    }

    ch_closing = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=CLOSING_METRICS,
    chart_title="CLOSING / FINANCE PROCESS / DOCUMENTATION "
    )

    FACILITY_METRICS = {
    'iQ6a':"Sales area appearance",
    'iQ6c':"Visible sales amenities",
    'iQ6d':"Seating area appearance",
    'iQ6e':"Toilet facilities condition",
    'iQ6f':"Car display quality",
    'iQ6g':"Vehicle inventory selection",
    }

    ch_facility = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=FACILITY_METRICS,
    chart_title="FACILITY AROUND THE SHOWROOM"
    )

    FOLLOWUP_METRICS = {
    'iQ8a':"Sales follow-up?",
    'iQ8b':"Call response time?",
    'iQ8c':"Consultant's post-visit communication?",
    }

    ch_followup = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=FOLLOWUP_METRICS,
    chart_title="POST VISIT COMMUNICATION/FOLLOW UP"
    )

    # Create charts
    charts = [ch_impression,ch_initial_greet,ch_interaction,ch_knowledge,ch_closing,ch_facility,ch_followup]

    if not filtered_df.empty:
        return charts
    else:
        return []
    
    