def get_API_key(path : str) -> str:
    """
    Get the API key from a .txt file stored elsewhere

    :param path: path to the .txt file containing the API key
    :return: the API key
    """
    with open(path, 'r') as f:
        return f.read().strip()