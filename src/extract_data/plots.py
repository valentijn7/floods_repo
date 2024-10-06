from getters import get_json_file

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
        "axes.labelsize": 8,     # fontsize for x and y labels
        "xtick.labelsize": 8,    # fontsize of the tick labels
        "ytick.labelsize": 8,    # fontsize of the tick labels
        "legend.fontsize": 8,    # fontsize of the legen
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