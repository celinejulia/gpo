import csv
import statistics

def hyperparameter_tuning(algo):

    if(algo == "DiffEvo"):

        folders_ga = ["best1bin_02/", "best1bin_07/", "best1exp_02/", "best1exp_07/"]
        path_ga = "../results/diffevo/"
        rest = "DiffEvo_1segments_sample"

    elif(algo = "GenAlgo"):

        folders_ga = ["rws_02/", "rws_04/", "sss_02/", "sss_04/", "tour_02/", "tour_04/"]
        path_ga = "../results/ga/"
        rest = "GenAlgo_1segments_sample"

    table_dict = {}

    for folder in folders_ga:

        sum = 0

        for k in range(9):
            filepath = path_ga + folder + rest + str(k+1) + ".csv"

            with open(filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    row = [float(score) for score in row]
                    last_iteration_score = row[-1]
                    print(k+1, last_iteration_score )
                    sum = sum + last_iteration_score

        average = sum/90

        print("average", k+1, average)

        table_dict[folder] = average

    print(table_dict)
    return

def main():
    if len(sys.argv) > 2:
        print('You have specified too many arguments.')
        sys.exit()

    if len(sys.argv) < 2:
        print('Please specify the name of the algorithm (DiffEvo/GenAlgo).')
        sys.exit()

    algo = sys.argv[1]

    hyperparameter_tuning(algo)


if __name__ == '__main__':
    main()
