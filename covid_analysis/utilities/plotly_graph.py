import utilities.datamassage as datamassage
from utilities.parameters import Params
import logging
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# logger module to log the information
logger = logging.getLogger("__main__.plotly_dash.plotly_graph")

logger.info("Step-0 Initialize generic parameters")
params = Params("params.ini")
# API call to get the data
logger.info("Step-1 API Call to get the data")
statesDatatime, statesData = datamassage.read_coviddata_api(
    url=params.states_url, url_timeseries=params.states_url_timeseries
)
# preparing data for visualization
logger.info("Step-2 Preparing the data for Vizualization")
(
    current,
    previous,
    statesdatanew,
    line_graph_data,
) = datamassage.subset_data_graph(statesData, statesDatatime)

# ininating dash class to create new dashboard
app = dash.Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                "https://codepen.io/chriddyp/pen/bWLwgP.css",
            ],
        )
# Displaying new cases, total cases and deaths along with the delta indicator which compares previous 
# count to current count and display as a percentage. 
# It displays green or red based on the increase or decrease of the cases and deaths.
@app.callback(Output("indicator", "figure"), [Input("update", "n_intervals")])
def display_indicator(timer):
    fig = go.Figure()
    fig.add_traces(
        [
            go.Indicator(
                mode="number+delta",
                value=current["actuals.cases"],
                title={
                    "text": "REPORTED CASES<br><span style='font-size:0.8em;color:navy'>Total</span>"
                },
                delta={
                    "reference": previous["actuals.cases"],
                    "relative": True,
                    "font": {"size": 12},
                },
                domain={"x": [0, 0.33], "y": [0, 0]},
            ),
            go.Indicator(
                mode="number+delta",
                value=current["actuals.deaths"],
                title={
                    "text": "REPORTED DEATHS<br><span style='font-size:0.8em;color:navy'>Total</span>"
                },
                delta={
                    "reference": previous["actuals.deaths"],
                    "relative": True,
                    "font": {"size": 12},
                },
                domain={"x": [0.33, 0.66], "y": [0, 0]},
            ),
            go.Indicator(
                mode="number+delta",
                value=current["actuals.newCases"],
                title={
                    "text": "REPORTED NEW CASES<br><span style='font-size:0.8em;color:navy'>Total</span>"
                },
                delta={
                    "reference": previous["actuals.newCases"],
                    "relative": True,
                    "font": {"size": 12},
                },
                domain={"x": [0.66, 1], "y": [0, 0]},
            ),
        ]
    )
    fig.update_traces(delta_font={"size": 12})

    return fig
# Displaying an animation graph on the USA map for cases, deaths and vaccinations which would increment monthly
@app.callback(Output("choropleth", "figure"), [Input("filter", "value")])
def display_choropleth(filter):
    fig = px.choropleth(
        statesdatanew,
        locations="state",
        color=filter,
        hover_name="state",
        hover_data=["text"],
        animation_frame="DateNew",
        locationmode="USA-states",
        projection="albers usa",
        color_continuous_scale="Plasma",
        labels={
            "actuals.cases": "Cases",
            "actuals.deaths": "Deaths",
            "actuals.vaccinesAdministered": "Vaccines Administered",
            "DateNew": "Date",
            "text": "Description",
        },
        height=600,
    )

    fig.update_layout(
        title=dict(font=dict(size=25), x=0.5, xanchor="center"),
        margin=dict(l=60, r=60, t=50, b=50),
        title_text="US Covid Analysis (Hover for breakdown)",
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            showlakes=True,  # lakes
            lakecolor="rgb(255, 255, 255)",
        ),
    )

    return fig
# Displaying the line graph for top 10 states for new cases
@app.callback(Output("linegraph", "figure"), [Input("update", "n_intervals")])
def display_linegraph(timer):
    fig = px.line(
        line_graph_data, x="date", y="actuals.newCases", color="state"
    )

    fig.update_layout(
        title={
            "text": "Line Graph for TOP 10 States for new cases",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis_title="Date",
        yaxis_title="New Cases",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list(
                    [
                        dict(
                            args=[{"yaxis.type": "linear"}],
                            label="LINEAR",
                            method="relayout",
                        ),
                        dict(
                            args=[{"yaxis.type": "log"}],
                            label="LOG",
                            method="relayout",
                        ),
                    ]
                ),
            ),
        ],
    )

    return fig
#Displaying the pie chart for the total cases and remaining icu beds for the selected state.
@app.callback(
    Output(component_id="my-graph", component_property="figure"),
    Input(component_id="drop-down", component_property="value"),
)
def update_line_graph(country_chosen):
    dff = statesdatanew[statesdatanew.statename.isin(country_chosen)]
    fig = px.line(
        data_frame=dff,
        x="DateNew",
        y="actuals.cases",
        color="statename",
        custom_data=[
            "statename",
            "actuals.newCases",
            "actuals.icuBeds.currentUsageCovid",
            "actuals_icuBeds_remaining",
        ],
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cases",
    )
    fig.update_traces(mode="lines+markers")
    return fig
#Displaying the line graph for the total cases for the selected state.
@app.callback(
    Output(component_id="pie-graph", component_property="figure"),
    Input(component_id="my-graph", component_property="hoverData"),
    Input(component_id="my-graph", component_property="clickData"),
    Input(component_id="my-graph", component_property="selectedData"),
    Input(component_id="drop-down", component_property="value"),
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen):
    if hov_data is None:
        dff2 = statesdatanew[statesdatanew.statename.isin(country_chosen)]
        dff2 = dff2[dff2.DateNew == "20211130"]
        fig2 = px.pie(
            data_frame=dff2,
            values="actuals_icuBeds_remaining",
            names="statename",
            title="ICU Bed Remaining for 20211130",
        )
        return fig2
    else:
        dff2 = statesdatanew[statesdatanew.statename.isin(country_chosen)]
        hov_date = hov_data["points"][0]["x"]
        dff2 = dff2[dff2.DateNew == hov_date]
        fig2 = px.pie(
            data_frame=dff2,
            values="actuals_icuBeds_remaining",
            names="statename",
            title=f"ICU Bed Remaining for: {hov_date}",
        )
        return fig2
