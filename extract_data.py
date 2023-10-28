"""CSC110 Fall 2021 Project: Extracting the Data

This Python module contains the functions that extract the relevant COVID-19, marriage, and birth
data from the COVID19 Data and Vital Events Data by Month datasets using Pandas. The data is
formatted and added to separate dictionaries.

This file is Copyright (c) 2021 Cosette Li, Amelia Riddell, and Jamie Yuan.
"""
import pandas as pd

COVID_REGION = 1
COVID_DATE = 3
COVID_NUM_CONFIRMED_CASES = 5
EVENTS_MONTH = 0
EVENTS_YEAR = 1
EVENTS_NUM_BIRTHS = 2
EVENTS_NUM_MARRIAGES = 3


class MonthNotFoundError(Exception):
    """Exception raised when attempting to number the month in a string that does not contain a
    full month name.
    """

    def __str__(self) -> str:
        """Return a string representation of this error.
        """
        return "No month was found in the string."


def convert_month_to_num(month_name: str) -> int:
    """Convert a string containing a full month name to the positive integer n where the month is
    the nth month of the year.

    Preconditions:
        - any(month in month_name for month in ["January", "February", "March", "April", "May",
        "June", "July", "August", "September", "October", "November", "December"])

    >>> convert_month_to_num("January/janvier") == 1
    True
    >>> convert_month_to_num("August/août") == 8
    True
    """
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]

    for i in range(len(months)):
        if months[i] in month_name:
            return i + 1

    raise MonthNotFoundError


def extract_covid19_data() -> dict[tuple: int]:
    """Read and add relevant data from the COVID19 Data dataset to a dictionary mapping month and
    year of cases (January 2020 - June 2021) to the corresponding number of confirmed cases,
    using Pandas.

    Preconditions:
        - The file "covid19_data.csv" is in the data directory.
    """
    covid_file = "data/covid19_data.csv"
    read_file = pd.read_csv(covid_file)
    cases_by_month = {}

    for row in read_file.iterrows():
        if "2021-07" in row[1][COVID_DATE]:
            break

        if row[1][COVID_REGION] == "Canada":
            date = row[1][COVID_DATE]  # format: YYYY-MM-DD
            date = (int(date[5:7]), int(date[0:4]))  # format: (month, year)
            if date not in cases_by_month:
                cases_by_month[date] = 0
            cases_by_month[date] += row[1][COVID_NUM_CONFIRMED_CASES]  # number of confirmed cases

    return cases_by_month


def extract_marriage_data() -> dict[tuple, int]:
    """Read and add relevant marriage data from the Vital Events Data by Month dataset to a
    dictionary mapping month and year of marriages (January 2010 - June 2021) to the corresponding
    number of marriages, using Pandas.

    Preconditions:
        - The file "vital_events_data_by_month.csv" is in the data directory.
    """
    marriages_file = "data/vital_events_data_by_month.csv"
    read_file = pd.read_csv(marriages_file)
    marriages_by_month = {}
    relevant_years = set(range(2010, 2022))

    for row in read_file.iterrows():
        year = int(row[1][EVENTS_YEAR])
        if year in relevant_years:
            month = convert_month_to_num(row[1][EVENTS_MONTH])
            date = (month, year)
            marriages_by_month[date] = row[1][EVENTS_NUM_MARRIAGES]

    return marriages_by_month


def extract_birth_data() -> dict[tuple, int]:
    """Read and add relevant birth data from the Vital Events Data by Month dataset to a
    dictionary mapping month and year of births (January 2010 - June 2021) to the corresponding
    number of live births, using Pandas.

    Preconditions:
        - The file "vital_events_data_by_month.csv" is in the data directory.
    """
    births_file = "data/vital_events_data_by_month.csv"
    read_file = pd.read_csv(births_file)
    births_by_month = {}
    relevant_years = set(range(2010, 2022))

    for row in read_file.iterrows():
        year = int(row[1][EVENTS_YEAR])
        if year in relevant_years:
            month = convert_month_to_num(row[1][EVENTS_MONTH])
            date = (month, year)
            births_by_month[date] = row[1][EVENTS_NUM_BIRTHS]

    return births_by_month


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
