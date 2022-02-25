import sys
import ast
import csv
import random


def generate_sample_uniform(k0_range, S_range, sample_size, filepath):
    """
    Generate a sample by sampling uniformly from given ranges.

    :k0_range: Range of k0.
    :S_range: Range of S.
    :sample_size: Size that the sample should be.
    :filepath: Specifies the filepath the generated sample parameters
               should be written to.
    """

    f = open(filepath, 'a', newline ='\n')

    # Writing the data into the file
    with f:
        writer = csv.writer(f)
        writer.writerow(["k0", "S"])

        for i in range(sample_size):
            k0 = random.uniform(k0_range[0], k0_range[1])
            S = random.uniform(S_range[0], S_range[1])
            writer.writerow([k0, S])
    return


def main():
    if len(sys.argv) > 5:
        print('You have specified too many arguments.')
        sys.exit()

    if len(sys.argv) < 5:
        print('Please specify the following parameters in order:')
        print("- Bounds for k0")
        print("- Bounds for S")
        print("- Sample size")
        print("- Filepath to write sample to")
        sys.exit()

    bounds_k0 = ast.literal_eval(sys.argv[1])
    bounds_s = ast.literal_eval(sys.argv[2])
    sample_size = int(sys.argv[3])
    filepath = sys.argv[4]
    generate_sample_uniform(bounds_k0 , bounds_s, sample_size, filepath)
    #generate_sample_uniform([1000,2000],[5,20], 100, "data/samples_tyteca/sample9.csv")


if __name__ == '__main__':
    main()
