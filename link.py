import random
from leg import LEG


class LINK():
    def __init__(self, id, dimension):
        self.id = id
        # Link Info

        self.Size = {
            "length": random.uniform(.1, 1),
            "width": random.uniform(.1, 1),
            "height": random.uniform(.1, 1),
        }

        self.Pos = {
            "y": 0,
            "z": 0 if id > 0 else self.Size["height"] / 2,
            "x": 0 if id == 0 else self.Size["length"] / 2,
        }
        # # Generate Size
        # self.length = random.uniform(.1, 1)
        # self.width = random.uniform(.1, 1)
        # self.height = random.uniform(.1, 1)

        # # Generate Position
        # self.y = 0
        # if id == 0:
        #     self.z = self.height / 2
        #     self.x = 0

        # elif id > 0:
        #     self.x = self.length / 2
        #     self.z = 0

        # Generate Names for Joints
        self.parent = f"Body{str(id)}"
        self.child = f"Body{str(id+1)}"

        # Joint Axis
        jointAxisType = random.randint(0, 2)
        if jointAxisType == 0:
            self.jointAxis = "0 0 1"
        if jointAxisType == 1:
            self.jointAxis = "0 1 0"
        if jointAxisType == 2:
            self.jointAxis = "1 0 0"

        # Joint Type
        jointTypes = ["revolute", "floating",
                      "continuous", "planar"]
        self.jointType = jointTypes[random.randint(0, 3)]
        self.jointType = "revolute"

        # Create children
        self.legs = []
        self.legExists = random.randint(0, 1)
        if self.legExists == 1:
            self.legs = self.Create_Legs(dimension)

    def Create_Legs(self, dimension):
        legs = []

        if dimension == 2:
            left_leg = LEG(dimension)
            right_leg = LEG(dimension)

            # 1 block
            # legs.append()
            # legs.append()

        if dimension == 3:
            left_leg = LEG(dimension)
            right_leg = LEG(dimension)

            # 2 block legs
            # legs.append()
            # legs.append()

        return legs
