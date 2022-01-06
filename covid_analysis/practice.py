import mysql.connector
from mysql.connector import Error
import pandas as pd
import utilities.helpers as helper

states_url = (
    "https://api.covidactnow.org/v2/states.csv?apiKey=6671d1f59ae34df4a51378c75ca559c7"
)
counties_url = "https://api.covidactnow.org/v2/counties.csv?apiKey=6671d1f59ae34df4a51378c75ca559c7"

statesData = pd.read_csv(states_url, index_col=False)
print(statesData.columns)
print(statesData.head())


# statesData[pd.isnull(statesData)] = None
statesData.where(pd.notnull(statesData), None)
statesData=helper.reading_url_txt(states_url)

try:
    conn = mysql.connector.connect(user="Gandhi", password="Mysql123", database='COVIDDB', host="127.0.0.1")
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS COVIDDB")
        print("COVIDDB database is created")

    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute("DROP TABLE IF EXISTS statesData;")
        print("Creating table....")
        cursor.execute(
            """CREATE TABLE COVIDDB.statesData ( 		
                fips	varchar(10)	,
                country	varchar(50)	,
                state	varchar(50)	,
                county	varchar(60)	,
                level	varchar(60)	,
                lat	varchar(60)	,
                locationId	varchar(60)	,
                longitute	varchar(60)	,
                population	varchar(60)	,
                metrics_testPositivityRatio	varchar(60)	,
                metrics_testPositivityRatioDetails_source	varchar(60)	,
                metrics_caseDensity	varchar(60)	,
                metrics_contactTracerCapacityRatio	varchar(60)	,
                metrics_infectionRate	varchar(60)	,
                metrics_infectionRateCI90	varchar(60)	,
                unused1	varchar(60)	,
                unused2	varchar(60)	,
                unused3	varchar(60)	,
                unused4	varchar(60)	,
                unused5	varchar(60)	,
                metrics_icuCapacityRatio	varchar(60)	,
                riskLevels_overall	varchar(60)	,
                riskLevels_testPositivityRatio	varchar(60)	,
                riskLevels_caseDensity	varchar(60)	,
                riskLevels_contactTracerCapacityRatio	varchar(60)	,
                riskLevels_infectionRate	varchar(60)	,
                unused6	varchar(60)	,
                riskLevels_icuCapacityRatio	varchar(60)	,
                actuals_cases	varchar(60)	,
                actuals_deaths	varchar(60)	,
                actuals_positiveTests	varchar(60)	,
                actuals_negativeTests	varchar(60)	,
                actuals_contactTracers	varchar(60)	,
                actuals_hospitalBeds_capacity	varchar(60)	,
                actuals_hospitalBeds_currentUsageTotal	varchar(60)	,
                actuals_hospitalBeds_currentUsageCovid	varchar(60)	,
                unused7	varchar(60)	,
                actuals_icuBeds_capacity	varchar(60)	,
                actuals_icuBeds_currentUsageTotal	varchar(60)	,
                actuals_icuBeds_currentUsageCovid	varchar(60)	,
                unused8	varchar(60)	,
                actuals_newCases	varchar(60)	,
                actuals_vaccinesDistributed	varchar(60)	,
                actuals_vaccinationsInitiated	varchar(60)	,
                actuals_vaccinationsCompleted	varchar(60)	,
                lastUpdatedDate	varchar(60)	,
                url	varchar(60)	,
                metrics_vaccinationsInitiatedRatio	varchar(60)	,
                metrics_vaccinationsCompletedRatio	varchar(60)	,
                actuals_newDeaths	varchar(60)	,
                actuals_vaccinesAdministered	varchar(60)	,
                cdcTransmissionLevel	varchar(60)	)
            """
        )
        print("statesData table is created....")
        for row in statesData.splitlines():
            print(tuple(row.split (",")))
            sql = '''INSERT INTO COVIDDB.statesData (fips,
                    country	,
                    state	,
                    county	,
                    level	,
                    lat	,
                    locationId	,
                    longitute	,
                    population	,
                    metrics_testPositivityRatio	,
                    metrics_testPositivityRatioDetails_source	,
                    metrics_caseDensity	,
                    metrics_contactTracerCapacityRatio	,
                    metrics_infectionRate	,
                    metrics_infectionRateCI90	,
                    unused1	,
                    unused2	,
                    unused3	,
                    unused4	,
                    unused5	,
                    metrics_icuCapacityRatio	,
                    riskLevels_overall	,
                    riskLevels_testPositivityRatio	,
                    riskLevels_caseDensity	,
                    riskLevels_contactTracerCapacityRatio	,
                    riskLevels_infectionRate	,
                    unused6	,
                    riskLevels_icuCapacityRatio	,
                    actuals_cases	,
                    actuals_deaths	,
                    actuals_positiveTests	,
                    actuals_negativeTests	,
                    actuals_contactTracers	,
                    actuals_hospitalBeds_capacity	,
                    actuals_hospitalBeds_currentUsageTotal	,
                    actuals_hospitalBeds_currentUsageCovid	,
                    unused7	,
                    actuals_icuBeds_capacity	,
                    actuals_icuBeds_currentUsageTotal	,
                    actuals_icuBeds_currentUsageCovid	,
                    unused8	,
                    actuals_newCases	,
                    actuals_vaccinesDistributed	,
                    actuals_vaccinationsInitiated	,
                    actuals_vaccinationsCompleted	,
                    lastUpdatedDate	,
                    url	,
                    metrics_vaccinationsInitiatedRatio	,
                    metrics_vaccinationsCompletedRatio	,
                    actuals_newDeaths	,
                    actuals_vaccinesAdministered	,
                    cdcTransmissionLevel) VALUES (  %s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s)'''
            cursor.execute(sql, tuple(row.split (",")))
            # the connection is not autocommitted by default, so we must commit to save our changes
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)
