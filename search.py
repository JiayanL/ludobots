import os
from hillclimber import HILL_ClIMBER
from parallelHillClimber import PARALLEL_HILL_ClIMBER
import random
import constants as c
import sys
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    random.seed(int(sys.argv[1]))
else:
    random.seed(c.seed)

fitness_curves = defaultdict(list)

for i in range(10):
    random.seed(i)
    phc = PARALLEL_HILL_ClIMBER()
    phc.Evolve()
    # phc.Show_Best()

    with open(f"phc{i}.pickle", "wb") as f:
        pickle.dump(phc, f)

    fitness_curves[f"Random Seed {i}"] = phc.fitnessCurves

phc.Show_Best()

# Plot all 10 runs
fig, ax = plt.subplots()
for key, value in fitness_curves.items():
    ax.plot(value, label=key)

ax.legend()
ax.set_title("Fitness Curves of Ludobots with Different Random Seeds")
ax.set_xlabel("Best Fitness")
ax.set_ylabel("Generation")

plt.show()

# phc.Plot()
