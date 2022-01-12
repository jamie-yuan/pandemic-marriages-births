"""CSC110 Fall 2021 Project: Computing on the Data

This Python module contains the functions that calculate the approximate sinusoidal curves for the
relevant marriage and birth data from the Vital Events Data by Month dataset. These equations are
then used to calculate the differences between the actual and expected data as COVID-19 cases
increase.

This file is Copyright (c) 2021 Cosette Li, Amelia Riddell, and Jamie Yuan.
"""
import math
from extract_data import marriage_data, birth_data


def calculate_sinusoid(data: dict[str, int]) -> tuple[float, float, float, float]:
    """Calculate the four constants (amplitude, frequency, horizontal shift, vertical shift) for a
    sinusoidal equation to represent the number of marriages or births from Vital Events Data by
    Month, based on the 2018-2019 values of data.
    """
    data_1819 = {date: data[date] for date in data if '2020' not in date}  # create a new
    # dictionary containing only data from 2018-2019

    most = max(data_1819.values())
    least = min(data_1819.values())
    amplitude = (most - least) / 2

    frequency = (2 * math.pi) / 12  # period is 12 months
    vertical_shift = (amplitude / 2) + least

    horizontal_shift = ''
    month = 1
    while month < 8:  # determine, from the first eight months (since July/August is the peak),
        # the month that has approximately the average number of marriages/births
        current_date = '2018-0' + str(month)
        if data_1819[current_date] < vertical_shift:
            horizontal_shift = current_date
        month += 1
    horizontal_shift = (int(horizontal_shift[5:7]) - 1)  # convert the date into the number of
    # months from January 2018
    if data == marriage_data():
        horizontal_shift += 1
    elif data == birth_data():
        horizontal_shift += 2
    # adjust based on the graph of the curve

    return (amplitude, frequency, horizontal_shift, vertical_shift)


def marriage_difference() -> dict[str, float]:
    """Calculate the difference between the actual and expected number of marriages (based on
    the calculated sinusoidal equation) to determine if the difference increases as COVID cases
    increase.
    """
    marriage_dates = list(marriage_data().keys())
    marriage_nums = list(marriage_data().values())
    a, b, c, d = calculate_sinusoid(marriage_data())
    differences = {}

    for x in range(len(marriage_dates)):
        y = (a * math.sin(b * (x - c)) + d) + 1750
        differences[marriage_dates[x]] = abs(marriage_nums[x] - y)

    return differences


def birth_difference() -> dict[str, float]:
    """Calculate the difference between the actual and expected number of births (based on
    the calculated sinusoidal equation) to determine if the difference increases as COVID cases
    increase.
    """
    birth_dates = list(birth_data().keys())
    birth_nums = list(birth_data().values())
    a, b, c, d = calculate_sinusoid(birth_data())
    differences = {}

    for x in range(len(birth_dates)):
        y = (a * math.sin(b * (x - c)) + d) + 1000
        differences[birth_dates[x]] = abs(birth_nums[x] - y)

    return differences


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
#         'extra-imports': ['math', 'python_ta.contracts'],
#         'max-line-length': 100,
#         'disable': ['R1705', 'C0200']
#     })
