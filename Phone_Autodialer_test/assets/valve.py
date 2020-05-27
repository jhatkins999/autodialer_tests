from scipy.stats import binom
import time
import sys
import os
import csv


# Probability k > 1 = 1 - binom.cdf(...)
# Constrained optimization problem
# Pick the greatest n such that p(k > 1) < alpha -- super easy because binom.cdf is monotonically increasing
# p = P(a|t) = probability an individual answers given the time
# p(a|t) = limit the search space to the time specified, count answers in space / count total in space

def valve(p, alpha, max_phones):
    """Valve to determine the number of devices that should be calling numbers"""
    # Uses a brute force approach to generate n
    for i in range(max_phones):
        prob = 1 - binom.cdf(1, i, p)
        if prob > alpha:
            return i - 1
    return max_phones


def csv_to_dict(filepath):
    file = open(filepath)
    reader = csv.reader(file)
    phone_lookup = {}
    for row in reader:
        phone_lookup[row[0]] = row[1:]
    return phone_lookup


def output_data(filepath):
    period = time.localtime().tm_hour // 4  # Convert the hours to one of six time periods
    os.chdir('C:/Users/ja383/PycharmProjects/autodialer/Phone_Autodialer_test/assets')
    file = open('csvfiles/parameters.csv', 'r')
    paramreader = csv.reader(file)
    param = {}
    for row in paramreader:
        param[row[0]] = row[1]

    prob = float(param['contact'+str(period)] )/ float(param['total'+str(period)])
    n = valve(prob, float(param['alpha']), int(param['max_phones']))
    phone_table = csv_to_dict(filepath)

    print(n)
    for num in list(phone_table.keys()):
        print(num)
    sys.stdout.flush()


if __name__ == "__main__":
    output_data(sys.argv[1])
