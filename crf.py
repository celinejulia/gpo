import math
import numpy as np


def resolution(tR1, tR2, W1, W2):
    """Return the resolution of 2 peaks, given tR and W for both peaks."""
    resolution = ((2*abs(tR2-tR1))/(W1+W2))
    return(resolution)


def sigmoid(x, a, b):
    """Return a sigmoidal transformation of x."""
    sigmoid = 1/(1 + np.exp(-a*x + b))
    return(sigmoid)


def sort_peaks(retention_times, peak_widths):
    """
    Sort peaks based on retention time
    and return sorted retention time list and peak width list.
    """
    number_of_peaks = len(retention_times)

    # Create a list of tuples, one for each peak (rt, W)
    peak_tuple_list = []
    for i in range(number_of_peaks):
        peak_tuple = (retention_times[i], peak_widths[i])
        peak_tuple_list.append(peak_tuple)
    # Sort according to first element
    peak_tuples_sorted = sorted(peak_tuple_list, key=lambda x: x[0])

    retention_times = []
    peak_widths = []
    for i in range(number_of_peaks):
        retention_times.append(peak_tuples_sorted[i][0])
        peak_widths.append(peak_tuples_sorted[i][1])

    return(retention_times, peak_widths)


def crf(retention_times, peak_widths, phi_list):
    """
    Return CRF score for a chromatogram characterized by a list of retention
    times and a corresponding list of peak widths.
    """

    N = len(retention_times)

    # Parameters sigmoidal transformations
    b0 = 3.93
    b1 = 3.66
    b2 = -0.0406
    b3 = -4.646

    resolutions = []
    sigmoid_resolutions = []

    # Sort retention times and peak widths
    retention_times, peak_widths = sort_peaks(retention_times, peak_widths)

    prod_S = 1

    # Loop over all neighboring peak pairs and get S. Multiply together.
    for i in range(N - 1):
        tR1 = retention_times[i]
        tR2 = retention_times[i+1]
        W1 = peak_widths[i]
        W2 = peak_widths[i+1]

        R = resolution(tR1, tR2, W1, W2)
        S = sigmoid(R, b0, b1)
        prod_S = prod_S * S

        sigmoid_resolutions.append(S)
        resolutions.append(R)

    # Create f and g
    f = prod_S ** (1/(N-1))

    # Get T
    tR_last = retention_times[-1]
    W_last = peak_widths[-1]
    T = tR_last + 0.5*(W_last)

    g = sigmoid(T, b2, b3)

    score = f * g

    # Optional penalty for gradient segments with negative slope
    # Comment out to remove penalty:
    if(sorted(phi_list) != phi_list):
        return(0.8 * score)

    return(score)
