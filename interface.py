from crf import crf
import retention_model
import read_data as rd
import math
import numpy as np
import chromatographic_response_funcions as of
import globals


# HPLC system parameters
t_0 = globals.t_0
t_D = globals.t_D
N = globals.N


def chromosome_to_lists(chromosome):
    """
    Transform a candidate solution vector into separate lists for
    phi values, t_init and delta_t values respectively.
    """
    l = len(chromosome)
    segments = int((l - 2)/2)

    phi_list = []
    for i in range(segments + 1):
        phi_list.append(chromosome[i])

    t_init = chromosome[segments + 1]
    delta_t_list = []

    for i in range(segments + 2, 2*segments + 2):
        delta_t_list.append(chromosome[i])
    t_list = [0]

    for i, delta_t in enumerate(delta_t_list):
        t_list.append(t_list[i] + delta_t)
    return(phi_list, t_init, t_list)


# Input has to be a numpy array
def interface(chromosome):
    """
    This function serves as an interface between the Bayesian optimization,
    differential evolution, random search and grid search packages and the CRF
    function. This is necessary because the gradient profile specified by the
    candidate solution vector has to be transformed into a chromatogram
    (list of retention times and peak widths) for a given sample before the CRF
    score can be calculated. It does this using the following steps:

    1. Read in sample sample sample data using read_data.py
    2. Calculate retention times and peak widths for all sample compounds
       using the chromatographic simulator as implemented in retention_model.py
    3. Calculate and return the CRF score

    :chromosome: Gradient profile vector in the form of a numpy array.
    :return: CRF score for a chromatogram produced by the specified gradient
             profile.

    """

    phi_list, t_init, t_list = chromosome_to_lists(chromosome)

    # Get lnk0 and S data
    k0_list, S_list = rd.read_data()
    #k0_list = [math.exp(lnk0) for lnk0 in lnk0_list]

    tR_list = []
    W_list = []

    # Calculate retention times and peak widths
    for i in range(len(k0_list)):
        k_0 = k0_list[i]
        S = S_list[i]

        tR, W = retention_model.retention_time_multisegment_gradient(k_0, S, t_0, t_D, t_init, phi_list, t_list, N)
        tR_list.append(tR)
        W_list.append(W)

    # Calculate crf
    #score = crf(tR_list, W_list, phi_list) * -1
    score = of.critical_resolution(tR_list, W_list) * -1
    return(score)


# Input has to be a numpy array
def interface_pygad(chromosome, solution_id):
    """
    This function serves as an interface between the genetic algorithm package
    and the CRF function. This is necessary because the gradient profile
    specified by the candidate solution vector has to be transformed into a
    chromatogram (list of retention times and peak widths) for a given sample
    before the CRF score can be calculated. It does this using the following
    steps:

    1. Read in sample sample sample data using read_data.py
    2. Calculate retention times and peak widths for all sample compounds
       using the chromatographic simulator as implemented in retention_model.py
    3. Calculate and return the CRF score

    :chromosome: Gradient profile vector in the form of a numpy array.
    :return: CRF score for a chromatogram produced by the specified gradient
             profile.

    """

    phi_list, t_init, t_list = chromosome_to_lists(chromosome)

    # Get lnk0 and S data
    k0_list, S_list = rd.read_data()
    #k0_list = [math.exp(lnk0) for lnk0 in lnk0_list]

    tR_list = []
    W_list = []

    # Calculate retention times and peak widths
    for i in range(len(k0_list)):
        k_0 = k0_list[i]
        S = S_list[i]

        tR, W = retention_model.retention_time_multisegment_gradient(k_0, S, t_0, t_D, t_init, phi_list, t_list, N)
        tR_list.append(tR)
        W_list.append(W)

    # Calculate CRF (Change this line to choose a different CRF)
    score = crf(tR_list, W_list, phi_list)
    return(score)
