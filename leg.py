import random


class Position():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Size():
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height


class Leg():
    def __init__(self, currentLink, id, side):
        self.parent = currentLink
        self.id = id
        self.name = f"Body{str(id)}"

        # Joint Type
        jointTypes = ["revolute", "floating", "planar"]
        self.jointType = jointTypes[random.randint(0, 2)]
        self.jointType = "revolute"

        # Joint Axis
        jointAxisType = random.randint(0, 2)
        if jointAxisType == 0:
            self.jointAxis = "0 0 1"
        if jointAxisType == 1:
            self.jointAxis = "0 1 0"
        if jointAxisType == 2:
            self.jointAxis = "1 0 0"

        # Sensor and Color
        self.sensorExists = random.randint(0, 1)
        if self.sensorExists == 1:
            self.colorString = "0 1.0 0 1.0"
            self.colorName = "Green"
        if self.sensorExists == 0:
            self.colorString = "0 0 1.0 1.0"
            self.colorName = "Blue"

        # Size and Position based on Side
        if side == "left":
            self.CreateLeft()
        if side == "left-down":
            self.CreateLeftFoot()
        if side == "right":
            self.CreateRight()
        if side == "right-down":
            self.CreateRightFoot()

    def CreateLeft(self):
        # Size
        self.Size = Size(random.uniform(0, self.parent.Size["length"]),
                         random.uniform(0, self.parent.Size["width"]),
                         random.uniform(0, self.parent.Size["height"]))

        # Position
        self.jointPos = Position(self.parent.Size["length"] / 2,
                                 self.parent.Size["width"] / 2,
                                 0)

        self.linkPos = Position(0, self.Size.width / 2, 0)

    def CreateLeftFoot(self):
        self.Size = Size(
            random.uniform(0, self.parent.Size.length),
            random.uniform(0, self.parent.Size.width),
            random.uniform(0, 2 * self.parent.Size.height)
        )

        self.jointPos = Position(
            0, self.parent.Size.width, -self.parent.Size.height/2)
        self.linkPos = Position(0, 0, -self.Size.height / 2)

    def CreateRight(self):
        self.Size = Size(random.uniform(0, self.parent.Size["length"]),
                         random.uniform(0, self.parent.Size["width"]),
                         random.uniform(0, self.parent.Size["height"]))
        self.linkPos = Position(0, -self.Size.width / 2, 0)

        self.jointPos = Position(self.parent.Size["length"] / 2,
                                 -self.parent.Size["width"] / 2,
                                 0)

    def CreateRightFoot(self):
        self.Size = Size(
            random.uniform(0, self.parent.Size.length),
            random.uniform(0, self.parent.Size.width),
            random.uniform(0, 2 * self.parent.Size.height)
        )

        self.jointPos = Position(
            0, -self.parent.Size.width, -self.parent.Size.height/2)
        self.linkPos = Position(0, 0, -self.Size.height / 2)
