# components/pca.py
from dash import html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data_manager import get_data, get_analysis_results

def create_variance_plot(pca_summary):
    # explained variance ratios
    explained_variance = pca_summary['explained_variance_ratio']
    cumulative_variance = pca_summary['cumulative_variance_ratio']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # bar
    fig.add_trace(
        go.Bar(
            x=list(range(1, len(explained_variance) + 1)),
            y=explained_variance * 100,
            name="Individual",
            marker_color='rgb(71, 160, 169)'
        ),
        secondary_y=False
    )
    
    # line
    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(cumulative_variance) + 1)),
            y=cumulative_variance * 100,
            name="Cumulative",
            line=dict(color='rgb(255, 127, 14)', width=3)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title="PCA Explained Variance Ratio",
        xaxis_title="Principal Component",
        showlegend=True,
        height=500
    )
    
    # y-axis
    fig.update_yaxes(title_text="Individual Explained Variance (%)", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Explained Variance (%)", secondary_y=True)
    
    return fig

def create_component_loadings_plot(final_df):
    sampled_data = final_df.sample(n=min(10000, len(final_df)), random_state=42)
    
    # get first 2 principal components
    pc1 = sampled_data['PC1']
    pc2 = sampled_data['PC2']
    
    # scatter plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pc1,
            y=pc2,
            mode='markers',
            marker=dict(
                color='rgb(71, 160, 169)',
                size=5,
                opacity=0.5
            ),
            name='Data Points'
        )
    )
    
    fig.update_layout(
        title="First Two Principal Components",
        xaxis_title="First Principal Component",
        yaxis_title="Second Principal Component",
        height=600,
        showlegend=False
    )
    
    return fig

def layout_setting():
    # get PCA result and the final data
    analysis_results = get_analysis_results()
    pca_summary = analysis_results.get('pca_summary')
    final_df = get_data('final')
    
    if pca_summary is None or final_df is None:
        return html.Div("No PCA results available")
    
    # explained variance ratios
    explained_variance = pca_summary['explained_variance_ratio']
    cumulative_variance = pca_summary['cumulative_variance_ratio']
    
    return html.Div([
        html.H1("Principal Component Analysis", style={'textAlign': 'center'}),
        
        html.Div([
            html.Div([
                html.H2("Explained Variance Analysis"),
                dcc.Graph(figure=create_variance_plot(pca_summary)),

                html.Table([
                    html.Tr([
                        html.Th("Principal Component"),
                        html.Th("Individual Variance (%)"),
                        html.Th("Cumulative Variance (%)")
                    ]),
                    *[
                        html.Tr([
                            html.Td(f"PC{i+1}"),
                            html.Td(f"{var*100:.2f}%"),
                            html.Td(f"{cum*100:.2f}%")
                        ]) for i, (var, cum) in enumerate(zip(
                            explained_variance,
                            cumulative_variance
                        ))
                    ]
                ], style={
                    'width': '80%',
                    'margin': '20px auto',
                    'borderCollapse': 'collapse'
                })
            ]),
            
            html.Hr(),
            
            html.Div([
                html.H2("Principal Components Visualization"),
                html.P("""
                    This plot shows the projection of the data onto the first two principal components.
                    Each point represents a taxi trip, and the axes represent the two most important
                    patterns found in the data.
                """),
                dcc.Graph(figure=create_component_loadings_plot(final_df)),
            ]),
            
            html.Div([
                html.H2("PCA Interpretation"),
                html.P([
                    html.Strong("Key Findings:"),
                    html.Br(),
                    f"• The first principal component explains {explained_variance[0]*100:.2f}% of the total variance",
                    html.Br(),
                    f"• The first two components together explain {(explained_variance[0] + explained_variance[1])*100:.2f}% of the variance",
                    html.Br(),
                    f"• We need {np.sum(cumulative_variance < 0.95) + 1} components to explain 95% of the variance"
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