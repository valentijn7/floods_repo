# src/extract_data/plots.py

from .getters import get_json_file

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
import datetime
import seaborn as sns


def get_custom_palette(n_colours) -> list:
    """
    Returns a custom palette with red and dark blue colors

    :param n_colours: number of colours in the palette
    :return: list with n colours
    """
    cmap = LinearSegmentedColormap.from_list("red_to_blue",
                                             ['#DB0A13', '#092448'],
                                             N = n_colours)
    return [cmap(idx) for idx in range(cmap.N)]


def set_TeX_style() -> None:
    """
    Sets the style environment for the plots to use TeX for text rendering
    """
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Computer Modern Serif",
        "axes.labelsize": 10,     # fontsize for x and y labels
        "xtick.labelsize": 10,    # fontsize of the tick labels
        "ytick.labelsize": 10,    # fontsize of the tick labels
        "legend.fontsize": 10,    # fontsize of the legen
    })


def set_plot_style(
        TeX: bool = False, style: str = 'ticks', context: str = None) -> None:
    """
    Sets the style environment for the plots, including:
    - through the set_TeX_style function:
        - whether to use TeX for text rendering
        - the font family for titles, labels, etc.
        - the font size for titles, labels, etc.
    - seaborn style to use (default = 'ticks')
    - the context for the plot (default = 'notebook')
    
    :param TeX: whether to use TeX for text rendering
    :param style: seaborn style to use
    :param context: the context for the plot
    """
    if TeX:
        set_TeX_style()
    sns.set_theme(style = 'ticks')
    sns.set_context(context) if context else None


def make_subset_for_gauge_and_issue_time(
        df: pd.DataFrame, gauge: str, issue_date: datetime.datetime) -> pd.DataFrame:
    """
    Create a subset of a DataFrame for a specific gauge and issue time

    :param df: DataFrame with forecasted values
    :param gauge: ID of the gauge
    :param issue_time: issue time of the forecast
    :return: subset of the DataFrame
    """
    if not all(df['gaugeId'].apply(lambda x: isinstance(x, str))):
        df['gaugeId'] = df['gaugeId'].astype(str)
    if not all(df['issue_date'].apply(lambda x: isinstance(x, datetime.date))):
        df['issue_date'] = pd.to_datetime(df['issue_date']).dt.date
    assert all(df['gaugeId'].apply(lambda x: isinstance(x, str))), \
        "gaugeId column contains non-string values, subseting hindered"
    assert all(df['issue_date'].apply(lambda x: isinstance(x, datetime.date))), \
        "issue_date column contains non-date values, subsetting hindered"

    return df[(df['gaugeId'] == gauge) & (df['issue_date'] == issue_date.date())]  


def create_dates_series(start_date : datetime.datetime, delta: int) -> pd.Series:
    """
    Create a series of dates starting from a given date and going on for a given number of days

    :param start_date: starting date
    :param delta: number of days
    :return: Series of dates
    """
    return pd.Series(
        # minus one here because, strangely enough, the first forecasted
        # date is one day in the past compared to the issue date...
        [start_date.date() + datetime.timedelta(days = idx - 1) for idx in range(0, delta + 1)]
    )


def set_custom_date_ticks(ax: plt.Axes, dates: pd.Series) -> None:
    """
    Set custom date ticks on the x-axis of a plot, where only
    the first and final date are displayed, while keeping the ticks

    :param ax: Axes object
    :param dates: Series of dates (datetime.date objects)
    """
    ax.set_xticks(dates)
    x_labels = [
        dates.iloc[0].strftime('%Y-%m-%d')
    ] + [''] * (len(dates) - 2) + [
        dates.iloc[-1].strftime('%Y-%m-%d')
    ]
    ax.set_xticklabels(x_labels)  


def plot_gauge_forecast_for_issue_time(
        df : pd.DataFrame, gauge: str, issue_date : datetime.datetime, country : str = None) -> None:
    """
    Plots with a graph the forecasted values for a specific gauge and issue time

    :param df: DataFrame with forecasted values
    :param gauge: ID of the gauge
    :param issue_time: issue time of the forecast
    :param country: name of the country
    """
    set_plot_style()

    df_subset = make_subset_for_gauge_and_issue_time(df, gauge, issue_date)
    if df_subset.empty:
        print(f"No forecasted values for gauge {gauge} at {issue_date.date()}")
        return

    ax = sns.lineplot(
        x = 'fc_date',
        y = 'fc_value',
        data = df_subset,
        color = '#DB0A13'
    )

    # only display first and final forecast date on date-axis while keeping ticks
    set_custom_date_ticks(
        ax,
        create_dates_series(issue_date, 7)
    )

    plt.title(f'Forecasts for gauge {gauge} in {country}, w/ 1st issue date: {issue_date.date()}')
    plt.xlabel('date')
    plt.ylabel('[m³/s]')
    plt.show()


