import numpy as np
# Description: This file contains all the constants used in the simulation
steps = 1000

# Backleg target angles
amplitude = np.pi/4
frequency = 5
phaseOffset = np.pi/2

# Frontleg target angles
FrontLeg_amplitude = np.pi/3
FrontLeg_frequency = 5
FrontLeg_phaseOffset = 0

# Evolution and Hillclimbing
numberOfGenerations = 0
populationSize = 1

# Parameterization
numSensorNeurons = 3
numMotorNeurons = 7
numHiddenNeurons = 4
motorJointRange = 1

# Snake
maxLinks = 6
minLinks = 1

# Testing
testBody = True
