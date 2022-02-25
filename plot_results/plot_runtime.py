import csv
import statistics
import numpy as np
import matplotlib.pyplot as plt

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True)
axs = [ax1, ax2, ax3, ax4]
grid = ['50625', '46656', '65536', '59049']
titles = ["1 Gradient Segment", "2 Gradient Segments", "3 Gradient Segments", "4 Gradient Segments"]
#fig.suptitle('Average Performance Over All Samples')
names = ["Differential Evolution", "Genetic Algorithm"]
labels = ["Differential Evolution", "Genetic Algorithm", "Random Search"]
for s in range(4):
    plots = []
    segment = s + 1
    current_ax = axs[s]

    path = '../results/' + str(segment) + 'segments/'
    segments = str(segment) + 'segments'
    #result_filenames = ["DiffEvo_" + segments + "_sample", "GenAlgo_" + segments + "_sample"]
    result_filenames = ["DiffEvo_" + segments + "_runtime" + "_sample", "GenAlgo_" + segments + "_runtime" + "_sample"]
    colors = ["lightseagreen", "goldenrod"]


    # Plot line for all algorithms:
    for i, filename in enumerate(result_filenames):
        # NEW GENALGO
        results_dict = {}
        #x =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, ]
        x = range(1, 301)
        y = []
        std_list = []

        for k in range(8):

            with open(path + filename + str(k+1) + ".csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    row = [float(score) for score in row]
                    for j in x:
                        bla = 10*j
                        best_score_so_far = max(row[:j])
                        if bla not in results_dict:
                            results_dict[bla] = [best_score_so_far]
                        else:
                            results_dict[bla].append(best_score_so_far)



        for key in results_dict:
            crf_list = results_dict[key]
            mean = statistics.mean(crf_list)
            std = statistics.stdev(crf_list)
            y.append(mean)
            std_list.append(std/2)


        #plot = plt.errorbar([j*10 for j in x], y, yerr=std_list, color=colors[i], alpha=0.6)
        #plot = plt.plot([j*10 for j in x], y, color=colors[i])

        globals()["plot" + str(i)], = current_ax.plot([j*10 for j in x], y, color=colors[i], label=names[i])

    # NEW RAnDom
    results_dict = {}
    #x =  [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    x = range(10, 3010, 10)
    y = []
    std_list = []

    for k in range(8):

        with open(path + "RandomSearch_" + segments + "_runtime" + "_sample" + str(k+1) + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row = [float(score) for score in row]
                for i in x:
                    best_score_so_far = max(row[:i])
                    if i not in results_dict:
                        results_dict[i] = [best_score_so_far]
                    else:
                        results_dict[i].append(best_score_so_far)



    for key in results_dict:
        crf_list = results_dict[key]
        mean = statistics.mean(crf_list)
        std = statistics.stdev(crf_list)
        y.append(mean)
        std_list.append(std/2)

    #plot = plt.errorbar(x, y, yerr=std_list, color="slateblue", alpha=0.6)
    #plot = plt.plot(x, y, color="pink")
    #plots.append(plot)
    plot3, = current_ax.plot(x, y, color="pink", label="Random Search")

    current_ax.grid(alpha=0.5, linestyle='--')
    current_ax.set_title(titles[s])

fig.legend(handles=[plot0, plot1, plot3], labels=labels, loc="upper center", ncol=5, prop={'size': 10})
fig.text(0.5, 0.04, 'Number of CRF evaluations (beyond 10 initial points)', ha='center')
fig.text(0.04, 0.5, 'Runtime (seconds)', va='center', rotation='vertical')
fig.set_size_inches(12.5, 8.5, forward=True)
plt.savefig("images/fig_runtime.jpg", dpi=300)
plt.ylim([0, 4])
plt.show()
