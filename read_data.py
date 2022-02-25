import csv
import random
import numpy as np


def read_data():
    """
    Return list of k0 and S samples for a given sample. Sample needs to be
    manually specified here, because optimization algorithm packages don't allow
    for extra arguments in the objective function, other than the parameters
    to be optimized.

    """
    k0_list = []
    S_list = []

    #with open('samples/snyder_samples/regular_sample.csv', 'r') as file:
    with open('samples/samples_tyteca/sample3.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            k0_list.append(float(row[0]))
            S_list.append(float(row[1]))

    # Get the first 35 elements from each list. This is the sample.
    k0_list = k0_list[:25]
    S_list = S_list[:25]
    return(k0_list, S_list)
