import dash
import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, ServersideOutputTransform

app = DashProxy(
    __name__,
    transforms=[ServersideOutputTransform()],
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {'name': 'viewport',
         'content': 'width=device-width, initial-scale=1.0'}
    ]
)

navbar = dbc.NavbarSimple(
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("top_nav")
        ],
    ),
    brand="Liquor Store Fun",
    color="primary",
    dark=True,
    className="mb-2",
    fluid=True
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=False)
