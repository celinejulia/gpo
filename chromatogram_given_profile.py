import crf
import sys
import ast
import math
import globals
import peak_width
import numpy as np
import retention_model
import read_data as rd
import plot_chromatogram
import chromatographic_response_funcions as of


t_0 = globals.t_0
t_D = globals.t_D
t_init = globals.t_init
N = globals.N


def plot_chromatogram_given_gradient_profile(phi_list, t_list):
    """
    Plot chromatogram for a specified gradient profile.
    Please specify the sample in read_data.py

    :phi_list: List of phi values; one for each turning point in the gradient profile.
    :t_list: List of t values; one for each turning point in the gradient profile.
    """

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


    score = crf.crf(tR_list, W_list, phi_list)
    plot_chromatogram.plot_chromatogram(tR_list, W_list, phi_list, t_list, t_D, t_0, t_init, score)


def main():
    if len(sys.argv) > 3:
        print('You have specified too many arguments.')
        sys.exit()

    if len(sys.argv) < 3:
        print('Please specify the following parameters in order:')
        print("- List of phi values; 1 for each turning point. Ex.: '[0.10, 0.10, 0.11, 0.275, 0.295, 0.30]'")
        print("- List of t values; 1 for each turning point. Ex.: '[0, 11.7, 23.5, 36, 48, 60]'")
        sys.exit()

    phi_list = ast.literal_eval(sys.argv[1])
    t_list = ast.literal_eval(sys.argv[2])

    plot_chromatogram_given_gradient_profile(phi_list, t_list)

if __name__ == '__main__':
    main()
