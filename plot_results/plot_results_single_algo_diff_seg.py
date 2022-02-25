import csv
import statistics
import numpy as np
import matplotlib.pyplot as plt



result_filenames = ["DiffEvo_1segments.csv", "DiffEvo_2segments.csv", "DiffEvo_3segments.csv"]
colors = ["lightseagreen", "goldenrod", "cornflowerblue", "slateblue"]

# Initialize figure
fig = plt.figure()
plots = []

# Plot line for all algorithms:
for i, filename in enumerate(result_filenames):
    results_dict = {}
    x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    y = []
    std_list = []

    with open('../results/' + filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                iters = int(row[0])
                crf = float(row[2])
                if iters not in results_dict:
                    results_dict[iters] = [crf]
                else:
                    results_dict[iters].append(crf)

                line_count += 1

    for key in results_dict:
        crf_list = results_dict[key]
        mean = statistics.mean(crf_list)
        std = statistics.stdev(crf_list)
        y.append(mean)
        std_list.append(std/2)


    color = colors[i]
    plot = plt.errorbar(x, y, yerr=std_list, color=color, alpha=0.6)
    plots.append(plot)
    #plt.plot(x, y, color=color)


plt.grid(alpha=0.5, linestyle='--')
plt.legend(plots, ["1 segment", "2 segments", "3 segments", "4 segments"])
plt.xlim(xmin=0)
plt.title("Differential Evolution")
plt.show()
