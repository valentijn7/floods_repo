# src/main.py

import sys
import extract


# This main function is used to extract data from the API.
# Later, a governing function for analysis will be added.


def main():
    print("BEWARE: as of October 2024, the API contains no data issued before July 2024\n")
    
    try:
        country, a, b = extract.validate_args(sys.argv)
        _, _, _ = extract.extract_country_data_for_time_delta(
            "../data/keys/key.txt", country, (a, b)
            )
        print(
            f"Extraction succesful for {country} with issue date {str(a)[:10]} "
            f"and {(b - a).days} issue days of data"
        )
    except Exception as exc:
        extract.handle_exception(exc)


if __name__ == '__main__':
    main()