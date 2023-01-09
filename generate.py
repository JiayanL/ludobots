import pyrosim.pyrosim as pyrosim

# use pyrosim to generate a link
# tells pyrosim the name of the file where information about the world should be stored
pyrosim.Start_SDF("box.sdf")

# store in a world.sdf
# stores box with parameters
pyrosim.Send_Cube(name="box", pos=[0, 0, 0.5], size=[1, 1, 1])
# closes the file
pyrosim.End()
# read it in and simulate it
