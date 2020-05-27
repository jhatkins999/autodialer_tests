from scipy.stats import binom
import pandas as pd
import time
import sys


# Probability k > 1 = 1 - binom.cdf(
# Constrained optimization problem
# Pick the greatest n such that p(k > 1) < alpha
# p = P(a|t) = probability an individual answers given the time
# p(a|t) = limit the search space to the time specified, count answers in space / count total in space
# If you want to add more variables you can do so easily but the space will become too small

def valve(p, alpha, max_phones):
    """Valve to determine the number of devices that should be calling numbers"""
    # Uses a brute force approach to generate n
    for i in range(max_phones):
        prob = 1 - binom.cdf(1, i, p)
        if prob > alpha:
            return i - 1
    return max_phones


def csv_to_dict(filepath):
    df = pd.read_csv(filepath, skiprows=1)
    df = df.T
    phone_lookup = df.to_dict()  # Creates a dictionary where the key is the phone numbers
    return phone_lookup


def output_data(filepath):
    period = time.localtime().tm_hour // 4  # Convert the hours to one of six time periods
    df = pd.read_csv('parameters.csv')
    param = df.to_dict()
    prob = param['contact_'+str(period)] / param['total'+str(period)]
    n = valve(prob, param['alpha'], param['max_phones'])
    phone_table = csv_to_dict(filepath)

    return n, list(phone_table.keys())


if __name__ == "__main__":
    output_data(sys.argv[1])
