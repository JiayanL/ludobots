import os
from hillclimber import HILL_ClIMBER
from parallelHillClimber import PARALLEL_HILL_ClIMBER
import random
import constants as c
import sys
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

type = str(sys.argv[1])

if type == "seed":
    random.seed(int(sys.argv[2]))
    phc = PARALLEL_HILL_ClIMBER(int(sys.argv[2]))
    phc.Evolve()
    phc.Show_Best()
    phc.Plot()

elif type == "engineer":
    fitness_curves = defaultdict(list)

    for i in range(10):
        random.seed(i)
        phc = PARALLEL_HILL_ClIMBER(i)
        phc.Evolve()

        with (open(f"Seed{i}.pickle", "wb")) as f:
            pickle.dump(phc, f)

        fitness_curves[f"Random Seed {i}"] = phc.fitnessCurves

    phc.Show_Best()

    # Plot all 10 runs
    fig, ax = plt.subplots()
    for key, value in fitness_curves.items():
        ax.plot(value, label=key)

    ax.legend()
    ax.set_title("Fitness Curves of Ludobots with Different Random Seeds")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness")

    plt.show()
