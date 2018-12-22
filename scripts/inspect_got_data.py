import logging
import os
import pandas as pd
import sys as sys

def main(argv=None):
    """
	Utilize Pandas library to read in character_more_info.csv file
	(comma delimited).
	Extract cultures and houses column data.  Filter out duplicate values and NaN values and sort the
	series in alphabetical order. Write out each series to a .csv file for inspection.
	"""

    if argv is None:
        argv = sys.argv

    msg = [
        'Source file read {0}',
        'cultures written to file {0}',
        'houses written to tile {0}'
    ]

    # Setting logging format and default level
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    # Read in character_more_info data set (comma separator)
    character_csv = './input/csv/character_more_info.csv'
    character_data_frame = read_csv(character_csv, ',')
    logging.info(msg[0].format(os.path.abspath(character_csv)))

    # Write cultures to a .csv file.
    character_culture = extract_filtered_series(character_data_frame, 'culture')
    cuture_csv = './output/character_culture.csv'
    write_series_to_csv(character_culture, cuture_csv, ',', False)
    logging.info(msg[1].format(os.path.abspath(cuture_csv)))

    # Write houses to a .csv file.¥
    character_house = extract_filtered_series(character_data_frame, 'house')
    house_csv = './output/character_house.csv'
    write_series_to_csv(character_house, house_csv, ',', False)
    logging.info(msg[2].format(os.path.abspath(house_csv))) 

def extract_filtered_series(data_frame, column_name):
    """
    Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
    Duplicate values and NaN or blank values are dropped from the result set which is
    returned sorted (ascending).
    :param data_frame: Pandas DataFrame
    :param column_name: column name string
    :return: Panda Series one-dimensional ndarray
    """
    return data_frame[column_name].drop_duplicates().dropna().sort_values()


def read_csv(path, delimiter=','):
    """
    Utilize Pandas to read in *.csv file.
    :param path: file path
    :param delimiter: field delimiter
    :return: Pandas DataFrame
    """
    return pd.read_csv(path, sep=delimiter, engine='python')


def write_series_to_csv(series, path, delimiter=',', row_name=True):
    """
    Write Pandas DataFrame to a *.csv file.
    :param series: Pandas one dimensional ndarray
    :param path: file path
    :param delimiter: field delimiter
    :param row_name: include row name boolean
    """
    series.to_csv(path, sep=delimiter, index=row_name)

if __name__ == '__main__':
	sys.exit(main())