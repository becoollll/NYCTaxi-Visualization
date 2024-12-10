# components/normality_test.py
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import scipy.stats as stats
from data_manager import get_data
import dash

def perform_selected_tests(data, feature, selected_methods):
    sample_data = data[feature].sample(n=min(5000, len(data)), random_state=42)
    results = {}
    
    for method in selected_methods:
        if method == 'shapiro':
            stat, p = stats.shapiro(sample_data)
            results['Shapiro-Wilk'] = (stat, p)
        elif method == 'anderson':
            result = stats.anderson(sample_data, dist='norm')
            results['Anderson-Darling'] = (result.statistic, result.critical_values[2])
        elif method == 'dagostino':
            stat, p = stats.normaltest(sample_data)
            results["D'Agostino-Pearson"] = (stat, p)
        elif method == 'kstest':
            stat, p = stats.kstest(sample_data, 'norm')
            results['Kolmogorov-Smirnov'] = (stat, p)
    
    return results

def create_analysis_plots(data, feature, title_prefix=""):
    sampled_data = data.sample(n=min(10000, len(data)), random_state=42)
    feature_data = sampled_data[feature]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f"{title_prefix}Normal Q-Q Plot",
            f"{title_prefix}Distribution Plot"
        )
    )

    # qq plot
    sorted_data = np.sort(feature_data)
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(sorted_data)))
    
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=sorted_data,
            mode='markers',
            name='Q-Q Plot',
            marker=dict(
                color='rgb(71, 160, 169)',
                size=5,
                opacity=0.6
            )
        ),
        row=1, col=1
    )
    
    # reference line for qq plot
    line_x = np.linspace(min(theoretical_quantiles), max(theoretical_quantiles), 100)
    line_y = np.linspace(min(sorted_data), max(sorted_data), 100)
    
    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode='lines',
            name='Reference Line',
            line=dict(
                color='rgb(255, 127, 14)',
                width=2
            )
        ),
        row=1, col=1
    )
    
    # distribution plot
    fig.add_trace(
        go.Histogram(
            x=feature_data,
            name='Data Distribution',
            nbinsx=50,
            opacity=0.7,
            marker_color='rgb(71, 160, 169)'
        ),
        row=1, col=2
    )
    
    # normal curve to distribution plot
    x_range = np.linspace(min(feature_data), max(feature_data), 100)
    mean = np.mean(feature_data)
    std = np.std(feature_data)
    pdf = stats.norm.pdf(x_range, mean, std)
    
    hist, bin_edges = np.histogram(feature_data, bins=50)
    scaling_factor = max(hist) / max(pdf)
    pdf_scaled = pdf * scaling_factor
    
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=pdf_scaled,
            name='Normal Distribution',
            line=dict(
                color='rgb(255, 127, 14)',
                width=2
            )
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text=f"{title_prefix}Analysis for {feature}",
        title_x=0.5,
    )
    
    fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=1)
    fig.update_xaxes(title_text=feature, row=1, col=2)
    fig.update_yaxes(title_text="Sample Quantiles", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)
    
    return fig



