import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.enrich import ServersideOutput, Output, State, Input, callback, html, dcc

import plotly.graph_objects as go

import pandas as pd
import json
import utils

dash.register_page(__name__, path="/", top_nav=True)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                id='geomap'
            ),
            dcc.Store(
                id='store_gb',
            ),
            dcc.Store(
                id='store_id'
            ),
            dcc.Store(
                id='serverside_store',
            ),
            html.Div(
                id='dummy',
                style={'display': None}
            )
        ],
            width=5
        ),
        dbc.Col([
            dbc.Row(
                id='g1'
            ),
            dbc.Row(
                id='g2',
                children=[
                    dbc.Container([
                        dbc.Row([
                            html.Div(
                                dcc.Dropdown(
                                    id='drop_neighbors',
                                    options=[
                                        {'label': i, 'value': i + 1} for i in range(1, 6)
                                    ],
                                    placeholder='Compare total sale with "n" closest stores',
                                    multi=False,
                                ), style={'width': '50%'}
                            ),
                            html.Div(
                                dbc.RadioItems(
                                    id='radio_quarter',
                                    className="btn-group",
                                    options=[
                                        {'label': 'Quarter 1', 'value': '2021Q1'},
                                        {'label': 'Quarter 3', 'value': '2021Q2'},
                                        {'label': 'Quarter 3', 'value': '2021Q3'},
                                        {'label': 'Quarter 4', 'value': '2021Q4'},
                                    ],
                                    value='2021Q1',
                                    label_style={'margin-right': '12px'}
                                ), style={'width': '50%'}
                            )
                        ], className='d-flex align-items-center'),
                        dbc.Row(
                            dcc.Graph(
                                id='graph_2',
                            )
                        )
                    ])
                ],
                style={'visibility': 'hidden'}
            ),
        ], width=7
        )
    ])
], fluid=True)


# this callback gets triggered only at app start by a dummy component which is always hidden
# I did this, because I could not figure out, how to initiate the serverside store with initial
# values, i.e. data!=None
@callback(
    [
        ServersideOutput('serverside_store', 'data'),
        Output('geomap', 'children'),
        Output('store_gb', 'data'),
    ],
    Input('dummy', 'children'),
    prevent_initial_call=False
)
def prepare_date(_):
    # prepare data
    gb_store_number, kdt, markers = utils.prepare_data()

    # this is actually a pandas.DataFrame.groupby(store_number) stored in a json format
    gb = json.loads(gb_store_number)

    # create html.Div for the map
    g_map = html.Div(
        [
            dl.Map(
                id='basemap',
                children=[
                    dl.TileLayer(
                        url=utils.url,
                        attribution=utils.attribution
                    ),
                    dl.GeoJSON(
                        id='liquor_stores',
                        data=utils.dicts_to_geojson(
                            [{**marker, **dict(tooltip=marker['id'])} for marker in markers]
                        ),
                        cluster=True,
                        zoomToBoundsOnClick=True,
                        superClusterOptions={"radius": 80}
                    )
                ],
                style={'width': '100%', 'height': '800px'},
                # center the view on the first store location
                center=[markers[0].get('lat'), markers[0].get('lon')],
                zoom=5,
            )
        ]
    )
    return kdt, g_map, gb


# callback triggers the click feature on the map, if a marker is clicked, return its ID
@callback(
    Output('store_id', 'data'),
    Input('liquor_stores', 'click_feature'),
)
def liquor_store_id(feature):
    if not feature:
        raise PreventUpdate
    # this is necessary if a click_feature is fired but no marker has been clicked
    if not feature.get('properties').get('id'):
        raise PreventUpdate
    return feature['properties']['id']


# callback is triggerd by updating the data in the dcc.Store(id='store_id')
# which basically means, a different store number has been clicked
# updates the dcc.Graph(id='g1')
@callback(
    Output('g1', 'children'),
    Input('store_id', 'data'),
    State('store_gb', 'data'),
    prevent_initial_call=True
)
def get_stats(store_id, store_gb):
    # convert the json into a DataFrame
    df_store_id = pd.read_json(store_gb[store_id])

    # create figure and update layout
    fig = go.Figure()
    fig.add_bar(x=df_store_id.date, y=df_store_id.sale_dollars)
    fig.update_layout(utils.figure_layout)

    return dbc.Container(
        [
            dbc.Row(
                html.Div(
                    dcc.Dropdown(
                        id='drop',
                        options=[
                            'bottles_sold',
                            'sale_dollars',
                            'volume_sold_liters'
                        ],
                        value='sale_dollars',
                        multi=True,

                    ), style={'width': '50%'}
                )
            ),
            dbc.Row(
                dcc.Graph(
                    id='graph_1',
                    figure=fig
                )
            )
        ]
    )


# this callback updates the figure of graph_1 depending on the selections of the
# dropdown component right above
@callback(
    Output('graph_1', 'figure'),
    Input('drop', 'value'),
    [
        State('store_id', 'data'),
        State('store_gb', 'data')
    ],
    prevent_initial_call=True
)
def update_figure(drop_selection, store_id, store_gb):
    # convert the json into a DataFrame
    df_store_id = pd.read_json(store_gb[store_id])

    # create figure and update layout
    fig = go.Figure()
    for selection in drop_selection:
        fig.add_bar(x=df_store_id.date, y=df_store_id[selection], name=selection)

    fig.update_layout(utils.figure_layout)
    return fig


# this callback shows the hidden dropdown (only at first selection of store)
# and updates the figure depending on the number of neighbors chosen in the
# dropdown right above the figure. Also takes into account the quarter chosen
# by the radio item
@callback(
    [
        Output('g2', 'style'),
        Output('graph_2', 'figure')
    ],
    [
        Input('store_id', 'data'),
        Input('drop_neighbors', 'value'),
        Input('radio_quarter', 'value'),
    ],
    State('serverside_store', 'data'),
    State('store_gb', 'data'),
    prevent_initial_call=True
)
def compare_with_neighbors(
        store_id,
        no_of_neighbors,
        quarter,
        serverside_store,
        store_gb
):
    # retrieve information from server side store
    kdt, store_objects, store_coord_dict = serverside_store

    # get the location of the current store number
    current_stor_loc = store_coord_dict.get(int(store_id))

    # set default for number of neighbors
    if not no_of_neighbors:
        no_of_neighbors = 1

    # query in KDTree for the current store location
    dist, idx = kdt.query([current_stor_loc], no_of_neighbors)

    # get the list of neighboring stores
    neighbors = [store_objects[int(i)].num for i in idx[0]]

    # create base figure
    fig = go.Figure()

    # get DataFrames, create traces
    for neighbor in neighbors:
        df = pd.read_json(store_gb[str(neighbor)])
        df = df[df.quarter == quarter]
        fig.add_bar(x=df.date, y=df.sale_dollars, name=f'id:{neighbor}')

    # group the bar charts and change the layout
    fig.update_layout(utils.figure_layout)

    # add yaxis title
    fig.update_layout({'yaxis': {'title': 'Total sale in USD'}})
    return {}, fig
