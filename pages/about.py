import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, top_nav=True)

h1 = dbc.Card(
    [
        dbc.CardImg(src='https://dash-leaflet.herokuapp.com/assets/leaflet.png', top=True),
        dbc.CardBody(
            [
                html.H4('DASH Leaflet', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'I always wanted to play around with it',
                    className='card-text',
                ),
                html.A(
                    'link',
                    href='https://dash-leaflet.herokuapp.com/',
                    style={'color': '#375a7f'}
                ),
            ]
        ),
    ],
)

h2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Use of dcc.Store', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'I tried not to use global variables but use dcc.Store instead. '
                    'The JSON serialization of the pandas groupBy object is something '
                    'I never tried before. Not sure if this is actually the best / fastest '
                    'way to deal with this kind of data though',
                    className='card-text',
                ),
            ]
        ),
    ],
)

h3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Use of KDTree', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'Surely there are other options of dealing with this, but I wanted to '
                    'use a KDTree for nearest neighbors search',
                    className='card-text',
                ),
            ]
        ),
    ],
)

h4 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Time', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'Finishing a first version of this app before the deadline',
                    className='card-text',
                ),
            ]
        ),
    ],
)

h5 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Custom plotly template', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'Experiment with customizing plotly templates',
                    className='card-text',
                ),
            ]
        ),
    ],
)

b1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('The data', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'The EDA of the data was quite straight forward. Usually one would invest more'
                    ' time in the EDA, looking for NAN, think about how to handle missing information,'
                    ' take a look at the distribution of the data, data types and so on.',
                    className='card-text',
                ),
            ]
        ),
    ]
)

b2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Flexibility of layout', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'I did not try to vary the screen size and adapt the layout accordingly, '
                    'but I know more or less how to tackle this',
                    className='card-text',
                ),
            ]
        ),
    ],
)

b3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('General layout', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'Aligning and positioning of components and items is quite time consuming '
                    'and seems to be difficult due to the vast amount of options to achieve it.',
                    className='card-text',
                ),
            ]
        ),
    ],
)

b4 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Use of CSS', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'CSS seems to be handy for styling the apps. Unfortunately I did '
                    'not have the time to investigate how to use it properly. I actually used this.',
                    className='card-text',
                ),
                html.A(
                    'link',
                    href='https://community.plotly.com/t/change-textcolor-for-dropdown-menu/35230/3',
                    style={'color': '#375a7f'}
                )
            ]
        ),
    ],
)

b5 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('DASH Leaflet interactivity', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'I would like to hide all other markers and keep only the selected ones '
                    '(neighbors) and change the marker color to match the colors from the graph',
                    className='card-text',
                ),
            ]
        ),
    ],
)

b6 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Graphs', className='card-title', style={'color': '#375a7f'}),
                html.P(
                    'Formatting of titles, axes legends',
                    className='card-text',
                ),
            ]
        ),
    ],
)

layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H3('Satisfied with'),
                    width=6,
                    className='text-center'
                ),
                dbc.Col(
                    html.H3('Could be better'),
                    width=6,
                    className='text-center')
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    h1,
                    width=3
                ),
                dbc.Col(
                    [
                        h2,
                        h3,
                        h4,
                        h5
                    ], width=3,
                ),
                dbc.Col(
                    [
                        b1,
                        b2,
                        b3,
                    ], width=3
                ),
                dbc.Col(
                    [
                        b4,
                        b5,
                        b6
                    ], width=3
                )
            ]
        )
    ], fluid=True
)
