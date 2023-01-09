import pyrosim.pyrosim as pyrosim


def Create_World():
    # use pyrosim to generate a link
    # tells pyrosim the name of the file where information about the world should be stored
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box",
                      pos=[3, 4, .5], size=[1, 1, 1])
    # closes the file
    pyrosim.End()


def Create_Robot():
    # URDF body is used to describe a robot
    pyrosim.Start_URDF("body.urdf")
    # all URDF files must describe robot in a tree structure (root link + joints)
    pyrosim.Send_Cube(name="Link0",
                      pos=[0, 0, .5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0",
                       child="Link1", type="revolute", position=[0, 0, 1])
    pyrosim.Send_Cube(name="Link1", pos=[0, 0, .5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1",
                       child="Link2", type="revolute", position=[0, 0, 1])
    pyrosim.Send_Cube(name="Link2", pos=[0, 0, .5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Link2_Link3", parent="Link2",
                       child="Link3", type="revolute", position=[0, .5, .5])
    pyrosim.Send_Cube(name="Link3", pos=[0, .5, 0], size=[1, 1, 1])
    pyrosim.End()


def Create_Link_Joint_Robot():
    pyrosim.Start_URDF("body.urdf")

    # create Torso (root link)
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso",
                       child="FrontLeg", type="revolute", position=[2.5, 0, 1])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso",
                       child="BackLeg", type="revolute", position=[.5, 0, 1])
    # create BackLeg
    pyrosim.Send_Cube(name="BackLeg", pos=[0, 0, -.5], size=[1, 1, 1])

    # create FrontLeg
    pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0, -.5], size=[1, 1, 1])

    # create joints
    pyrosim.End()


Create_World()
Create_Link_Joint_Robot()
# Create_Robot()
