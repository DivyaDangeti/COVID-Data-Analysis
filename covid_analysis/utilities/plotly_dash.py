from utilities.plotly_graph import app, statesdatanew
from dash import html, dcc
import dash_bootstrap_components as dbc
import logging


logger = logging.getLogger("__main__.plotly_graph")

logger.info("Step-1 Bulding your skeleton for app...")

##########################################################################
#Skeleton of the app
##########################################################################

#Creating a radio button
radiobutton = html.Div(
    [
        dbc.Label("Select one option for filtering:"),
        dcc.RadioItems(
            id="filter",
            options=[
                {"value": "actuals.cases", "label": "Cases"},
                {"value": "actuals.deaths", "label": "Deaths"},
                {
                    "value": "actuals.vaccinesAdministered",
                    "label": "Vaccines Administered",
                },
            ],
            value="actuals.cases",
            labelStyle={"display": "inline-block"},
        ),
    ]
)

#Creating a drop down
dropdown = html.Div(
    [
        dcc.Dropdown(
            id="drop-down",
            value=["California", "Florida"],
            multi=True,
            options=[
                {"label": x, "value": x} for x in statesdatanew.statename.unique()
            ],
        ),
        html.Div(
            [
                dcc.Graph(id="pie-graph", figure={}, className="six columns"),
                dcc.Graph(
                    id="my-graph",
                    figure={},
                    clickData=None,
                    hoverData=None,
                    config={
                        "staticPlot": False,
                        "scrollZoom": True,
                        "doubleClick": "reset",  # 'reset', 'autosize' or 'reset+autosize', False
                        "showTips": False,
                        "displayModeBar": True,  # True, False, 'hover'
                        "watermark": True,
                    },
                    className="six columns",
                ),
            ]
        ),
    ]
)

#Creating the layout for the Dash APP
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    src="assets/unh.png",
                                    top=True,
                                    style={"width": "9rem", "padding": "10px"},
                                ),
                                html.H1(
                                    "COVID DATA ANALYSIS",
                                    style={
                                        "text-align": "center",
                                        "color": "navy",
                                    },
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dcc.Graph(
                                                    id="indicator",
                                                    figure={},
                                                    config={"displayModeBar": False},
                                                )
                                            ]
                                        ),
                                        dbc.Row([radiobutton]),
                                        dbc.Row(
                                            [
                                                dcc.Graph(
                                                    id="choropleth",
                                                    figure={},
                                                    config={"displayModeBar": False},
                                                )
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dcc.Graph(
                                                    id="linegraph",
                                                    figure={},
                                                    config={"displayModeBar": False},
                                                )
                                            ]
                                        ),
                                        dbc.Row([dropdown]),
                                    ]
                                ),
                            ],
                        )
                    ]
                )
            ]
        ),
        dcc.Interval(id="update", n_intervals=0, interval=1000 * 5),
    ]
)

#Assign the layout to the app
app.layout = layout
