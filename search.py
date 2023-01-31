import os
from hillclimber import HILL_ClIMBER
from parallelHillClimber import PARALLEL_HILL_ClIMBER

# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

# os.system("python3 simulate.py")
# hc = HILL_ClIMBER()
# hc.Evolve()
# hc.Show_Best()

phc = PARALLEL_HILL_ClIMBER()
phc.Evolve()
phc.Show_Best()
exit()
