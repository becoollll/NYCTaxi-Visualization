# components/statistics.py
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from data_manager import get_data

def create_correlation_heatmap(data, features):
    # remove constant columns before calculating correlation
    non_constant_features = [col for col in features if data[col].std() != 0]
    
    # correlation matrix
    corr_matrix = data[non_constant_features].corr()
    
    # heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=non_constant_features,
        y=non_constant_features,
        text=np.round(corr_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title='Correlation Heatmap of Numerical Features',
        height=600,
        width=800,
        title_font=dict(family='serif', color='blue', size=24),
        title_x=0.5,
        title_font_weight='bold'
    )

    fig.update_xaxes(tickfont=dict(family='serif', color='darkred', size=18))
    fig.update_yaxes(tickfont=dict(family='serif', color='darkred', size=18))
    
    return fig

def layout_setting():
    data = get_data('final')
    
    numerical_features = [
        'trip_distance', 'fare_amount', 'total_amount',
        'tip_amount', 'tolls_amount', 'extra', 'mta_tax',
        'improvement_surcharge', 'congestion_surcharge', 'Airport_fee'
    ]
    
    stats_df = data[numerical_features].describe()
    
    return html.Div([
        html.H1("Statistical Analysis", style={'textAlign': 'center'}),
        
        html.Div([
            # correlation heatmap
            html.Div([
                html.H3("Feature Correlations", style={'textAlign': 'center'}),
                html.Div([
                    dcc.Graph(
                        figure=create_correlation_heatmap(data, numerical_features),
                    )
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'width': '100%'
                }),
            ]),
            
            html.Hr(),
            
            # summary statistics
            html.Div([
                html.H2("Summary Statistics"),
                html.Div([
                    html.H3("Basic Statistics", style={'textAlign': 'center'}),
                    html.Table([
                        html.Tr([html.Th("Feature"), html.Th("Count"), 
                                html.Th("Mean"), html.Th("Std")]),
                        *[
                            html.Tr([
                                html.Td(feature),
                                html.Td(f"{stats_df.loc['count', feature]:,.0f}"),
                                html.Td(f"{stats_df.loc['mean', feature]:.2f}"),
                                html.Td(f"{stats_df.loc['std', feature]:.2f}")
                            ]) for feature in numerical_features
                        ]
                    ], style={
                        'width': '100%',
                        'margin': '20px 0',
                        'borderCollapse': 'collapse'
                    })
                ]),
                html.Br(),
                
                # percentile statistics
                html.Div([
                    html.H3("Percentile Statistics", style={'textAlign': 'center'}),
                    html.Table([
                        html.Tr([html.Th("Feature"), html.Th("Min"), 
                                html.Th("25%"), html.Th("50%"), 
                                html.Th("75%"), html.Th("Max")]),
                        *[
                            html.Tr([
                                html.Td(feature),
                                html.Td(f"{stats_df.loc['min', feature]:.2f}"),
                                html.Td(f"{stats_df.loc['25%', feature]:.2f}"),
                                html.Td(f"{stats_df.loc['50%', feature]:.2f}"),
                                html.Td(f"{stats_df.loc['75%', feature]:.2f}"),
                                html.Td(f"{stats_df.loc['max', feature]:.2f}")
                            ]) for feature in numerical_features
                        ]
                    ], style={
                        'width': '100%',
                        'margin': '20px 0',
                        'borderCollapse': 'collapse'
                    })
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