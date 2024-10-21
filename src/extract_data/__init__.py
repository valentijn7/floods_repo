# src/extract_data/__init__.py
# Runs automatically when extract_data is imported

__version__ = '0.0.0' # MAJOR.MINOR.PATCH versioning
__author__ = 'valentijn7' # GitHub username


from .getters import get_API_key
from .getters import get_json_file
from .call_ListGauges import get_ListGauges
from .call_GetGaugeModel import get_GetGaugeModel
from .call_QueryGaugeForecasts import get_QueryGaugeForecasts


def init():
    print('GoogleFloodHub-data-extractor initialized')


init()