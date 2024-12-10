# components/categorical_plots.py
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from data_manager import get_data
import json
import dash

color_palette1 = ['#47A0A9', '#94C81A', '#FFBF33', '#FF7636', '#2D4ECD', '#45D6FF']
color_palette2 = ['rgba(133, 191, 198, 0.3)', 'rgba(183, 218, 102, 0.3)', 'rgba(255, 212, 119, 0.3)', 'rgba(255, 164, 121, 0.3)']

def create_pickup_location_map(data):
    # load GeoJSON data
    try:
        with open('datasets/taxi_zones.geojson') as f:
            taxi_zones = json.load(f)
            
        # zone mapping dictionary
        zone_mapping = {
            str(feature['properties']['location_id']): feature['properties']['zone']
            for feature in taxi_zones['features']
        }
    except FileNotFoundError:
        return go.Figure().update_layout(
            title="GeoJSON file not found",
            annotations=[{"text": "Map data not available", "showarrow": False}]
        )
    
    # count pickups by location
    pickup_counts = data['PULocationID'].value_counts().reset_index()
    pickup_counts.columns = ['location_id', 'count']
    
    # convert location IDs to string and add zone names
    pickup_counts['location_id'] = pickup_counts['location_id'].astype(str)
    pickup_counts['zone'] = pickup_counts['location_id'].map(zone_mapping)
    
    # create the pickup map
    fig = px.choropleth_mapbox(
        pickup_counts,
        geojson=taxi_zones,
        locations='location_id',
        color='count',
        color_continuous_scale='Viridis',
        featureidkey='properties.location_id',
        mapbox_style='carto-positron',
        zoom=11,
        center={"lat": 40.76, "lon": -73.9857},
        opacity=0.7,
        labels={'count': 'Pickup Count'},
        title='Taxi Pickup Locations',
        hover_data={'location_id': True, 'zone': True, 'count': True}
    )
    
    # hover info
    fig.update_traces(
        hovertemplate="<br>".join([
            "Zone: %{customdata[1]}",
            "Location ID: %{customdata[0]}",
            "Count: %{customdata[2]:,.0f}"
        ])
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title_x=0.5
    )
    
    return fig

def create_dropoff_location_map(data):
    try:
        with open('datasets/taxi_zones.geojson') as f:
            taxi_zones = json.load(f)
            
        zone_mapping = {
            str(feature['properties']['location_id']): feature['properties']['zone']
            for feature in taxi_zones['features']
        }
    except FileNotFoundError:
        return go.Figure().update_layout(
            title="GeoJSON file not found",
            annotations=[{"text": "Map data not available", "showarrow": False}]
        )
    
    dropoff_counts = data['DOLocationID'].value_counts().reset_index()
    dropoff_counts.columns = ['location_id', 'count']
    
    dropoff_counts['location_id'] = dropoff_counts['location_id'].astype(str)
    dropoff_counts['zone'] = dropoff_counts['location_id'].map(zone_mapping)
    
    fig = px.choropleth_mapbox(
        dropoff_counts,
        geojson=taxi_zones,
        locations='location_id',
        color='count',
        color_continuous_scale='Viridis',
        featureidkey='properties.location_id',
        mapbox_style='carto-positron',
        zoom=11,
        center={"lat": 40.76, "lon": -73.9857},
        opacity=0.7,
        labels={'count': 'Dropoff Count'},
        title='Taxi Dropoff Locations',
        hover_data={'location_id': True, 'zone': True, 'count': True}
    )
    
    fig.update_traces(
        hovertemplate="<br>".join([
            "Zone: %{customdata[1]}",
            "Location ID: %{customdata[0]}",
            "Count: %{customdata[2]:,.0f}"
        ])
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title_x=0.5
    )
    
    return fig

