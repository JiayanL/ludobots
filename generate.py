import pyrosim.pyrosim as pyrosim

# use pyrosim to generate a link
# tells pyrosim the name of the file where information about the world should be stored
pyrosim.Start_SDF("boxes.sdf")

# store in a world.sdf
# stores box with parameters
length, width, height = 1, 1, 1
x, y, z = 0, 0, .5

# 5 rows
for k in range(5):
    # 5 columns
    for j in range(5):
        # generate a tower
        for i in range(10):
            pyrosim.Send_Cube(name="Box" + str(i),
                              pos=[x+j, y+k, z], size=[length, width, height])
            # adjust height
            z += height

            # adjust block size
            height *= .9
            width *= .9
            length *= .9
        z = .5
        length, width, height = 1, 1, 1

# closes the file
pyrosim.End()
# read it in and simulate it
