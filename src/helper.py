import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np


Month_Dict={1:'March-2025',2:'April-2025',3:'May-2025',4:'June-2025',5:'July-2025',6:'August-2025',7:'September-2025',8:'October-2025',9:'November-2025',10:'December-2025',11:'January-2025',12:'February-2025',13:'March-2025',14:'April-2026'}

def load_data(data_file,segment):
    df = pd.read_csv(data_file,index_col=False)
    df = df.replace(r'^\s*$', np.nan, regex=True)  # Replace empty strings with NaN

    if segment == 'Branch':
        try:
            df['Branch'] = df['Branch'].map({1: 'Dubai', 2: 'Sharjah', 3: 'Abu Dhabi'})  # Map branch numbers to names
            df['NATIONALITY'] = df['NATIONALITY'].map({1: 'Emarati', 2: 'Non-Emarati'})  # Map branch numbers to names
            df['Q1_1'] = df['Q1_1'].map({1: 'Social Media Lead', 2: 'Website Visit Lead', 3: 'Call Centre Lead', 4: 'Walkin Customer'})  # Map branch numbers to names
            df['WAVE'] = df['WAVE'].map(Month_Dict)  # Map branch numbers to names
        except:
            df = pd.DataFrame()  # Create empty dataframe if file not found

    if segment == 'Contact Centre':
        try:
            df['WAVE'] = df['WAVE'].map(Month_Dict)  # Map branch numbers to names
        except:
            df = pd.DataFrame()  # Create empty dataframe if file not found
    
    if segment == 'Social Media':
        try:
            df['WAVE'] = df['WAVE'].map(Month_Dict)  # Map branch numbers to names
        except:
            df = pd.DataFrame()  # Create empty dataframe if file not found
    
    if segment == 'Website':
        try:
            df['WAVE'] = df['WAVE'].map(Month_Dict)  # Map branch numbers to names
        except:
            df = pd.DataFrame()  # Create empty dataframe if file not found
                
    
    return df




def create_month_filter(df, column_name='WAVE', id_prefix=''):
    
    if not df.empty and column_name in df.columns:
        unique_values = sorted([val for val in df[column_name].unique() if pd.notna(val)])
        options = [{'label': 'Overall', 'value': 'Overall'}] + [
            {'label': val, 'value': val} for val in unique_values
        ]
    else:
        options = [{'label': 'Overall', 'value': 'Overall'}]
    
    # Create the component
    return html.Div([
        html.Label("Month"),
        dcc.Dropdown(
            id=f'{id_prefix}month-dropdown',
            options=options,
            value=Month_Dict[1],
            multi=True,
            clearable=False
        )
    ], className='filter-item')

def create_title(title):

    return  html.Div([
                html.H3(title),
                html.Div(id='visit-count'),
                html.Div([
                    html.Div([
                        html.Div(className="legend-color legend-low"),
                        html.Span("Below 50", className="legend-text")
                    ], className="legend-item"),
                    html.Div([
                        html.Div(className="legend-color legend-medium"),
                        html.Span("50-74", className="legend-text")
                    ], className="legend-item"),
                    html.Div([
                        html.Div(className="legend-color legend-high"),
                        html.Span("75+", className="legend-text")
                    ], className="legend-item"),
                ], className="score-legend")
            ], className="title")
            

# Helper functions
def generate_card(title, score, icon_type):
     # Determine color class based on value
    if score < 50:
        color_class = "card-score-low"
        card_class = "card card-low"
    elif score < 75:
        color_class = "card-score-medium"
        card_class = "card card-medium"
    else:
        color_class = "card-score-high"
        card_class = "card card-high"

    return html.Div([
        html.I(className=f"{icon_type} card-bg-icon"),
        html.Div(title, className='card-title'),
        html.Hr(),
        html.Div(score, className=f'card-body {color_class}'),
        #html.Div(style={}),
    ], className=card_class)

def create_bar_chart(title, values, labels):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=labels,
            x=values,
            orientation='h',
            marker=dict(
                color='#9d3834',
                line_color='#9d3834',
                line_width=4,
                opacity=0.4
            ),
            width=0.6,
            text=values,
            textposition='auto',
            textangle=0,
            textfont=dict(size=16)
        )
    )
    
    fig.update_layout(
        template='plotly_white',
        title=title,
        title_x=0.5,
        title_font_size=22,
        title_font_family="Jost, sans-serif",
        font_family="Jost, sans-serif",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True, 
            gridwidth=0.5, 
            gridcolor='#f0f0f0',
            range=[0, 100]
        ),
        yaxis=dict(
            showgrid=False,
            autorange="reversed"  # <-- Fixes reverse order
        ),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dcc.Graph(figure=fig, id=f"chart-{title.lower().replace(' ', '-')}")
    ], className='chart-container')

#Chart Calcuation      
def create_metric_chart(filtered_df, metrics_dict, chart_title):
    """
    Creates a bar chart from DataFrame columns with robust error handling.
    
    Args:
        filtered_df (pd.DataFrame): Input data
        metrics_dict (dict): Dictionary of {column_name: label}
        chart_title (str): Title for the chart
    
    Returns:
        A Dash/Plotly chart component
    """
    values = []
    for col in metrics_dict.keys():
        if col not in filtered_df:
            values.append(0)
            continue
            
        try:
            # Convert column to numeric, coercing errors to NaN
            numeric_series = pd.to_numeric(filtered_df[col], errors='coerce')
            # Calculate mean, skipping NaN values
            mean_val = numeric_series.mean(skipna=True)
            values.append(round(mean_val) if not pd.isna(mean_val) else 0)
        except:
            values.append(0)
    
    return create_bar_chart(
        title=chart_title,
        values=values,
        labels=list(metrics_dict.values())
    )
    