def create_location_statistics(data):
    try:
        with open('datasets/taxi_zones.geojson') as f:
            taxi_zones = json.load(f)
            
        zone_mapping = {
            str(feature['properties']['location_id']): feature['properties']['zone']
            for feature in taxi_zones['features']
        }
    except FileNotFoundError:
        zone_mapping = {}
    
    # calculate top5 locations for pickup/dropoff counts
    top_pickup = data['PULocationID'].value_counts().nlargest(5)
    top_dropoff = data['DOLocationID'].value_counts().nlargest(5)
    
    return html.Div([
        html.Div([
            html.H3("Top 5 Pickup Locations"),
            html.Table([
                html.Tr([html.Th("ID"), html.Th("Zone")]),
                *[html.Tr([
                    html.Td(f"{loc}"),
                    html.Td(zone_mapping.get(str(loc), "Unknown"))
                ]) for loc, count in top_pickup.items()]
            ], style={'width': '100%', 'margin': '10px 0'})
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.H3("Top 5 Dropoff Locations"),
            html.Table([
                html.Tr([html.Th("ID"), html.Th("Zone")]),
                *[html.Tr([
                    html.Td(f"{loc}"),
                    html.Td(zone_mapping.get(str(loc), "Unknown"))
                ]) for loc, count in top_dropoff.items()]
            ], style={'width': '100%', 'margin': '10px 0'})
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ])


def create_payment_analysis(data):
    payment_map = {
        1: 'Credit Card',
        2: 'Cash',
        3: 'No Charge',
        4: 'Dispute',
        5: 'Unknown',
        6: 'Voided Trip'
    }
    
    # convert payment types
    data['payment_method'] = data['payment_type'].map(payment_map)
    
    # counts
    payment_counts = data['payment_method'].value_counts()
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "bar"}]],
        subplot_titles=('Payment Methods Distribution', 'Payment Methods Count'),
        horizontal_spacing=0.15
    )
    
    # pie chart
    fig.add_trace(
        go.Pie(
            labels=payment_counts.index,
            values=payment_counts.values,
            name="Payment Methods",
            hole=0.3,
            textinfo='percent+label',
            legendgroup="pie",
            legendgrouptitle_text="Proportion",
            marker_colors=color_palette1,
            hovertemplate="Method: %{label}<br>Count: %{value:,.0f}<br>Percentage: %{percent}"
        ),
        row=1, col=1
    )

    # bar chart
    fig.add_trace(
        go.Bar(
            x=payment_counts.index,
            y=payment_counts.values,
            name="Payment Methods",
            marker_color=color_palette1,
            text=payment_counts.values,
            textposition='auto',
            legendgroup="bar",
            legendgrouptitle_text="Frequency",
            hovertemplate="Method: %{x}<br>Count: %{y:,.0f}"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        title_text="Payment Methods Analysis"
    )
    
    return fig

def create_rate_code_analysis(data):
    rate_map = {
        1: 'Standard rate',
        2: 'JFK',
        3: 'Newark',
        4: 'Nassau or Westchester',
        5: 'Negotiated fare',
        6: 'Group ride'
    }
    
    # convert rate codes
    data['rate_type'] = data['RatecodeID'].map(rate_map)
    
    # calculate average fare by rate code
    fare_by_rate = data.groupby('rate_type').agg({
        'total_amount': 'mean',
        'trip_distance': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Average Fare by Rate Type', 'Average Distance by Rate Type'),
        horizontal_spacing=0.15
    )
    
    # avg fare bar
    fig.add_trace(
        go.Bar(
            x=fare_by_rate['rate_type'],
            y=fare_by_rate['total_amount'],
            name="Avg Fare",
            marker_color=color_palette1,
            hovertemplate="Rate Type: %{x}<br>Avg Fare: $%{y:.2f}"
        ),
        row=1, col=1
    )
    
    # avg distance bar
    fig.add_trace(
        go.Bar(
            x=fare_by_rate['rate_type'],
            y=fare_by_rate['trip_distance'],
            name="Avg Distance",
            marker_color=color_palette1,
            hovertemplate="Rate Type: %{x}<br>Avg Distance: %{y:.2f} miles"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        title_text="Rate Code Analysis"
    )
    
    fig.update_xaxes(tickangle=45) # rotate x labels
    
    return fig

def create_vendor_analysis(data):
    data['hour'] = pd.to_datetime(data['tpep_pickup_datetime']).dt.hour
    
    # calculate hourly vendor distribution
    vendor_hourly = data.pivot_table(
        index='hour',
        columns='VendorID',
        values='trip_distance',
        aggfunc='count',
        fill_value=0
    ).reset_index()
    
    fig = go.Figure()
    
    # add traces for each vendor
    for vendor in vendor_hourly.columns[1:]:
        fig.add_trace(
            go.Scatter(
                x=vendor_hourly['hour'],
                y=vendor_hourly[vendor],
                name=f'Vendor {vendor}',
                mode='lines+markers',
                hovertemplate="Hour: %{x}<br>Trips: %{y:,.0f}"
            )
        )
    
    fig.update_layout(
        title="Hourly Distribution by Vendor (Full Dataset)",
        xaxis_title="Hour of Day",
        yaxis_title="Number of Trips",
        height=500,
        showlegend=True
    )
    
    # show all hours for x labels
    fig.update_xaxes(
        ticktext=list(range(24)),
        tickvals=list(range(24)),
        tickmode="array"
    )
    
    return fig

def layout_setting():
    # options
    analysis_types = [
        {'label': 'Geographical Analysis', 'value': 'geo'},
        {'label': 'Payment Methods', 'value': 'payment'},
        {'label': 'Rate Codes', 'value': 'rate'},
        {'label': 'Vendor Distribution', 'value': 'vendor'}
    ]
    
    return html.Div([
        html.H1("Categorical Features Analysis", style={'textAlign': 'center'}),
        
        html.Div([
            html.Div([
                html.P("Select Analysis Type"),
                dcc.Dropdown(
                    id='category-analysis-type',
                    options=analysis_types,
                    value='geo',
                    style={'marginBottom': '20px'}
                ),
            ]),
            
            # content Div
            html.Div(id='category-analysis-content')
            
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

@callback(
    Output('category-analysis-content', 'children'),
    Input('category-analysis-type', 'value')
)

# content layout
def update_category_analysis(analysis_type):
    if not analysis_type:
        return dash.no_update
    
    data = get_data('final')
    
    explanations = {
        'geo': """The geographical analysis shows the distribution of taxi pickups and dropoffs across NYC zones. 
                 The heatmap intensity indicates the frequency of trips in each area, helping identify high-traffic locations.""",
        'payment': """This analysis reveals the preferred payment methods among taxi users. The pie chart shows the proportion 
                     of each payment type, while the bar chart compares absolute counts.""",
        'rate': """The rate code analysis compares different fare types, showing average fares and trip distances for each category. 
                  This helps understand how special rate zones like JFK and Newark affect trip metrics.""",
        'vendor': """The vendor distribution analysis shows how trip volumes vary between different taxi vendors throughout the day,
                    revealing patterns in service coverage and market share.""",
        'flag': """The store and forward flag analysis examines trips with GPS data store-and-forward enabled vs disabled,
                  comparing average distances, fares, and total trip counts between these categories."""
    }
    
    if analysis_type == 'geo':
        return html.Div([
            html.P(explanations['geo'], className='analysis-explanation'),
            html.H3("Pickup Locations", style={'textAlign': 'center'}),
            dcc.Graph(figure=create_pickup_location_map(data)),
            html.H3("Dropoff Locations", style={'textAlign': 'center'}),
            dcc.Graph(figure=create_dropoff_location_map(data)),
            html.Hr(),
            html.H3("Location Statistics", style={'textAlign': 'center'}),
            create_location_statistics(data)
        ])
    
    elif analysis_type == 'payment':
        return html.Div([
            html.P([
                "How the passenger paid for the trip:",
                html.Br(),
                "• 1 = Credit card",
                html.Br(),
                "• 2 = Cash",
                html.Br(),
                "• 3 = No charge",
                html.Br(),
                "• 4 = Dispute",
                html.Br(),
                "• 5 = Unknown",
                html.Br(),
                "• 6 = Voided trip"
            ], style={'marginBottom': '20px'}),
            html.P(explanations['payment'], className='analysis-explanation'),
            dcc.Graph(figure=create_payment_analysis(data))
        ])
    
    elif analysis_type == 'rate':
        return html.Div([
            html.P([
                "The final rate code in effect at the end of the trip:",
                html.Br(),
                "• 1 = Standard rate",
                html.Br(),
                "• 2 = JFK",
                html.Br(),
                "• 3 = Newark",
                html.Br(),
                "• 4 = Nassau or Westchester",
                html.Br(),
                "• 5 = Negotiated fare",
                html.Br(),
                "• 6 = Group ride"
            ], style={'marginBottom': '20px'}),
            html.P(explanations['rate'], className='analysis-explanation'),
            dcc.Graph(figure=create_rate_code_analysis(data))
        ])
    
    else:
        return html.Div([
            html.P([
                "The VendorID indicating the TPEP provider:",
                html.Br(),
                "• 1 = Creative Mobile Technologies, LLC",
                html.Br(),
                "• 2 = VeriFone Inc."
            ], style={'marginBottom': '20px'}),
            html.P(explanations['vendor'], className='analysis-explanation'),
            dcc.Graph(figure=create_vendor_analysis(data))
        ])
    

layout = layout_setting()