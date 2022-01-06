CREATE DATABASE IF NOT EXISTS COVIDDB;

USE COVIDDB;

DROP TABLE IF EXISTS statesData;

CREATE TABLE statesData (
    fips varchar(10),
    country varchar(50),
    state varchar(50),
    county varchar(60),
    level varchar(60),
    lat varchar(60),
    locationId varchar(60),
    longitute varchar(60),
    population varchar(60),
    metrics_testPositivityRatio varchar(60),
    metrics_testPositivityRatioDetails_source varchar(60),
    metrics_caseDensity varchar(60),
    metrics_contactTracerCapacityRatio varchar(60),
    metrics_infectionRate varchar(60),
    metrics_infectionRateCI90 varchar(60),
    unused1 varchar(60),
    unused2 varchar(60),
    unused3 varchar(60),
    unused4 varchar(60),
    unused5 varchar(60),
    metrics_icuCapacityRatio varchar(60),
    riskLevels_overall varchar(60),
    riskLevels_testPositivityRatio varchar(60),
    riskLevels_caseDensity varchar(60),
    riskLevels_contactTracerCapacityRatio varchar(60),
    riskLevels_infectionRate varchar(60),
    unused6 varchar(60),
    riskLevels_icuCapacityRatio varchar(60),
    actuals_cases varchar(60),
    actuals_deaths varchar(60),
    actuals_positiveTests varchar(60),
    actuals_negativeTests varchar(60),
    actuals_contactTracers varchar(60),
    actuals_hospitalBeds_capacity varchar(60),
    actuals_hospitalBeds_currentUsageTotal varchar(60),
    actuals_hospitalBeds_currentUsageCovid varchar(60),
    unused7 varchar(60),
    actuals_icuBeds_capacity varchar(60),
    actuals_icuBeds_currentUsageTotal varchar(60),
    actuals_icuBeds_currentUsageCovid varchar(60),
    unused8 varchar(60),
    actuals_newCases varchar(60),
    actuals_vaccinesDistributed varchar(60),
    actuals_vaccinationsInitiated varchar(60),
    actuals_vaccinationsCompleted varchar(60),
    lastUpdatedDate varchar(60),
    url varchar(60),
    metrics_vaccinationsInitiatedRatio varchar(60),
    metrics_vaccinationsCompletedRatio varchar(60),
    actuals_newDeaths varchar(60),
    actuals_vaccinesAdministered varchar(60),
    cdcTransmissionLevel varchar(60)
);