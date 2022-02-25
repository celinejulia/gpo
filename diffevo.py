import sys
import time
from interface import interface
from plot_result_optimization import plot_result
from scipy.optimize import differential_evolution


def diffevo(iters, segments):
    """
    Run the differential evolution algorithm for a given number of
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
    # We need to create the list of bounds for every parameter.
    bounds = []
    # Add phi bounds
    for i in range(segments + 1):
        bounds.append((0.0, 1.0))
    # Add t_init bounds
    bounds.append((0.0, 5.0))
    for i in range(segments):
        bounds.append((0.1, 20.0))

    # Record starting time
    start_time = time.time()

    # Run the differential evolution algorithm
    res, func_vals, runtime_per_iteration = differential_evolution(
                                                interface,
                                                bounds,
                                                maxiter=iters,
                                                polish=False,
                                                init="random",
                                                popsize=10,
                                                recombination = 0.7,
                                                strategy = "best1bin")

    runtime = time.time() - start_time
    func_values = [-1 * score for score in func_vals]
    return_list = [iters, runtime, -res.fun, res.x, func_values, runtime_per_iteration]
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

    result_list = diffevo(number_of_iterations, number_of_segments)

    print("Best CRF score found: ", result_list[2])
    print("Best solution found: ", result_list[3])
    print("Total runtime: ", result_list[1])
    print("Number of iterations: ", number_of_iterations)
    print("Number of segments in the gradient profile: ", number_of_segments)
    plot_result(result_list)


if __name__ == '__main__':
    main()
