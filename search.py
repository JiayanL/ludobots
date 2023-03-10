import os
from hillclimber import HILL_ClIMBER
from parallelHillClimber import PARALLEL_HILL_ClIMBER
import random
import constants as c
import sys
# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

# os.system("python3 simulate.py")
# hc = HILL_ClIMBER()
# hc.Evolve()
# hc.Show_Best()

# set seed
if len(sys.argv) > 1:
    random.seed(int(sys.argv[1]))
else:
    random.seed(c.seed)

phc = PARALLEL_HILL_ClIMBER()
phc.Evolve()
phc.Show_Best()
phc.Plot()
