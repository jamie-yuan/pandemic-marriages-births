"""CSC110 Fall 2021 Project: Extracting the Data

This Python module contains the functions that pull the relevant COVID-19, marriage, and birth data
from the COVID19 Data and Vital Events Data by Month datasets using Pandas. The data is formatted
and added to separate dictionaries.

This file is Copyright (c) 2021 Cosette Li, Amelia Riddell, and Jamie Yuan.
"""
import pandas as pd


class MonthNotFoundError(Exception):
    """Exception raised when attempting to number the month in a string that does not contain a
    full month name.
    """

    def __str__(self) -> str:
        """Return a string representation of this error.
        """
        return 'No month was found in the string.'


def covid19_data() -> dict[str: int]:
    """Read and add relevant data from COVID19 Data to a dictionary mapping
    month and year of cases (2018-2020) to its corresponding number of cases, using Pandas.

    Preconditions:
        - The file 'covid19_data.csv' is in the same directory as this file.
    """
    covid_file = 'covid19_data.csv'
    read_file = pd.read_csv(covid_file)
    cases_by_month = {}

    for row in read_file.iterrows():
        date = row[1][3][0:7]
        if (row[1][1] == 'Canada') and ('2020' in date):
            if date not in cases_by_month:
                cases_by_month[date] = 0
            cases_by_month[date] += row[1][5]

    return cases_by_month


def marriage_data() -> dict[str, int]:
    """Read and add relevant marriage data from Vital Events Data by Month to a dictionary mapping
    month and year of marriages (2018-2020) to its corresponding number of marriages, using Pandas.

    Preconditions:
        - The file 'vital_events_data_by_month.csv' is in the same directory as this file.
    """
    marriages_file = 'vital_events_data_by_month.csv'
    read_file = pd.read_csv(marriages_file)
    marriages_by_month = {}

    for row in read_file.iterrows():
        year = str(row[1][1])
        if year in {'2018', '2019', '2020'}:
            month = month_to_number(row[1][0])
            year_month = year + '-' + month
            marriages_by_month[year_month] = row[1][3]

    return marriages_by_month


def birth_data() -> dict[str, int]:
    """Read and add relevant birth data from Vital Events Data by Month to a dictionary mapping
    month and year of births (2018-2020) to its corresponding number of live births, using Pandas.

    Preconditions:
        - The file 'vital_events_data_by_month.csv' is in the same directory as this file.
    """
    births_file = 'vital_events_data_by_month.csv'
    read_file = pd.read_csv(births_file)
    births_by_month = {}

    for row in read_file.iterrows():
        year = str(row[1][1])
        if year in {'2018', '2019', '2020'}:
            month = month_to_number(row[1][0])
            year_month = year + '-' + month
            births_by_month[year_month] = row[1][2]

    return births_by_month


def month_to_number(full_month_name: str) -> str:
    """Convert a full month name to a string representation of the number n where the month is
    the nth month of the year.

    Preconditions:
        - any(month in full_month_name for month in ['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    >>> month_to_number('January/janvier') == '01'
    True
    >>> month_to_number('Month of birth, December') == '12'
    True
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December']

    for i in range(len(months)):
        if months[i] in full_month_name and i + 1 < 10:
            return '0' + str(i + 1)
        elif months[i] in full_month_name and i + 1 >= 10:
            return str(i + 1)

    raise MonthNotFoundError


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     python_ta.check_all(config={
#         'extra-imports': ['pandas', 'python_ta.contracts'],
#         'max-line-length': 100,
#         'disable': ['R1705', 'C0200']
#     })
