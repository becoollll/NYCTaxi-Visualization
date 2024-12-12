# components/numerical_plots.py
from dash import html, dcc, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data_manager import get_data
from dash.dependencies import Input, Output
import dash

color_palette1 = ['#47A0A9', '#94C81A', '#FFBF33', '#FF7636', '#2D4ECD', '#45D6FF']
color_palette2 = ['rgba(133, 191, 198, 0.7)', 'rgba(183, 218, 102, 0.7)', 'rgba(255, 212, 119, 0.7)', 'rgba(255, 164, 121, 0.7)']

def create_peak_summary(data):
    # datetime info
    data = data.copy()
    data['hour'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.hour
    data['date'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.date
    data['weekday'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.day_name()
    
    # avg hourly peaks
    hourly_trips = data.groupby('hour').size()
    days = len(data['date'].unique())
    avg_hourly_trips = hourly_trips / days
    peak_hours = avg_hourly_trips.nlargest(3)
    
    # avg daily peaks
    weekday_trips = data['weekday'].value_counts()
    total_weeks = len(data['tpep_pickup_datetime'].dt.isocalendar().week.unique())
    avg_weekday_trips = weekday_trips / total_weeks
    peak_days = avg_weekday_trips.nlargest(3)
    
    # summary table
    summary_table = html.Table([
        html.Tr([
            html.Th("Rank", style={'width': '10%'}),
            html.Th("Peak Hours", style={'width': '40%'}),
            html.Th("Peak Days", style={'width': '40%'})
        ]),
        *[html.Tr([
            html.Td(f"#{i+1}"),
            html.Td(f"{peak_hours.index[i]}:00 ({peak_hours.values[i]:,.0f} avg trips)"),
            html.Td(f"{peak_days.index[i]} ({peak_days.values[i]:,.0f} avg trips)")
        ]) for i in range(3)]
    ], style={
        'width': '80%',
        'margin': '20px auto',
        'borderCollapse': 'collapse',
        'border': '1px solid #ddd',
        'textAlign': 'center'
    })
    
    summary_stats = {
        'total_trips': len(data),
        'total_days': days,
        'avg_daily_trips': len(data) / days
    }
    
    summary_text = [
        html.Div([
            html.P([
                f"Analysis of {summary_stats['total_trips']:,} trips over {summary_stats['total_days']} days ",
                f"(average {summary_stats['avg_daily_trips']:.0f} trips per day) reveals distinct temporal patterns:"
            ]),
            html.Ul([
                html.Li("Peak Hours: Evening rush hour (5-7 PM) show highest activity"),
                html.Li("Weekend vs Weekday: Weekdays consistently show higher trip volumes than weekends"),
                html.Li("Daily Pattern: Trip volume gradually increases throughout the day, peaks during rush hours")
            ])
        ], style={'marginBottom': '20px'})
    ]
    
    return html.Div([*summary_text, summary_table])


def create_time_analysis(data):
    data = data.copy()
    data['hour'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.hour
    data['weekday'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.day_name()
    data['date'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.date
    
    # Calculate average hourly trips
    hourly_trips = data.groupby('hour').size()
    days = len(data['date'].unique())
    avg_hourly_trips = hourly_trips / days
    
    # Average weekday trips
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_trips = data['weekday'].value_counts()
    weekday_trips = weekday_trips.reindex(weekday_order)
    total_weeks = len(data['tpep_pickup_datetime'].dt.isocalendar().week.unique())
    avg_weekday_trips = weekday_trips / total_weeks
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            'Average Hourly Trip Distribution',
            'Average Daily Trips by Weekday'
        ),
        vertical_spacing=0.15
    )
    
    # hourly average
    fig.add_trace(
        go.Bar(
            x=avg_hourly_trips.index,
            y=avg_hourly_trips.values,
            name='Average Trips per Hour',
            marker_color=color_palette1[0],
            hovertemplate="Hour: %{x}:00<br>Avg Trips: %{y:,.0f}<extra></extra>",
            showlegend=False,
        ),
        row=1, col=1,
    )
    
    # weekdays
    fig.add_trace(
        go.Bar(
            x=weekday_order,
            y=avg_weekday_trips.values,
            name='Average Daily Trips',
            marker_color=color_palette1[1],
            hovertemplate="Day: %{x}<br>Average Trips: %{y:,.0f}<extra></extra>",
            showlegend=False
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title={
            'text': "Temporal Patterns Analysis",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(family='serif', color='blue', size=24),
        title_font_weight='bold'
    )
    
    fig.update_xaxes(
        title_text="Hour of Day",
        tickmode='linear',
        tick0=0,
        dtick=1,
        ticktext=[f"{hour}:00" for hour in range(24)],
        tickvals=list(range(24)),
        row=1, col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    
    fig.update_xaxes(
        title_text="Day of Week",
        tickangle=0,
        row=2, 
        col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    
    fig.update_yaxes(
        title_text="Average Number of Trips per Hour", 
        tickformat=",d", 
        row=1, 
        col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_yaxes(
        title_text="Average Number of Trips per Day", 
        tickformat=",d", 
        row=2, 
        col=1,
        title_font=dict(family='serif', color='darkred', size=18),
    )

    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family='serif', color='blue', size=22)
    
    return fig

def create_fare_analysis(data):
    sampled_data = data.sample(n=min(10000, len(data)), random_state=42)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Total Amount vs Distance',
            'Fare Amount vs Distance',
            'Tip Amount vs Distance',
            'Tolls Amount vs Distance'
        )
    )
    
    features = ['total_amount', 'fare_amount', 'tip_amount', 'tolls_amount']
    positions = [(1,1), (1,2), (2,1), (2,2)]
    colors = color_palette2
    colors_line = color_palette1
    
    for feature, pos, color, line_color in zip(features, positions, colors, colors_line):
        # scatter plot
        fig.add_trace(
            go.Scatter(
                x=sampled_data['trip_distance'],
                y=sampled_data[feature],
                mode='markers',
                marker=dict(
                    color=color,
                    size=5,
                    opacity=0.5
                ),
                name=feature,
                showlegend=False
            ),
            row=pos[0], col=pos[1]
        )
        
        # regression line
        coeffs = np.polyfit(sampled_data['trip_distance'], sampled_data[feature], 1)
        line_x = np.array([sampled_data['trip_distance'].min(), sampled_data['trip_distance'].max()])
        line_y = coeffs[0] * line_x + coeffs[1]
        
        fig.add_trace(
            go.Scatter(
                x=line_x,
                y=line_y,
                mode='lines',
                name=f'{feature} trend',
                line=dict(color=line_color, width=2),
                showlegend=False
            ),
            row=pos[0], col=pos[1]
        )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Fare Components Analysis",
        title_font=dict(family='serif', color='blue', size=24),
        title_font_weight='bold',
        title_x=0.5
    )
    
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(
                title_text="Trip Distance (miles)", 
                row=i, col=j,
                title_font=dict(family='serif', color='darkred', size=18)
            )
            fig.update_yaxes(
                title_text="Amount ($)", 
                row=i, col=j,
                title_font=dict(family='serif', color='darkred', size=18)
            )

    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family='serif', color='blue', size=20)
    
    return fig


def create_distance_analysis(data):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            'Trip Distance Distribution',
            'Average Fare by Distance Range'
        )
    )
    
    fig.add_trace(
        go.Histogram(
            x=data['trip_distance'],
            name='Trip Distance',
            marker_color=color_palette1[0],
            nbinsx=30,
            hovertemplate="Distance: %{x:.1f} miles<br>Count: %{y}<extra></extra>"
        ),
        row=1, col=1
    )
    
    # avg fare by distance range
    distance_bins = pd.cut(data['trip_distance'], bins=10)
    avg_fare = data.groupby(distance_bins, observed=True)['total_amount'].mean()
    
    fig.add_trace(
        go.Bar(
            x=[f"{int(i.left)}-{int(i.right)} miles" for i in avg_fare.index],
            y=avg_fare.values,
            name='Avg Fare',
            marker_color=color_palette1[1],
            hovertemplate="Distance: %{x}<br>Avg Fare: $%{y:.2f}<extra></extra>"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400, 
        showlegend=False,
        title_font=dict(family='serif', color='blue', size=24)
    )
    fig.update_xaxes(
        title_text="Trip Distance (miles)", 
        row=1, col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_xaxes(
        title_text="Distance Range", 
        row=1, col=2,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_yaxes(
        title_text="Number of Trips", 
        row=1, col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_yaxes(
        title_text="Average Fare ($)", 
        row=1, col=2,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family='serif', color='blue', size=20)
    
    return fig


def create_passenger_analysis(data):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            'Passenger Count Distribution',
            'Average Fare by Passenger Count'
        )
    )
    
    # passenger count
    passenger_counts = data['passenger_count'].value_counts().sort_index()
    fig.add_trace(
        go.Bar(
            x=passenger_counts.index,
            y=passenger_counts.values,
            name='Passenger Count',
            marker_color=color_palette1[2],
            hovertemplate="Passengers: %{x}<br>Trips: %{y}<extra></extra>"
        ),
        row=1, col=1
    )
    
    # avg fare by passenger count
    avg_fare = data.groupby('passenger_count')['total_amount'].mean().sort_index()
    fig.add_trace(
        go.Bar(
            x=avg_fare.index,
            y=avg_fare.values,
            name='Avg Fare',
            marker_color=color_palette1[3],
            hovertemplate="Passengers: %{x}<br>Avg Fare: $%{y:.2f}<extra></extra>"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400, 
        showlegend=False,
        title_font=dict(family='serif', color='blue', size=24)
    )
    fig.update_xaxes(
        title_text="Number of Passengers", 
        row=1, col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_xaxes(
        title_text="Number of Passengers", 
        row=1, col=2,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_yaxes(
        title_text="Number of Trips", 
        row=1, col=1,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    fig.update_yaxes(
        title_text="Average Fare ($)", 
        row=1, col=2,
        title_font=dict(family='serif', color='darkred', size=18)
    )
    
    # 更新子圖標題字型
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family='serif', color='blue', size=20)
    
    return fig
def layout_setting():
    data = get_data('final')
    
    return html.Div([
        html.H1("Numerical Features Analysis", style={'textAlign': 'center'}),
        
        html.Div([
            html.Div([
                html.P("Select Analysis Type"),
                dcc.Dropdown(
                    id='analysis-type',
                    options=[
                        {'label': 'Temporal Patterns', 'value': 'temporal'},
                        {'label': 'Fare Components', 'value': 'fare'},
                        {'label': 'Trip Distance Analysis', 'value': 'distance'},
                        {'label': 'Passenger Analysis', 'value': 'passenger'}
                    ],
                    value='temporal',
                    style={'marginBottom': '20px'}
                ),
            ]),

            # content div
            html.Div(id='analysis-content')
            
        ], style={
            'margin': '3%',
            'marginLeft': '20%',
            'marginRight': '20%',
            'padding': '2%',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
    ])

layout = layout_setting()

@callback(
    Output('analysis-content', 'children'),
    Input('analysis-type', 'value')
)

def update_analysis(analysis_type):
    if not analysis_type:
        return dash.no_update
    
    data = get_data('final')
    
    if analysis_type == 'temporal':
        time_insights = html.Div([
            html.H3("Temporal Pattern Analysis", style={'textAlign': 'center'}),
            html.P("Two temporal distribution:"),
            html.Ul([
                html.Li("Hourly Trip Distribution: Shows the number of trips per hour of the day"),
                html.Li("Daily Trip Count: Shows the number of trips per day of the week"),
                ], style={'marginBottom': '20px'})
        ])
        
        return html.Div([
            time_insights,
            dcc.Graph(figure=create_time_analysis(data)),
            html.Hr(),
            html.Div([
                html.H3("Peak Hours and Days Summary", style={'textAlign': 'center', 'marginTop': '30px'}),
                create_peak_summary(data)
            ])
        ])
    
    elif analysis_type == 'fare':
        fare_insights = html.Div([
            html.H3("Fare Component Analysis", style={'textAlign': 'center'}),
            html.P([
                "Analysis based on 10,000 randomly sampled trips reveals:"
            ]),
            html.Ul([
                html.Li("Total Amount vs Distance: Strong positive correlation reflecting base fare plus distance-based pricing"),
                html.Li("Tips: Moderate positive correlation with trip distance, suggesting longer trips tend to receive higher tips"),
                html.Li("Tolls: Weak correlation with distance, indicating toll charges depend more on route choice than distance"),
                html.Li("Base Fare: Visible as the y-intercept in the regression lines, showing minimum charge per trip")
            ], style={'marginBottom': '20px'})
        ])
        
        return html.Div([
            fare_insights,
            dcc.Graph(figure=create_fare_analysis(data))
        ])
        
    elif analysis_type == 'distance':
        distance_insights = html.Div([
            html.H3("Trip Distance Analysis", style={'textAlign': 'center'}),
            html.P([
                "Analysis of trip distances and their relationship with fares:"
            ]),
            html.Ul([
                html.Li("Distance Distribution: Shows the most common trip distances and identifies any unusual patterns"),
                html.Li("Fare Relationship: Demonstrates how fares increase with distance, helping understand pricing structure")
            ], style={'marginBottom': '20px'})
        ])
        
        return html.Div([
            distance_insights,
            dcc.Graph(figure=create_distance_analysis(data))
        ])
        
    else:  # passenger analysis
        passenger_insights = html.Div([
            html.H3("Passenger Count Analysis", style={'textAlign': 'center'}),
            html.P([
                "Analysis of passenger counts and their impact on fares:"
            ]),
            html.Ul([
                html.Li("Passenger Distribution: Shows the typical number of passengers per trip"),
                html.Li("Fare Impact: Illustrates how the number of passengers affects the total fare")
            ], style={'marginBottom': '20px'})
        ])
        
        return html.Div([
            passenger_insights,
            dcc.Graph(figure=create_passenger_analysis(data))
        ])