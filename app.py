# app.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from components import (
    home, data_cleaning, outlier, pca, normality_test,
    data_transform, numerical_plots, categorical_plots, statistics
)

# initialization
app = dash.Dash(
    __name__,
    external_stylesheets=['assets/style.css'],
    suppress_callback_exceptions=True
)

#server = app.server

app.layout = html.Div([
    html.Div([
        html.Img(
            src='/assets/images/logo.png',
            className='header-logo',
            id='header-logo'
        ),
        dcc.Tabs(
            id='all-tabs',
            value='tab1',
            children=[
                dcc.Tab(
                    label='HOME',
                    value='tab1',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='DATA CLEANING',
                    value='tab2',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='OUTLIER',
                    value='tab3',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='PCA',
                    value='tab4',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='NORMALITY TEST',
                    value='tab5',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='DATA TRANSFORM',
                    value='tab6',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='NUMERICAL FEATURES',
                    value='tab7',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='CATEGORICAL FEATURES',
                    value='tab8',
                    className='tab',
                    selected_className='tab-selected'
                ),
                dcc.Tab(
                    label='STATISTICS',
                    value='tab9',
                    className='tab',
                    selected_className='tab-selected'
                ),
            ],
        )
    ], className='header-container'),
    html.Div(id='tabs-content', children=home.layout),
    html.Div(id='processed-store', style={'display': 'none'})
])

@app.callback(
    Output('all-tabs', 'value'),
    Input('header-logo', 'n_clicks')
)

def navigate_to_home(n_clicks):
    if n_clicks is not None:
        return 'tab1'
    return dash.no_update

@app.callback(
    Output('tabs-content', 'children'),
    Input('all-tabs', 'value')
)

def render_content(tab):
    if tab == 'tab1':
        return home.layout
    elif tab == 'tab2':
        return data_cleaning.layout
    elif tab == 'tab3':
        return outlier.layout
    elif tab == 'tab4':
        return pca.layout
    elif tab == 'tab5':
        return normality_test.layout
    elif tab == 'tab6':
        return data_transform.layout
    elif tab == 'tab7':
        return numerical_plots.layout
    elif tab == 'tab8':
        return categorical_plots.layout
    elif tab == 'tab9':
        return statistics.layout

if __name__ == '__main__':
    app.run_server(debug=True)