import pyrosim.pyrosim as pyrosim
import random


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
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])

    # Front Leg
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso",
                       child="FrontLeg", type="revolute", position=[.5, 0, 1])

    # create FrontLeg
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[1, 1, 1])

    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso",
                       child="BackLeg", type="revolute", position=[-.5, 0, 1])
    # create BackLeg
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])

    # create joints
    pyrosim.End()


def Generate_Body():
    Create_Link_Joint_Robot()
    # Create_Robot()


def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for sensor in range(3):
        for motor in range(3, 5):
            pyrosim.Send_Synapse(sourceNeuronName=sensor,
                                 targetNeuronName=motor, weight=random.randrange(-1, 1))


Create_World()
Generate_Body()
Generate_Brain()
