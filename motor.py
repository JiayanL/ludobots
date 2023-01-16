import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR():
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        # Prepare constants
        self.amplitude = c.amplitude
        self.offset = c.phaseOffset
        if self.jointName == b"Torso_BackLeg":
            self.frequency = c.frequency * 2
        else:
            self.frequency = c.frequency

        # Prepare sensor values
        targetAngles = np.arange(0, np.pi*2, np.pi*2/c.steps)
        self.motorValues = self.amplitude * \
            np.sin(self.frequency * (targetAngles + self.offset))

    def Set_Value(self, robotId, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[t],
            maxForce=50)

    def Save_Values(self):
        np.save("data/" + self.jointName + "MotorValues.npy", self.motorValues)
