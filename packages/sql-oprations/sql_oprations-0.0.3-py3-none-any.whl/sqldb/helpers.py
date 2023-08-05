import csv
import io
import logging


def csv_to_list(csv_file):
    """
    convert csv to list of tuple objects
    :param csv_file:
    :return: list of tuples
    """
    try:
        with io.TextIOWrapper(csv_file, encoding='utf-8') as text_file:
            reader = csv.reader(text_file, delimiter=',')
            line_count = 0
            csv_list = []

            for line in reader:
                if line_count == 0:
                    columns = tuple(line)
                    csv_list.append(columns)
                else:
                    value = tuple(line)
                    csv_list.append(value)

            return csv_list
    except csv.Error as err:
        logging.error(f"can't able to read csv file {csv_file}, Error: {err} ")
        return -1








