# components/data_transform.py
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import scipy.stats as stats
from data_manager import get_data, get_analysis_results
import dash

color_palette1 = ['#47A0A9', '#94C81A', '#FFBF33', '#FF7636', '#2D4ECD', '#45D6FF']

def create_transformation_plots(data, feature):
    sampled_data = data.sample(n=min(10000, len(data)), random_state=42)
    original_data = sampled_data[feature]
    
    # calculate transformations
    log_transform = np.log1p(original_data)
    sqrt_transform = np.sqrt(original_data)
    boxcox_transform = stats.boxcox(original_data + 1)[0]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Original Distribution',
            'Log Transform',
            'Square Root Transform',
            'Box-Cox Transform'
        ]
    )
    
    # original
    fig.add_trace(
        go.Histogram(
            x=original_data,
            name='Original',
            marker_color=color_palette1[0],
            showlegend=False
        ),
        row=1, col=1
    )
    
    # log transform
    fig.add_trace(
        go.Histogram(
            x=log_transform,
            name='Log',
            marker_color=color_palette1[1],
            showlegend=False
        ),
        row=1, col=2
    )
    
    # square root transform
    fig.add_trace(
        go.Histogram(
            x=sqrt_transform,
            name='Square Root',
            marker_color=color_palette1[2],
            showlegend=False
        ),
        row=2, col=1
    )
    
    # box-cox transform
    fig.add_trace(
        go.Histogram(
            x=boxcox_transform,
            name='Box-Cox',
            marker_color=color_palette1[3],
            showlegend=False
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        title_text=f"Distribution Comparison for {feature} After Different Transformations",
        showlegend=False
    )
    
    return fig

def create_transformation_summary(data, feature):
    sampled_data = data.sample(n=min(5000, len(data)), random_state=42)
    original_data = sampled_data[feature]

    transforms = {
        'Original': original_data,
        'Log': np.log1p(original_data),
        'Square Root': np.sqrt(original_data),
        'Box-Cox': stats.boxcox(original_data + 1)[0]
    }
    
    # calculation
    summary_stats = {}
    for name, transformed_data in transforms.items():
        stat, p_value = stats.shapiro(transformed_data)
        skew = stats.skew(transformed_data)
        kurtosis = stats.kurtosis(transformed_data)
        
        summary_stats[name] = {
            'Shapiro-Wilk p-value': p_value,
            'Skewness': skew,
            'Kurtosis': kurtosis
        }
    
    return summary_stats

def layout_setting():
    numerical_features = [
        'trip_distance', 'fare_amount', 'total_amount',
        'tip_amount', 'tolls_amount'
    ]
    
    return html.Div([
        html.H1("Data Transformation", style={'textAlign': 'center'}),
        
        html.Div([
            # explanations
            html.Div([
                html.H3("Transformation Methods", style={'textAlign': 'center'}),
                html.Div([
                    html.H4("Logarithmic Transformation"),
                    dcc.Markdown(r"""
                        Applied when data is right-skewed and contains positive values.
                        
                        Formula: $y = \ln(x + 1)$
                        
                        The "+1" is used to handle zero values (log1p). This transformation is effective for:
                        - Right-skewed distributions
                        - Data spanning multiple orders of magnitude
                        - Multiplicative relationships
                    """, mathjax=True),
                    
                    html.H4("Square Root Transformation"),
                    dcc.Markdown(r"""
                        A milder alternative to log transformation for right-skewed data.
                        
                        Formula: $y = \sqrt{x}$
                        
                        This transformation is suitable for:
                        - Moderately right-skewed data
                        - Count data
                        - Data where variance increases with the mean
                    """, mathjax=True),
                    
                    html.H4("Box-Cox Transformation"),
                    dcc.Markdown(r"""
                        A family of power transformations that includes both log and square root.
                        
                        Formula: $y_{\lambda} = \begin{cases} 
                        \frac{x^{\lambda} - 1}{\lambda} & \text{if } \lambda \neq 0 \\
                        \ln(x) & \text{if } \lambda = 0
                        \end{cases}$
                        
                        Features:
                        - Automatically finds optimal transformation parameter λ
                        - λ = 0 gives log transform
                        - λ = 0.5 gives square root transform
                        - λ = 1 means no transformation needed
                    """, mathjax=True)
                ], style={'marginBottom': '30px'}),
            ]),
            
            # select feature
            html.Div([
                html.P("Select Feature"),
                dcc.Dropdown(
                    id='transform-feature-select',
                    options=[{'label': f, 'value': f} for f in numerical_features],
                    value=numerical_features[0],
                    style={'marginBottom': '20px'}
                ),
            ]),

            # plots
            html.Div([
                html.H3("Transformation Comparison", style={'textAlign': 'center'}),
                dcc.Graph(id='transformation-plots'),
            ]),
            
            html.Hr(),
            
            # summary
            html.Div(id='transformation-summary'),

            html.Br(),
            
            # interpretation
            html.Div([
                html.H2("Interpretation Guidelines"),
                html.P([
                    "• A normal distribution is symmetric and bell-shaped",
                    html.Br(),
                    "• Shapiro-Wilk test p-value > 0.05 suggests normality",
                    html.Br(),
                    "• Skewness close to 0 indicates symmetry",
                    html.Br(),
                    "• Kurtosis close to 0 indicates normal tail weight"
                ])
            ])
            
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
    [Output('transformation-plots', 'figure'),
     Output('transformation-summary', 'children')],
    [Input('transform-feature-select', 'value')]
)

def update_transformations(feature):
    if not feature:
        return dash.no_update
    
    data = get_data('cleaned')
    
    # create plots
    plots = create_transformation_plots(data, feature)
    
    # calculate statistics
    stats_summary = create_transformation_summary(data, feature)
    
    # summary table without transformation effect
    summary_table = html.Div([
        html.H2("Transformation Statistics"),
        html.Table([
            # Header
            html.Tr([
                html.Th("Transformation"),
                html.Th("Shapiro-Wilk p-value"),
                html.Th("Skewness"),
                html.Th("Kurtosis")
            ]),
            # Data rows
            *[html.Tr([
                html.Td(transform),
                html.Td(f"{stats['Shapiro-Wilk p-value']:.4e}"),
                html.Td(f"{stats['Skewness']:.4f}"),
                html.Td(f"{stats['Kurtosis']:.4f}")
            ]) for transform, stats in stats_summary.items()]
        ], style={
            'width': '100%',
            'margin': '20px 0',
            'borderCollapse': 'collapse'
        })
    ])
    
    return plots, summary_table