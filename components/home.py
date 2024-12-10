# components/home.py
from dash import html

layout = html.Div([
    html.H1('Introduction', style={'textAlign': 'center'}),
    html.Div([
        # dataset info
        html.P([
            html.Strong('Dataset: '),
            'New York City Taxi and Limousine Commission (TLC) Trip Record Data'
        ]),
        
        html.P([
            html.Strong('Range: '),
            'July 2024 Yelllow Taxi Trip Records'
        ]),

        html.Br(),
        
        html.P([
            html.Strong('Total Observation: '),
            '3,076,903'
        ]),
        html.P([
            html.Strong('Number of Numerical Features: '),
            '13'
        ]),
        html.P([
            html.Strong('Number of Categorical Features: '),
            '6'
        ]),

        html.Br(),
        
        # numerical features
        html.H3('Numerical Features', style={'textAlign': 'center'}),
        html.Table([
            html.Tr([
                html.Th('Feature', style={'width': '20%', 'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                html.Th('Description', style={'width': '80%', 'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'})
            ]),
            html.Tr([html.Td('tpep_pickup_datetime', style={'padding': '8px'}), 
                    html.Td('The date and time when the meter was engaged.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('tpep_dropoff_datetime', style={'padding': '8px'}), 
                    html.Td('The date and time when the meter was disengaged.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('passenger_count', style={'padding': '8px'}), 
                    html.Td('The number of passengers in the vehicle. (This is a driver-entered value.)', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('trip_distance', style={'padding': '8px'}), 
                    html.Td('The elapsed trip distance in miles reported by the taximeter.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('fare_amount', style={'padding': '8px'}), 
                    html.Td('The time-and-distance fare calculated by the meter.', style={'padding': '8px', 'textAlign': 'left', 'textAlign': 'left'})]),
            html.Tr([html.Td('extra', style={'padding': '8px'}), 
                    html.Td('Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('mta_tax', style={'padding': '8px'}), 
                    html.Td('$0.50 MTA tax that is automatically triggered based on the metered rate in use.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('tip_amount', style={'padding': '8px'}), 
                    html.Td('Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('tolls_amount', style={'padding': '8px'}), 
                    html.Td('Total amount of all tolls paid in trip.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('improvement_surcharge', style={'padding': '8px'}), 
                    html.Td('$0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('total_amount', style={'padding': '8px'}), 
                    html.Td('The total amount charged to passengers. Does not include cash tips.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('congestion_surcharge', style={'padding': '8px'}), 
                    html.Td('Total amount collected in trip for NYS congestion surcharge.', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('airport_fee', style={'padding': '8px'}), 
                    html.Td('$1.25 for pick up only at LaGuardia and John F. Kennedy Airports', style={'padding': '8px', 'textAlign': 'left'})])
        ], style={
            'width': '100%',
            'margin': '20px 0',
            'borderCollapse': 'collapse', 
        }),

        # categorical features
        html.H3('Categorical Features', style={'textAlign': 'center'}),
        html.Table([
            html.Tr([
                html.Th('Feature', style={'width': '20%', 'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                html.Th('Description & Values', style={'width': '80%', 'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'})
            ]),
            html.Tr([html.Td('VendorID', style={'padding': '8px'}), 
                    html.Td(['A code indicating the TPEP provider that provided the record:', html.Br(),
                            '• 1 = Creative Mobile Technologies, LLC', html.Br(),
                            '• 2 = VeriFone Inc.'], style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('RatecodeID', style={'padding': '8px'}), 
                    html.Td(['The final rate code in effect at the end of the trip:', html.Br(),
                            '• 1 = Standard rate', html.Br(),
                            '• 2 = JFK', html.Br(),
                            '• 3 = Newark', html.Br(),
                            '• 4 = Nassau or Westchester', html.Br(),
                            '• 5 = Negotiated fare', html.Br(),
                            '• 6 = Group ride'], style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('store_and_fwd_flag', style={'padding': '8px'}), 
                    html.Td(['This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka "store and forward," because the vehicle did not have a connection to the server:', html.Br(),
                            '• Y = store and forward trip', html.Br(),
                            '• N = not a store and forward trip'], style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('PULocationID', style={'padding': '8px'}), 
                    html.Td('TLC Taxi Zone in which the taximeter was engaged', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('DOLocationID', style={'padding': '8px'}), 
                    html.Td('TLC Taxi Zone in which the taximeter was disengaged', style={'padding': '8px', 'textAlign': 'left'})]),
            html.Tr([html.Td('payment_type', style={'padding': '8px'}), 
                    html.Td(['A numeric code signifying how the passenger paid for the trip:', html.Br(),
                            '• 1 = Credit card', html.Br(),
                            '• 2 = Cash', html.Br(),
                            '• 3 = No charge', html.Br(),
                            '• 4 = Dispute', html.Br(),
                            '• 5 = Unknown', html.Br(),
                            '• 6 = Voided trip'], style={'padding': '8px', 'textAlign': 'left'})])
        ], style={
            'width': '100%',
            'margin': '20px 0',
            'borderCollapse': 'collapse'
        }),

        html.Br(),

        html.P([
            html.Strong('Data Source: '),
            html.A(
                'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page',
                href='https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page',
                target='_blank'
            )
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