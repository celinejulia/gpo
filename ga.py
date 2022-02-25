import sys
import time
import pygad
from interface import interface_pygad
from plot_result_optimization import plot_result


def ga(iters, segments):
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

    num_parents_mating = 4
    sol_per_pop = 10
    parent_selection_type = "sss"
    mutation_type = "random"
    mutation_probability = 0.4

    bounds = []
    # Add phi bounds
    for i in range(segments + 1):
        bounds.append({'low': 0.0, 'high': 1.0})
    # Add t_init bounds
    bounds.append({'low': 0.0, 'high': 5.0})
    for i in range(segments):
        bounds.append({'low': 0.1, 'high': 20.0})

    num_genes = len(bounds)

    ga_instance = pygad.GA(num_generations=iters,
                           num_parents_mating=num_parents_mating,
                           fitness_func=interface_pygad,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           parent_selection_type=parent_selection_type,
                           mutation_type=mutation_type,
                           mutation_probability=mutation_probability,
                           gene_space=bounds,
                           keep_parents=2)

    # Record starting time
    start_time = time.time()

    # Run the differential evolution algorithm
    ga_instance.run()

    runtime = time.time() - start_time

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    runtime_per_iteration = ga_instance.runtimes
    return_list = [iters, runtime, solution_fitness, solution, ga_instance.best_solutions_fitness, runtime_per_iteration]
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

    result_list = ga(number_of_iterations, number_of_segments)

    print("Best CRF score found: ", result_list[2])
    print("Best solution found: ", result_list[3])
    print("Total runtime: ", result_list[1])
    print("Number of iterations: ", number_of_iterations)
    print("Number of segments in the gradient profile: ", number_of_segments)
    plot_result(result_list)


if __name__ == '__main__':
    main()
