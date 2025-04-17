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
    facility_around_score =round(filtered_df['wFacility'].mean()) if not filtered_df.empty else 0
    follow_up_score =round(filtered_df['wFollowup'].mean()) if not filtered_df.empty else 0
    
    # Create cards
    card1 = generate_card('OVERALL BRANCH EVALUATION', overall_score, "fas fa-certificate")
    card2 = generate_card('1️ FACILITY AROUND THE SHOWROOM', facility_around_score, "fas fa-phone")
    card3 = generate_card('2️ INITIAL GREET', initial_greet_score, "fas fa-handshake")
    card4 = generate_card('3️ SALES CONSULTANT INTERACTION', interaction_score, "fas fa-users")
    card5 = generate_card('4️ SALES CONSULTANT’S KNOWLEDGE', knowledge_score, "fas fa-brain")
    card6 = generate_card('5️ CLOSING / FINANCE PROCESS / DOCUMENTATION ', closing_score, "fas fa-xmark")
    card7 = generate_card('6️ FACILITY ENVIORNMENT', facility_score, "fas fa-city")
    card8 = generate_card('7️ POST VISIT COMMUNICATION/FOLLOW UP', follow_up_score, "fas fa-phone")
    card9 = generate_card('8️ OVERALL IMPRESSION', impression_score, "fas fa-crown")
    
    
    if not filtered_df.empty:
        
        return [card1, card2, card3, card4, card5, card6, card7, card8, card9]
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
        "iQ7a":"Q7a.Overall Experience",
        "iQ7c":"Q7c.Overall Sales Process",
        "iQ7d":"Q7d.Was SC convincing and logical?",
        "iQ7f":"Q7f.Likelihood to return to delarship",
        
    }


    # For impression metrics
    ch_impression = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=IMPRESSION_METRICS,
    chart_title="8️ OVERALL IMPRESSION"
    )

    FACILITY_AROUND_METRICS = {
    "iQ1a":"Q1a.Parking Guidance - Appointment Customers",
    "iQ1b":"Q1b.Parking Guidance - Walking Customers",
    "iQ1c":"Q1c.Parking Availability",

    }


    # For impression metrics
    ch_facility_around = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict= FACILITY_AROUND_METRICS,
    chart_title="1️ FACILITY AROUND THE SHOWROOM"
    )



    INITIAL_GREET_METRICS = {
    "iQ2a":"Q2a.Person to greet at desk",
    "iQ2b":"Q2b.Time taken to greet",
    "iQ2c":"Q2c.Reasons for delay",
    "iQ2d":"Q2d.Was Greeted or Not",
    "iQ2e":"Q2e.Greeting with Smile / Gratitude",
    "iQ2f":"Q2f.Sales Consultant Appearance",

    }


    # For initial greet metrics
    ch_initial_greet = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INITIAL_GREET_METRICS,
    chart_title="2️ INITIAL GREET"
    )


    INTERACTION_METRICS = {
    "iQ3a":"Q3a.SC's Manners throughout discussion",
    "iQ3b":"Q3b.Did SC Recheck/confirm the customer details - Appointment Customers",
    "iQ3c":"Q3c.Did SC ask personal information? - Walking Customers",
    "iQ3d":"Q3d.Did SC Personalise the Discussion",
    "iQ3d_11":"Q3d_11.SC asked source of information for Chery",
    "iQ3e":"Q3e.SC asked the qualifications questions?",
    "iQ3f":"Q3f.Did SC asked all required information from customer?",
    "iQ3g":"Q3g.Did SC offer water/beverage?",
    "iQ3i":"Q3i.SC's attentiveness",
    "iQ3j":"Q3j.Did SC convince to buy early?",
    "iQ3k":"Q3k.Did SC asked Spouse Preference?",
    "iQ3l":"Q3l.Did SC Summarize customer needs",
    "iQ3m":"Q3m.SC's frendiliness ",
    "iQ3n":"Q3n.Did SC offer Business Card?",

    }


    ch_interaction = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=INTERACTION_METRICS,
    chart_title="3️ SALES CONSULTANT INTERACTION'"
    )



    KNOWLEDGE_METRICS = {
    "iQ4a":"Q4a.Did SC Stated Advance vs. Comp.?",
    "iQ4b":"Q4b.SC's Manners  in Explanation",
    "iQ4c":"Q4c.DiD SC explained all features/brochure/other information?",
    "iQ4d":"Q4d.Did SC built Trust?",
    "iQ4e":"Q4e.Was SC logical and sensible?",
    "iQ4f":"Q4f.Did SC offer Test Drive?",
    "iQ4g":"Q4g.Did SC convince for Test Drive?",
    "iQ4h":"Q4h.SC's clarity about vehicle's immediate availability",
    "iQ4i":"Q4i.Did SC explain the booking process?",

        }

       
    ch_knowledge = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=KNOWLEDGE_METRICS,
    chart_title="4️ SALES CONSULTANT’S KNOWLEDGE"
    )
    
    
    CLOSING_METRICS = {
    "iQ5a":"Q5a.Did SC promoted service department?",
    "iQ5b":"Q5b.Did SC explain vehicle pricing?",
    "iQ5c":"Q5c.Did SC explain values of freebies/offers?",
    "iQ5d":"Q5d.SC's clarifies on Bank/Finance eligibility",
    "iQ5e":"Q5e.Did SC explain the finance/lease/promotional offers",
    "iQ5f":"Q5f.Did SC give reasons for no finance eligibility?",
    "iQ5g":"Q5g.How SC respond in case of object to buy Chery",
    "iQ5h":"Q5h.Did SC close conversation in positive way?",

    }

    ch_closing = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=CLOSING_METRICS,
    chart_title="5️ CLOSING / FINANCE PROCESS / DOCUMENTATION "
    )

    FACILITY_METRICS = {
    "iQ6a":"Q6a.Appearance of sales area",
    "iQ6c":"Q6c.Visible Amenities",
    "iQ6d":"Q6d.Appearance of seating area",
    "iQ6e":"Q6e.Toliet Facilities",
    "iQ6f":"Q6f.Car Display Quality",
    "iQ6g":"Q6g.Vehicle Inventory at Showroom",

    }

    ch_facility = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=FACILITY_METRICS,
    chart_title="6️ FACILITY ENVIORNMENT"
    )

    FOLLOWUP_METRICS = {
    "iQ8a":"Q8a.Did SC followup?",
    "iQ8b":"Q8b.Time taken for followup",
    "iQ8c":"Q8c.Closing Conversation of a Followup Call",

    }

    ch_followup = create_metric_chart(
    filtered_df=filtered_df,
    metrics_dict=FOLLOWUP_METRICS,
    chart_title="7️ POST VISIT COMMUNICATION/FOLLOW UP"
    )

    # Create charts
    charts = [ch_facility_around,ch_initial_greet,ch_interaction,ch_knowledge,ch_closing,ch_facility,ch_followup,ch_impression]

    if not filtered_df.empty:
        return charts
    else:
        return []
    
    