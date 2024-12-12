# components/outlier.py
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_manager import get_data, get_analysis_results
import dash

def create_box_plot(feature, data, title_prefix=""):
    sampled_data = data.sample(n=min(10000, len(data)), random_state=42)
    
    fig = go.Figure()
    fig.add_trace(
        go.Box(
            y=sampled_data[feature],
            name=feature,
            boxmean=True,
            marker_color='rgb(71, 160, 169)'
        )
    )
    
    fig.update_layout(
        title=f"{title_prefix}Box Plot for {feature}",
        yaxis_title="Value",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False,
        title_font=dict(family='serif', color='blue', size=24),
        title_x=0.5,
        title_font_weight='bold'
    )

    fig.update_xaxes(title_font=dict(family='serif', color='darkred', size=18)),
    fig.update_yaxes(title_font=dict(family='serif', color='darkred', size=18))
    
    return fig

def layout_setting():
    numerical_features = [
        'trip_distance', 'fare_amount', 'total_amount',
        'tip_amount', 'tolls_amount', 'extra', 'mta_tax',
        'improvement_surcharge', 'congestion_surcharge', 'Airport_fee'
    ]
    
    transformed_features = [
        'trip_distance_log', 'fare_amount_log', 'total_amount_log',
        'tip_amount_log', 'tolls_amount_log'
    ]
    
    return html.Div([
        html.H1("Outlier Analysis", style={'textAlign': 'center'}),
        
        html.Div([
            # explanations
            html.Div([
                html.H3("Outlier Detection Method", style={'textAlign': 'center'}),
                html.P([
                    "Given this large dataset of over 3 million records and comprehensive data cleaning process, ",
                    "this program adopt a practical approach to outlier detection:"
                ]),
                html.Ul([
                    html.Li([
                        "Initial data cleaning has already handled invalid and extreme lower bound cases, such as:",
                        html.Ul([
                            html.Li("Negative values in monetary fields"),
                            html.Li("Zero or extremely short trip distances"),
                            html.Li("Invalid time durations")
                        ])
                    ]),
                    html.Li([
                        "Using a simple yet effective approach for upper bound outliers:",
                        html.Ul([
                            html.Li("Use 99th percentile as threshold, which is sufficient given our large sample size")
                        ])
                    ])
                ]),
                html.P([
                    "This approach is particularly suitable because:",
                    html.Br(),
                    "1. With 3M+ records, even retaining 99% of data still gives us a robust sample",
                    html.Br(),
                    "2. Lower bounds are already handled in cleaning stage"
                ])
            ], style={'marginBottom': '30px'}),
            
            # original data box plot
            html.Div([
                html.H2("Original Data Distribution"),
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=[{'label': feature, 'value': feature} 
                            for feature in numerical_features],
                    value=numerical_features[0],
                    style={'marginBottom': '20px'}
                ),
                dcc.Graph(id='box-plot-original'),
            ]),
            
            html.Hr(),
            
            html.Div([
                html.Button(
                    "View Data After Outlier Removal",
                    id='view-transformed-button',
                    n_clicks=0,
                    style={'marginBottom': '20px'}
                ),
            ], style={'textAlign': 'center'}),
            
            html.Div(id='transformed-content', children=[
                html.H2("Distribution After Outlier Removal", style={'display': 'none'}),
                dcc.Dropdown(
                    id='transformed-feature-dropdown',
                    options=[{'label': feature, 'value': feature} 
                            for feature in transformed_features],
                    value=transformed_features[0],
                    style={'display': 'none'}
                ),
                dcc.Graph(id='box-plot-transformed', style={'display': 'none'}),
                html.Div(id='outlier-summary', style={'display': 'none'})
            ]),
            
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
    Output('box-plot-original', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_box_plot(feature):
    if not feature:
        return go.Figure(layout=dict(
            title="Please select a feature to display the box plot",
            xaxis_visible=False,
            yaxis_visible=False
        ))
    
    data = get_data('cleaned')
    return create_box_plot(feature, data)

@callback(
    [Output('transformed-content', 'children'),
     Output('view-transformed-button', 'children')],
    Input('view-transformed-button', 'n_clicks'),
    prevent_initial_call=True
)
def show_transformed_data(n_clicks):
    if n_clicks == 0:
        return dash.no_update
    
    transformed_features = [
        'trip_distance_log', 'fare_amount_log', 'total_amount_log',
        'tip_amount_log', 'tolls_amount_log'
    ]
    
    # outlier summary
    outlier_results = get_analysis_results()['outlier_summary']
    
    # calculate outlier percentages
    final_data = get_data('final')
    cleaned_data = get_data('cleaned')
    
    initial_plot = create_box_plot(transformed_features[0], final_data, "After Outlier Removal - ")
    
    return [
        html.Div([
            html.H2("Distribution After Outlier Removal"),
            
            # summary table
            html.Div([
                html.H3("Outlier Removal Summary", style={'textAlign': 'center'}),
                html.Table([
                    html.Tr([
                        html.Th("Feature"), 
                        html.Th("Outliers Removed"),
                        html.Th("Percentage")
                    ]),
                    *[html.Tr([
                        html.Td(feature),
                        html.Td(f"{outlier_results[feature]:,}"),
                        html.Td(f"{(outlier_results[feature] / len(cleaned_data) * 100):.2f}%")
                    ]) for feature in transformed_features]
                ], style={
                    'width': '80%',
                    'margin': '20px auto',
                    'borderCollapse': 'collapse'
                })
            ]),
            
            dcc.Dropdown(
                id='transformed-feature-dropdown',
                options=[{'label': feature, 'value': feature} 
                        for feature in transformed_features],
                value=transformed_features[0],
                style={'marginBottom': '20px'}
            ),
            dcc.Graph(id='box-plot-transformed', figure=initial_plot)
        ]),
        "Reset Box Plot"
    ]

@callback(
    Output('box-plot-transformed', 'figure'),
    Input('transformed-feature-dropdown', 'value'),
    prevent_initial_call=True
)
def update_transformed_plot(feature):
    if not feature:
        return go.Figure(layout=dict(
            title="Please select a feature to display the box plot",
            xaxis_visible=False,
            yaxis_visible=False
        ))
    
    data = get_data('final')
    return create_box_plot(feature, data, "After Outlier Removal - ")