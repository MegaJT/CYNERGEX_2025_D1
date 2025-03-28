import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd

# Helper functions
def generate_card(title, score, icon_type):
    return html.Div([
        html.I(className=f"{icon_type} card-bg-icon"),
        html.Div(title, className='card-title'),
        html.Hr(),
        html.Div(score, className='card-body'),
    ], className='card')

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
    