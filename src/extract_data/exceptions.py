# src/extract_data/exceptions.py

class MissingKeyError(Exception):
    def __init__(self, key, file):
        self.key = key
        self.file = file
        super().__init__(f"Missing key '{key}' in file '{file}'")