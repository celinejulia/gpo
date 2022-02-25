import sys
import math
import time
import random
import globals
import interface
import numpy as np
from plot_result_optimization import plot_result


t_0 = globals.t_0
t_D = globals.t_D
N = globals.N


def run_rs(iters, segments):
    """
    Run the random_search algorithm for a given number of
    iterations and gradient profile segments.

    :iters: Number of iterations the algorithm should perform.
    :segments: Number of gradient segments in the gradient profile.
    :return: A list of the form
             [iters, runtime, solution_fitness, solution, crf_per_iteration, runtime_per_iteration]
             where iters is the number of iterations, runtime is the total runtime
             for all iterations, solution_fitness is the best crf score found, solution is
             the best solution found, crf_per_iteration is the best crf score found
             so far after every generation and runtime_per_iteration is the
             cumulative runtime after each generation.

    """
    bounds = []

    # Add phi bounds
    for i in range(segments + 1):
        bounds.append([0.0, 1.0])
    # Add t_init bounds
    bounds.append([0.0, 5.0])
    for i in range(segments):
        bounds.append([0.1, 20.0])


    best_performance = math.inf

    runtime_per_iteration = []
    # Record starting time
    start_time = time.time()
    best_score_per_iteration_list = []
    best_solution_per_iteration_list = []
    for i in range(iters + 10):


        # Get random chromosome
        chromosome = []
        for gene_range in bounds:
            lower_bound = gene_range[0]
            upper_bound = gene_range[1]
            chromosome.append(random.uniform(lower_bound, upper_bound))

        chromosome = np.array(chromosome)

        # Run the objective function for that set of parameters
        current_performance = interface.interface(chromosome)
        # If the performance is better than the best performance so far, (minimize)
        if(current_performance < best_performance):
            # Keep the parameters and performance
            best_performance = current_performance
            best_parameters = chromosome
        best_score_per_iteration_list.append(-best_performance)
        best_solution_per_iteration_list.append(best_parameters)
        runtime = time.time() - start_time
        runtime_per_iteration.append(runtime)

    return_list = [iters, runtime, -best_performance, best_parameters, best_score_per_iteration_list, runtime_per_iteration]
    return(return_list)


def main():
    if len(sys.argv) > 3:
        print('You have specified too many arguments.')
        sys.exit()

    if len(sys.argv) < 3:
        print('Please specify the number of iterations and the number of segments.')
        sys.exit()

    number_of_iterations = int(sys.argv[1])
    number_of_segments = int(sys.argv[2])

    result_list = run_rs(number_of_iterations, number_of_segments)

    print("Best CRF score found: ", result_list[2])
    print("Best solution found: ", result_list[3])
    print("Total runtime: ", result_list[1])
    print("Number of iterations: ", number_of_iterations)
    print("Number of segments in the gradient profile: ", number_of_segments)
    plot_result(result_list)


if __name__ == '__main__':
    main()
