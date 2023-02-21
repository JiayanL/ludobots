import random


class LEG():
    def __init__(self, currentLink, side, id):
        self.parent = currentLink
        self.id = id

        # Size
        self.Size = {
            "length": random.uniform(0, self.parent.Size["length"]),
            "width": random.uniform(0, self.parent.Size["width"]),
            "height": random.uniform(0, self.parent.Size["height"]),
        }

        # Joint Type
        jointTypes = ["revolute", "floating",
                      "continuous", "planar"]
        self.jointType = jointTypes[random.randint(0, 3)]

        # if side == "left":
        #     self.CreateLeft()
        # if side == "right":
        #     pass

    def CreateLeft(self):
        pass