def plot_week_of_gauge_forecast_for_issue_time(
        df : pd.DataFrame, gauge: str, issue_date : datetime.datetime, country : str = None) -> None:
    """
    Plots the forecasted values for a specific gauge over a week of
    issue times, giving seven graphs in total, each of (7 + 1 =) 8 days length 

    :param df: DataFrame with forecasted values
    :param gauge: ID of the gauge
    :param issue_time: first issue time
    :param country: Name of the country
    """
    set_plot_style()
    plt.figure(figsize = (10, 6))
    custom_palette = get_custom_palette(7)
    
    for idx in range(7): # loop for seven days, aka a week
        df_subset = make_subset_for_gauge_and_issue_time(
            df, gauge, issue_date + datetime.timedelta(days = idx)
        )
        if df_subset.empty:
            print(f"No forecasted values for gauge {gauge} at {issue_date.date()}")
            return

        sns.lineplot(
            x = 'fc_date',
            y = 'fc_value',
            data = df_subset,
            color = custom_palette[idx]
        )

    set_custom_date_ticks(
        plt.gca(),
        create_dates_series(issue_date, 7 + 7) # a week plus lead time
    )

    plt.title(f'Forecasts for gauge {gauge} in {country}, w/ 1st issue date: {issue_date.date()}')
    plt.xlabel('date')
    plt.ylabel('[m³/s]')
    plt.show()


def plot_x_days_of_gauge_forecast_for_issue_time(
        df : pd.DataFrame,
        gauge: str,
        issue_date : datetime.datetime,
        days: int,
        country : str = None,
        TeX: bool = False,
        export: bool = False) -> None:
    """
    Plots the forecasted values for a specific gauge over a month of
    issue times, giving 30 graphs in total, each of (7 + 1 =) 8 days length 

    :param df: DataFrame with forecasted values
    :param gauge: ID of the gauge
    :param issue_time: first issue time
    :param country: Name of the country
    """
    set_plot_style()
    set_TeX_style() if TeX else None
    plt.figure(figsize = (10, 6))
    custom_palette = get_custom_palette(days)
    
    for idx in range(days):
        df_subset = make_subset_for_gauge_and_issue_time(
            df, gauge, issue_date + datetime.timedelta(days = idx)
        )
        if df_subset.empty:
            print(f"No forecasted values for gauge {gauge} at {issue_date.date()}")
            return

        sns.lineplot(
            x = 'fc_date',
            y = 'fc_value',
            data = df_subset,
            color = custom_palette[idx]
        )

    set_custom_date_ticks(
        plt.gca(),
        create_dates_series(issue_date, days + 7) # a week plus lead time
    )

    plt.title(f'Forecasts for gauge {gauge} in {country}, w/ 1st issue date: {issue_date.date()}')
    plt.xlabel('date')
    plt.ylabel('[m³/s]')
    plt.draw()

    if export:
        plt.savefig(f"../../plots/graph_{days}_fcs_of_gauge_{gauge}_at_issue_date_{str(issue_date.date())}.pdf",
                    format = 'pdf',
                    bbox_inches = 'tight',
                    pad_inches = 0.015)
        
    plt.show()


def plot_danger_levels_hist(df: pd.DataFrame, country: str = None, bins: int = 10) -> None:
    """
    Plot histogram of danger levels in the dataset

    :param df: DataFrame with gauge information
    """
    set_plot_style()

    risk_levels = ['dangerLevel', 'extremeDangerLevel', 'warningLevel']
   
    for level in risk_levels:
        ax = sns.histplot(pd.DataFrame(df[level]),
                          color = '#DB0A13',
                          bins = bins)
        
        for patch in ax.patches:
            patch.set_facecolor('#DB0A13')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer = True))
        plt.legend(handles = [Patch(color = '#DB0A13', label = level)])
        plt.xlabel('Cubic meter per second')
        plt.ylabel('Frequency')
        plt.title('Distribution of danger levels in ' + country)
        
        plt.show()


def convert_df_to_gdf(df : pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Convert a DataFrame to a GeoDataFrame by taking the latitude and longitude columns

    :param df: the DataFrame
    :return: the GeoDataFrame
    """
    return gpd.GeoDataFrame(
        df,
        geometry = gpd.points_from_xy(df['longitude'], df['latitude']),
        crs = 'EPSG:4326' # Uniform projection to WGS84
    )


def get_shape_file(file : str) -> gpd.GeoDataFrame:
    """
    Get the shape file for a country

    :param country: the country
    :return: the GeoDataFrame
    """
    try:
        return gpd.read_file(f"../../data/shape_files/{file}")
    except Exception as exc:
        raise Exception(f'Error reading shapefile: {exc}')


def convert_country_code_to_iso_a3(country_code : str) -> str:
    """
    Convert a country code to an ISO A3 code

    :param country_code: the country code
    :return: the ISO A3 code
    """
    return get_json_file("../../data/country_codes_to_ISO_A3.json")[country_code]


def get_country_polygon(country_code : str) -> gpd.GeoDataFrame:
    """
    Get the polygon of a country as a GeoDataFrame

    :param country_code: the country code
    :return: the polygon
    """
    gdf = get_shape_file('ne_110m_admin_0_countries')
    iso_a3 = convert_country_code_to_iso_a3(country_code)

    country_row = gdf[gdf['SOV_A3'] == iso_a3]
    if country_row.empty:
        raise ValueError(f'Country with ISO A3 code {country_code} not found')
    
    return gpd.GeoDataFrame(geometry = [country_row['geometry'].values[0]])


def map_gauge_coordinates_of_country(df : pd.DataFrame, country : str) -> None:
    """
    Map gauge coordinates

    :param df: the DataFrame with the gauges
    :return: the GeoDataFrame
    """
    gdf = convert_df_to_gdf(df)
    shape = get_country_polygon(get_json_file("../../data/country_codes.json")[country])

    fig, ax = plt.subplots()
    shape.plot(ax = ax, color = 'lightgrey')
    gdf.plot(ax = ax, color = 'red', markersize = 10)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Gauge locations for {country}')
    ax.set_aspect('equal') # Ensure unwarped aspect ratio
    plt.show()