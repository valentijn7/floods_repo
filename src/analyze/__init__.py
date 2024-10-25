# src/analyze/__init__.py

__version__ = '0.0.0' # MAJOR.MINOR.PATCH versioning
__author__ = 'valentijn7' # GitHub username

print('\nRunning __init__.py for GoogleFloodHub-data-analyzer')

from .getters import get_country_data
from .getters import get_country_polygon
from .transform import convert_df_to_gdf
from .transform import subset_country_gauge_coords
from .transform import make_subset_for_gauge_and_issue_time
from .plots import map_gauge_coordinates_of_country
from .plots import plot_x_days_of_gauge_forecast_for_issue_time


print('GoogleFloodHub-data-analyzer initialized\n')