def layout_setting():
    numerical_features = [
        'trip_distance', 'fare_amount', 'total_amount',
        'tip_amount', 'tolls_amount'
    ]
    
    # options
    test_methods = [
        {'label': 'Shapiro-Wilk', 'value': 'shapiro'},
        {'label': 'Anderson-Darling', 'value': 'anderson'},
        {'label': "D'Agostino-Pearson", 'value': 'dagostino'},
        {'label': 'Kolmogorov-Smirnov', 'value': 'kstest'}
    ]

    return html.Div([
        html.H1("Normality Test", style={'textAlign': 'center'}),
        
        # explanations
        html.Div([   
            html.Div([
                html.H3("Test Methods Explanation", style={'textAlign': 'center'}),
                html.Div([
                    html.H4("Shapiro-Wilk Test"),
                    dcc.Markdown("""
                        A statistical test that examines whether a sample comes from a normally distributed population.
                        
                        Formula: $W = \\frac{(\\sum a_i x_{(i)})^2}{\\sum(x_i - \\bar{x})^2}$
                        
                        Where: $a_i$ are weights, $x_{(i)}$ are ordered sample values, $\\bar{x}$ is the sample mean
                    """, mathjax=True),
                    
                    html.H4("Anderson-Darling Test"),
                    dcc.Markdown("""
                        Measures how well the data follows a normal distribution, giving more weight to the tails.
                        
                        Formula: $A^2 = -n - \\frac{1}{n}\\sum(2i-1)[\\ln F(Y_i) + \\ln(1-F(Y_{n-i+1}))]$
                        
                        Where: $F$ is the cumulative distribution function, $Y_i$ are ordered standardized sample values
                    """, mathjax=True),
                    
                    html.H4("D'Agostino-Pearson Test"),
                    dcc.Markdown("""
                        Combines skewness and kurtosis tests to determine if data is normally distributed.
                        
                        Formula: $K^2 = Z_1^2(\\text{skewness}) + Z_2^2(\\text{kurtosis})$
                        
                        Tests both the symmetry and tail weight of the distribution
                    """, mathjax=True),
                    
                    html.H4("Kolmogorov-Smirnov Test"),
                    dcc.Markdown("""
                        Compares the empirical distribution function with that of a normal distribution.
                        
                        Formula: $D = \\max|F_{(x)} - S_{(x)}|$
                        
                        Where: $F_{(x)}$ is the theoretical CDF, $S_{(x)}$ is the empirical CDF
                    """, mathjax=True)
                ], style={'marginBottom': '30px'}),
                
                html.P("Select Test Method"),
                dcc.Dropdown(
                    id='test-method-select',
                    options=test_methods,
                    value=['shapiro'],
                    multi=True,
                    style={'marginBottom': '20px'}
                ),
            ]),
            html.Div(id='test-results'),

            html.Hr(),

            html.Div([
                html.P("Select Feature"),
                dcc.Dropdown(
                    id='feature-select',
                    options=[{'label': f, 'value': f} for f in numerical_features],
                    value=numerical_features[0],
                    style={'marginBottom': '20px'}
                ),
            ]),

            # original plot
            html.Div([
                html.H3("Original Data Analysis", style={'textAlign': 'center'}),
                dcc.Graph(id='qq-plot-original'),
            ]),
            
            html.Hr(),
            
            # after log transformation
            html.Div([
                html.H3("Log-Transformed Data Analysis", style={'textAlign': 'center'}),
                dcc.Graph(id='qq-plot-transformed'),
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
    [Output('qq-plot-original', 'figure'),
     Output('qq-plot-transformed', 'figure'),
     Output('test-results', 'children')],
    [Input('feature-select', 'value'),
     Input('test-method-select', 'value')]
)

def update_plots(feature, selected_methods):
    if not feature or not selected_methods:
        return dash.no_update, dash.no_update, dash.no_update
    
    cleaned_data = get_data('cleaned')
    final_data = get_data('final')
    
    # plots
    orig_plots = create_analysis_plots(cleaned_data, feature, "Original Data - ")
    feature_log = f"{feature}_log"
    trans_plots = create_analysis_plots(final_data, feature_log, "Log-Transformed - ")
    
    # test results
    orig_results = perform_selected_tests(cleaned_data, feature, selected_methods)
    trans_results = perform_selected_tests(final_data, feature_log, selected_methods)
    
    test_results = html.Div([
        html.H3("Normality Test Results", style={'textAlign': 'center'}),
        html.Table([
            html.Thead(html.Tr([
                html.Th("", rowSpan=2),
                html.Th("Original Data", colSpan=2),
                html.Th("Log-Transformed", colSpan=2),
            ])),
            html.Thead(html.Tr([
                html.Th("Test Method"),
                html.Th("Statistic"),
                html.Th("p-value"),
                html.Th("Statistic"),
                html.Th("p-value"),
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(test_name),
                    html.Td(f"{orig_results[test_name][0]:.4f}"),
                    html.Td(f"{orig_results[test_name][1]:.4e}"),
                    html.Td(f"{trans_results[test_name][0]:.4f}"),
                    html.Td(f"{trans_results[test_name][1]:.4e}")
                ]) for test_name in orig_results.keys()
            ])
        ], style={
            'width': '90%',
            'margin': '20px auto',
            'borderCollapse': 'collapse',
            'border': '1px solid #ddd',
            'textAlign': 'center'
        })
    ])
    
    return orig_plots, trans_plots, test_results