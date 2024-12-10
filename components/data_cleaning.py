# components/data_cleaning.py
from dash import html, callback
from dash.dependencies import Input, Output
from data_manager import get_data, get_analysis_results
import pandas as pd

# nan or zero
def get_missing_values_summary():
    original_data = get_data('original')
    missing_values = original_data.isnull().sum()
    
    missing_summary = pd.DataFrame({
        'Feature': missing_values.index,
        'Missing Count': missing_values.values,
    })
    missing_summary = missing_summary[missing_summary['Missing Count'] > 0]
    
    return missing_summary

def layout_setting():
    # get data
    original_data = get_data('original')
    missing_summary = get_missing_values_summary()
    
    return html.Div([
        html.H1("Data Cleaning", style={'textAlign': 'center'}),
        html.Div([
            # original data
            html.Div([
                html.H2("Before Data Cleaning"),
                html.H3(
                    f"Total number of records: {len(original_data):,}", 
                    style={'textAlign': 'center'}
                ),
                
                # missing values
                html.Table(
                    [html.Tr([
                        html.Th("Feature"), 
                        html.Th("Missing Count"),
                    ])] +
                    [html.Tr([
                        html.Td(row['Feature']),
                        html.Td(f"{row['Missing Count']:,}")
                    ]) for index, row in missing_summary.iterrows()],
                    style={
                        'width': '50%',
                        'marginBottom': '20px',
                        'borderCollapse': 'collapse'
                    }
                ) if not missing_summary.empty else html.P("No missing values found in the dataset.")
            ]),
            
            # data cleaning
            html.Br(),
            html.P('Click the button to view cleaning results.', style={'textAlign': 'center'}),
            html.Div([

                # button
                html.Div([
                    html.Button(
                        'Clean Data',
                        id='view-results-button',
                        n_clicks=0
                    ),
                ]),

                # results
                html.Div(id='cleaning-results'),

                # invalid rules
                html.Hr(),
                html.Div([
                    html.H3("* Data Cleaning Rules:", style={'textAlign': 'center'}),
                    html.Table(
                        [html.Tr([
                            html.Th("Feature"), 
                            html.Th("Rule"),
                        ])] +
                        [
                            html.Tr([
                                html.Td("VendorID"),
                                html.Td("must be either 1 or 2")
                            ]),
                            html.Tr([
                                html.Td("passenger_count"),
                                html.Td("must be greater than 0")
                            ]),
                            html.Tr([
                                html.Td("trip_distance"),
                                html.Td("must be greater than or equal to 0.1")
                            ]),
                            html.Tr([
                                html.Td("PULocationID and DOLocationID"),
                                html.Td("must not be missing")
                            ]),
                            html.Tr([
                                html.Td("RatecodeID"),
                                html.Td("must be between 1 and 6")
                            ]),
                            html.Tr([
                                html.Td("store_and_fwd_flag"),
                                html.Td("must be either 'Y' or 'N'")
                            ]),
                            html.Tr([
                                html.Td("payment_type"),
                                html.Td("must be between 1 and 6")
                            ]),
                            html.Tr([
                                html.Td("fare_amount"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("extra"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("mta_tax"),
                                html.Td("must be exactly 0.5")
                            ]),
                            html.Tr([
                                html.Td("improvement_surcharge"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("tip_amount"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("tolls_amount"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("total_amount"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("congestion_surcharge"),
                                html.Td("must be non-negative")
                            ]),
                            html.Tr([
                                html.Td("Airport_fee"),
                                html.Td("must be non-negative")
                            ])
                        ],
                        style={
                            'width': '70%',
                            'marginBottom': '20px',
                            'borderCollapse': 'collapse'
                        }
                    )
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
    Output('cleaning-results', 'children'),
    [Input('view-results-button', 'n_clicks')],
    prevent_initial_call=True
)

def update_cleaning_results(n_clicks):
    if n_clicks:
        results = get_analysis_results()['cleaning_summary']
        
        return html.Div([
            html.Table([
                html.Tr([html.Th("Stage"), html.Th("Records")]),
                html.Tr([
                    html.Td("Original records"),
                    html.Td(f"{results['original_records']:,}")
                ]),
                html.Tr([
                    html.Td("After cleaning"),
                    html.Td(f"{results['cleaned_records']:,}")
                ]),
                html.Tr([
                    html.Td("Total removed records"),
                    html.Td(f"{results['removed_records']:,}")
                ])
            ], style={
                'width': '80%',
                'marginTop': '5%',
                'borderCollapse': 'collapse'
            }),
        ])
    
    return "Click the button to view cleaning results."