import sys
import pickle

# unpickle
seed = int(sys.argv[1])
generation = int(sys.argv[2])

fileName = f"lineages/seed{seed}_gen{generation}.pickle"
with open(fileName, 'rb') as f:
    parent = pickle.load(f)

parent.Start_Simulation("GUI")
