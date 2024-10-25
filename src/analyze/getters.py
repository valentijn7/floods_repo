# src/analyze/getters.py

import datetime
import pandas as pd


def import_ListGauges_data(country: str) -> pd.DataFrame:
    """
    Imports the list of gauges for a given country from data/processed/ListGauges

    :param country: the country for which the list of gauges should be imported
    :return a dataframe containing the .csv data
    """
    return pd.read_csv(
        f"../data/processed/ListGauges/{country.lower()}_gauges_listed.csv",
        sep = ';',
        decimal = '.',
        encoding = 'utf-8'
    )


def import_GetGaugeModel_data(country: str) -> pd.DataFrame:
    """
    Imports the gauge model data for a given country from data/processed/GetGaugeModel

    :param country: the country for which the gauge model data should be imported
    :return a dataframe containing the .csv data
    """
    return pd.read_csv(
        f"../data/processed/GetGaugeModel/{country.lower()}_gauge_models_metadata.csv",
        sep = ';',
        decimal = '.',
        encoding = 'utf-8'
    )


def validate_date_string(date: str) -> bool:
    """
    Validates a date string in the format YYYY-MM-DD

    :param date: the date string to validate
    :return True if the date string is valid, False otherwise
    """
    # Check if the date string is in the correct format and otherwise print what the correct format should be and return false
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return False


def import_country_forecast_data(country: str, a: str, b: str) -> pd.DataFrame:
    """
    Imports the forecast data for a given country from data/processed/GetGaugeModel.
    It needs as parameters the country and time delta (= starting and ending issue
    time) of interest such that the exact correct file can be imported

    :param country: the country for which the forecast data should be imported
    :param a: the starting issue time of interest
    :param b: the ending issue time of interest
    :return a dataframe containing the .csv data
    """
    if not validate_date_string(a) or not validate_date_string(b):
        return None
    return pd.read_csv(
        f"../data/floods_data/{country.lower()}/{a}_to_{b}.csv",
        index_col = 0,
        sep = ';',
        decimal = '.',
        encoding = 'utf-8'
    )


def get_country_data(country: str, a: str, b: str) -> pd.DataFrame:
    """
    Imports three pieces of data for a given country:
    - metadata per country (eg containing the gauges and their coordinates)
    - metadata per gauge (eg containing the danger levels)
    - forecast data per gauge

    :param country: the country for which the data should be imported
    :param a: the starting issue time of interest
    :param b: the ending issue time of interest
    :return dataframes containing the three pieces of data
    """
    df_gauges = import_ListGauges_data(country)
    df_gauge_meta = import_GetGaugeModel_data(country)
    df_forecasts = import_country_forecast_data(country, a, b)

    return df_gauges, df_gauge_meta, df_forecasts