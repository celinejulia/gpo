from interface import chromosome_to_lists
import read_data as rd
import math
import numpy as np
import retention_model
import plot_chromatogram
import globals

"""Used to plot resulting chromatogram of single optimization run, straight from result_list."""
t_0 = globals.t_0
t_D = globals.t_D
N = globals.N

# Get chromatogram associated with result chromosome and plot them both.
def plot_result(result_list):

    phi_list, t_init, t_list = chromosome_to_lists(result_list[3])

    # Get lnk0 and S data
    k0_list, S_list = rd.read_data()
    #k0_list = [math.exp(lnk0) for lnk0 in lnk0_list]


    tR_list = []
    W_list = []

    for i in range(len(k0_list)):
        k_0 = k0_list[i]
        S = S_list[i]

        tR, W = retention_model.retention_time_multisegment_gradient(k_0, S, t_0, t_D, t_init, phi_list, t_list, N)
        tR_list.append(tR)
        W_list.append(W)

    plot_chromatogram.plot_chromatogram(tR_list, W_list, phi_list, t_list, t_0, t_D, t_init, result_list[2])
