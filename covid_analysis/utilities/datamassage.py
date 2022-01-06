import pandas as pd
import logging


logger = logging.getLogger("__main__.datamassage")
DAYS = 360
states_url_time = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=6671d1f59ae34df4a51378c75ca559c7"
states_url = (
    "https://api.covidactnow.org/v2/states.csv?apiKey=6671d1f59ae34df4a51378c75ca559c7"
)


# Loading or Reading the data
def read_coviddata_api(url, url_timeseries):
    logger.info(f"Reading api from {url} and {url_timeseries}")
    statesDatatime = pd.read_csv(
        url_timeseries, index_col=False, dtype={"fips": object}
    )
    statesData = pd.read_csv(url, index_col=False, dtype={"fips": object})
    statesDatatime = _massage_timeseries_data(statesDatatime=statesDatatime)
    return _add_state_abbreviation(statesDatatime), _add_state_abbreviation(statesData)


# Adding State Abbrevation to any dataset if it has state column
def _add_state_abbreviation(input_df):
    statesAbbr = pd.read_csv("./data/state-abbr.csv")
    # Merge dataset with State Abbrevations
    output_df = pd.merge(
        left=input_df, right=statesAbbr, how="left", left_on="state", right_on="state"
    )
    logger.info(f"Added abbrevation to the dataframe provided....")
    return output_df


# Cleanup any unused columns and formatting as required
def _massage_timeseries_data(statesDatatime):
    # Cleaning up of data for usage
    logger.info(f"Cleaning up the states Dataframe")
    for col in statesDatatime.columns:
        if col in "unused":
            statesDatatime.drop(col, axis=1, inplace=True)
        else:
            statesDatatime[col] = statesDatatime[col]

    statesDatatime["date"] = pd.to_datetime(statesDatatime["date"])
    statesDatatime["actuals.cases"] = (
        statesDatatime["actuals.cases"].fillna(method="ffill").fillna(0)
    )
    statesDatatime["actuals.deaths"] = (
        statesDatatime["actuals.deaths"].fillna(method="ffill").fillna(0)
    )
    statesDatatime["actuals.vaccinationsCompleted"] = statesDatatime[
        "actuals.vaccinationsCompleted"
    ].fillna(0)
    statesDatatime["actuals.newCases"] = statesDatatime["actuals.newCases"].fillna(0)
    statesDatatime["DateNew"] = pd.to_datetime(statesDatatime["date"]).dt.strftime(
        "%Y%m%d"
    )
    statesDatatime["text"] = (
        "<br>"
        + " Cases "
        + statesDatatime["actuals.cases"].astype(str)
        + "<br>"
        + " Deaths "
        + statesDatatime["actuals.deaths"].astype(str)
        + "<br>"
        + " NewCases "
        + statesDatatime["actuals.newCases"].astype(str)
        + "<br>"
        + " vaccinationsCompleted "
        + statesDatatime["actuals.vaccinationsCompleted"].astype(str)
    )
    statesDatatime["actuals.newCases"] = pd.to_numeric(
        statesDatatime["actuals.newCases"]
    )
    return statesDatatime

#Converted the dataframes into required data sets specifically used for each graphs and created a subset dataframe.
def subset_data_graph(statesData, statesDatatime):

    max_date = pd.to_datetime(max(statesDatatime["date"]))
    max_date_2 = max_date - pd.to_timedelta(2, unit="d")
    filtered_date = max_date - pd.to_timedelta(DAYS, unit="d")
    previous_data = statesDatatime[statesDatatime.date == max_date_2]

    current = statesData[["actuals.cases", "actuals.deaths", "actuals.newCases"]].sum()
    previous = previous_data[
        ["actuals.cases", "actuals.deaths", "actuals.newCases"]
    ].sum()

    # Identify top 10 states for number of cases
    top_states = statesData.nlargest(10, ["actuals.cases"])["state"]
    filtered_days_data = statesDatatime[
        (statesDatatime["date"] > filtered_date) & (statesDatatime["date"] <= max_date)
    ]
    line_graph_data = filtered_days_data[filtered_days_data["state"].isin(top_states)]

    monthend = pd.concat(
        [
            statesDatatime[
                (statesDatatime["date"].dt.is_month_end)
                & ~(statesDatatime.date == max_date)
            ],
            previous_data,
        ]
    )

    statesdatanew = monthend[
        [
            "DateNew",
            "country",
            "state",
            "actuals.cases",
            "actuals.deaths",
            "actuals.newCases",
            "actuals.vaccinationsCompleted",
            "actuals.vaccinesAdministered",
            "actuals.icuBeds.capacity",
            "actuals.icuBeds.currentUsageTotal",
            "actuals.icuBeds.currentUsageCovid",
            "statename",
            "text",
        ]
    ]
    statesdatanew = statesdatanew.assign(
        actuals_icuBeds_remaining=statesdatanew["actuals.icuBeds.capacity"]
        - statesdatanew["actuals.icuBeds.currentUsageTotal"]
    )

    statesdatanew = statesdatanew.sort_values(by=["DateNew"])
    return current, previous, statesdatanew, line_graph_data
