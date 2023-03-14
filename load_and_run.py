import os
from parallelHillClimber import PARALLEL_HILL_ClIMBER
import random
import constants as c
import sys
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

# unpickle
seed = int(sys.argv[1])
fileName = f"Saved Seeds/Seed{seed}.pickle"
with open(fileName, 'rb') as f:
    phc = pickle.load(f)

phc.Show_Best()
phc.Plot()
