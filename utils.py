from sklearn.neighbors import KDTree
import plotly.io as pio
import pandas as pd
import re


def prepare_data():
    """
    function prepares the data for the app.

    - read the raw data
    - filter the DataFrame so that only stores remain which have a location
    - create a KDTree for neighbor search
    - create markers for map
    - create a json which basically is a grouped DataFrame
    """
    # read Raw data
    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/liquor_iowa_2021.csv')

    # find stores without information concerning location and delete these stores
    filt = df.store_location.isnull()
    df = df.drop(df[filt].index)

    # group by store_number
    gb = df.groupby('store_number')

    # create dataframe of locations
    locations = gb.store_location.unique().to_frame()

    coordinates = {}
    for idx, row in zip(locations.index, locations.store_location):
        # information is stored in an array, extract coordinate information
        coords = re.search("\((.*)\)", row[0]).group(1)

        # convert string into float
        lon, lat = map(float, coords.split())

        # save into dictionary
        coordinates[idx] = [lat, lon]

    # replace values in column store_location
    df.store_location = df.store_number.apply(lambda x: coordinates[x])

    # create a list of dictionaries for later use as markers in the map
    markers = [{'id': str(ids), 'lat': coords[0], 'lon': coords[1]} for ids, coords in coordinates.items()]

    # convert date column into date_time
    df.date = pd.to_datetime(df.date)

    # add quarter of the year
    df['quarter'] = df.date.dt.to_period('Q').astype(str)

    # add day of the week
    lookup = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    df['weekday'] = df.date.apply(lambda x: lookup[x.weekday()])

    # group by store_number
    gb = df.groupby('store_number')

    # create a pandas.Series of json (for each group)
    gb = gb.apply(lambda x: x.to_json())

    # create a json from the pandas.Series
    gb = gb.to_json()

    # create a list of StoreLoc Objects (basically store number and location)
    locations = [StoreLoc(k, *v) for k, v in coordinates.items()]

    # create the tree with locations
    kdt = KDTree(locations)

    return gb, [kdt, locations, coordinates], markers


# borrowed from dash_leaflet.express
# I had problems importing dash_leaflet.express, so I just copied this code from github.
# https://github.com/thedirtyfew/dash-leaflet/blob/master/dash_leaflet/express.py#L12-L20
def dicts_to_geojson(dicts, lat="lat", lon="lon"):
    geojson = {"type": "FeatureCollection", "features": []}
    for d in dicts:
        feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [d[lon], d[lat]]}}
        props = [key for key in d.keys() if key not in [lat, lon]]
        if props:
            feature["properties"] = {prop: d[prop] for prop in props}
        geojson["features"].append(feature)
    return geojson


# Class for the store location and number
class StoreLoc:
    def __init__(self, num, lat, lon):
        self.num = num
        self.lat = lat
        self.lon = lon
        self.location = [lat, lon]

    def __getitem__(self, index):
        return self.location[index]

    def __len__(self):
        return 2


# create a custom theme for the plotly figures
# basically use the plotly_dark theme and change the first
# color of the colorway to match with navbar color
pio.templates["plotly_dark_custom"] = pio.templates["plotly_dark"]
pio.templates["plotly_dark_custom"]['layout'].update(
    {'colorway': (
        '#375a7f',
        '#EF553B',
        '#00cc96',
        '#ab63fa',
        '#FFA15A',
        '#19d3f3',
        '#FF6692',
        '#B6E880',
        '#FF97FF',
        '#FECB52'
    )
    }
)


# layout for plotly figures
figure_layout = {
    'margin': {'t': 10, 'b': 10, 'l': 0, 'r': 0},
    'template': 'plotly_dark_custom',
    'paper_bgcolor': 'rgb(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'legend_bgcolor': 'rgba(0,0,0,0)',
    'xaxis': {'tickangle': 45, 'title': ''},
    'height': 380,
    'barmode': 'group'
}

# load dark tiles by Stadia Maps.
url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
