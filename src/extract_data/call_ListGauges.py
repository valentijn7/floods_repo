from typing import List, Dict, Any
import requests
import pandas as pd

from getters import get_API_key, get_json_file


def generate_url_ListGauges(path_to_key : str) -> str:
    """
    Generate the URL to get the list of gauges for a specific country

    :param path_to_key: path to the .txt file containing the API key
    :return: the URL
    """
    base_url = 'https://floodforecasting.googleapis.com/v1/gauges:searchGaugesByArea'
    return f'{base_url}?key={get_API_key(path_to_key)}'


def make_request_ListGauges(country_code : str, path_to_key : str) -> List[Dict[str, Any]]:
    """
    Make the API request for the list of gauges for a specific country

    :param url: the URL
    :return: the list of gauges
    """
    response = requests.post(
        generate_url_ListGauges(path_to_key),
        json = {'regionCode': country_code}
    )
    
    return response


def verify_ListGauges(response : Any) -> List[Dict[str, Any]]:
    """
    Get the list of gauges for a specific country, and verify the response

    :param country_code: the country code
    :param path_to_key: path to the .txt file containing the API key
    :return: the list of gauges
    """
    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code} -- {response.text}')

    try:
        return response.json()['gauges']
    except ValueError as exc:
        raise Exception(f'Error parsing .json: {exc} -- {response.text}')
    

def convert_ListGauges_to_df(gauges : List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert the list of gauges to a pd.DataFrame

    :param gauges: the list of gauges
    :return: the DataFrame
    """
    df = pd.DataFrame(gauges)
    df['latitude'] = df['location'].apply(lambda x: x['latitude'])
    df['longitude'] = df['location'].apply(lambda x: x['longitude'])
    df.drop(columns = ['location'], inplace = True)
    return df


def get_ListGauges(country : str, path_to_key : str) -> pd.DataFrame:
    """
    Get the list of gauges for a specific country by calling helper functions which:
    - generate the URL;
    - make the request;
    - verify the response; and
    - convert to a pd.DataFrame in the end.

    :param country: the country
    :param path_to_key: path to the .txt file containing the API key
    :return: DataFrame with the gauges
    """
    return convert_ListGauges_to_df(
        verify_ListGauges(
            make_request_ListGauges(
                get_json_file("../../data/country_codes.json")[country], path_to_key
            )
        )
    )