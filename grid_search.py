import sys
import time
import numpy as np
from scipy import optimize
from interface import interface
from plot_result_optimization import plot_result


def grid_search(Ns, segments):
    """
    Run the grid search algorithm for a given number of
    grid points in each dimension and gradient profile segments.

    :Ns: Number of gradient points in each dimension.
    :segments: Number of gradient segments in the gradient profile.

    Total number of grid points is (Ns ** (2*segments + 2))

    :return: A list of the form
             [iters, runtime, solution_fitness, solution]
             where iters is the number of iterations, runtime is the total runtime
             for all iterations, solution_fitness is the best crf score found, solution is
             the best solution found.
    """


    rranges = []

    # Add phi bounds
    for i in range(segments + 1):
        rranges.append((0.01, 1.0))
    # Add t_init bounds
    rranges.append((0.01, 10.0))
    for i in range(segments):
        rranges.append((0.01, 20.0))

    rranges = tuple(rranges)


    start_time = time.time()

    resbrute = optimize.brute(interface, rranges, Ns=Ns, full_output=True, finish=None)

    runtime = time.time() - start_time

    iters = len(rranges) ** 5
    result_list = [iters, runtime, -resbrute[1], resbrute[0]]
    print()
    return(result_list)


def main():
    if len(sys.argv) > 3:
        print('You have specified too many arguments.')
        sys.exit()

    if len(sys.argv) < 3:
        print('Please specify the number of grid points in each dimension and the number of segments.')
        sys.exit()

    grid_points_per_dimension = int(sys.argv[1])
    number_of_segments = int(sys.argv[2])

    grid_points_total = grid_points_per_dimension ** (2*number_of_segments + 2)

    result_list = grid_search(grid_points_per_dimension, number_of_segments)

    print("Best CRF score found: ", result_list[2])
    print("Best solution found: ", result_list[3])
    print("Total runtime: ", result_list[1])
    print("Number of grid points (total): ", grid_points_total)
    print("Number of segments in the gradient profile: ", number_of_segments)
    plot_result(result_list)


if __name__ == '__main__':
    main()
