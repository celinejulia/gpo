import csv
import sys
import diffevo
import bayesopt
import ga
import random_search
import grid_search
from tqdm import tqdm


def run_n_times(algorithm, segments, n, iters):
    """
    Perform a meta-experiment. The chosen algorithm is run n times for a given
    number of gradient segments. The CRF score per iteration and the cumulative
    runtime per iteration are written to csv files. Filepaths need to be specified
    manually and should indicate which sample was used in read_data.py. This has
    to be done manually because optimization algorithm packages don't allow
    for extra arguments in the objective function, other than the parameters
    to be optimized.

    :algorithm: Optimization algorithm. Choose from:
                BayesOpt/DiffEvo/GenAlgo/GridSearch/RandomSearch
    :segments: Number of gradient segments in the gradient profile.
    """

    filename = algorithm + "_" + str(segments) + "segments_sample1.csv"
    filename_runtime = algorithm + "_" + str(segments) + "segments" + "_runtime_sample1" + ".csv"
    filepath = "results/" + str(segments) + "segments/" + filename
    filepath_runtime = "results/" + str(segments) + "segments/" + filename_runtime


    if(algorithm == "BayesOpt"):

        for nth_experiment in tqdm(range(n)):
            # n = number of meta experiments
            return_list = bayesopt.bayesopt(iters, segments)
            func_vals = return_list[4]
            runtime_per_iteration = return_list[5]
            # write the data from the list to a (csv?) file as a single line
            f = open(filepath, 'a', newline ='\n')

            # writing the data into the file
            with f:
                writer = csv.writer(f)
                writer.writerow(func_vals)

            f = open(filepath_runtime, 'a', newline ='\n')

            # writing the data into the file
            with f:
                writer = csv.writer(f)
                writer.writerow(runtime_per_iteration)

    elif(algorithm == "DiffEvo"):

        for nth_experiment in tqdm(range(n)):
            # n = number of meta experiments
            return_list = diffevo.diffevo(iters, segments)

            func_vals = return_list[4]
            runtime_per_iteration = return_list[5]
            f = open(filepath, 'a', newline ='\n')

            with f:
                writer = csv.writer(f)
                writer.writerow(func_vals)

            f = open(filepath_runtime, 'a', newline ='\n')

            with f:
                writer = csv.writer(f)
                writer.writerow(runtime_per_iteration)


    elif(algorithm == "GenAlgo"):

        for nth_experiment in tqdm(range(n)):
            return_list = ga.ga(iters, segments)
            func_vals = return_list[4]
            runtime_per_iteration = return_list[5]
            f = open(filepath, 'a', newline ='\n')

            with f:
                writer = csv.writer(f)
                writer.writerow(func_vals)

            f = open(filepath_runtime, 'a', newline ='\n')

            with f:
                writer = csv.writer(f)
                writer.writerow(runtime_per_iteration)



    elif(algorithm == "RandomSearch"):

        for nth_experiment in tqdm(range(n)):
            # n = number of meta experiments
            return_list = random_search.run_rs(iters, segments)
            func_vals = return_list[4]
            runtime_per_iteration = return_list[5]
            f = open(filepath, 'a', newline ='\n')

            with f:
                writer = csv.writer(f)
                writer.writerow(func_vals)

            f = open(filepath_runtime, 'a', newline ='\n')

            with f:
                writer = csv.writer(f)
                writer.writerow(runtime_per_iteration)

    elif(algorithm == "GridSearch"):

        return_list = grid_search.grid_search(iters, segments)
        func_val = return_list[2]
        runtime = return_list[1]
        f = open(filepath, 'a', newline ='\n')

        with f:
            writer = csv.writer(f)
            writer.writerow([func_val])

        f = open(filepath_runtime, 'a', newline ='\n')

        with f:
            writer = csv.writer(f)
            writer.writerow([runtime])


def main():
    if len(sys.argv) > 5:
        print('You have specified too many arguments.')
        sys.exit()

    if len(sys.argv) < 5:
        print('Please specify the following parameters in order:')
        print("- Choose an optimization algorithm (BayesOpt/DiffEvo/GenAlgo/GridSearch/RandomSearch)")
        print("- Number of segments in the gradient profile")
        print("- Number of sub-experiments the meta-experiment should consist of")
        print("- Number of iterations. Note that if the chosen algorithm is grid search, this is the number of grid points per dimension.")
        sys.exit()

    algorithm = sys.argv[1]
    number_of_segments = int(sys.argv[2])
    sub_experiments = int(sys.argv[3])
    iterations = int(sys.argv[4])

    run_n_times(algorithm, number_of_segments, number_of_segments, iterations)


if __name__ == '__main__':
    main()
