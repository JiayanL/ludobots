import random


class JOINT():
    def __init__(self, id, type, parent, child, length, width, height, first=False):
        self.id = id
        self.type = type
        self.length = length
        self.width = width
        self.height = height
        self.first = first
        self.parent = parent
        self.child = child

        if type == "spine":
            self.jointName = f"{self.parent}_{self.child}"
            self.parentName = parent
            self.childName = child
        else:
            # because of weird naming scheme I have with legs and links
            self.jointName = f"{self.parent.name}_{self.child.name}"
            self.parentName = parent.name
            self.childName = child.name

        # choose the specific generator
        if type == "spine":
            self.SpineJoint(self.length, self.height, self.first)
        elif type == "left":
            self.LeftJoint()
        elif type == "right":
            self.RightJoint()
        elif type == "left-down":
            self.LeftDownJoint()
        elif type == "right-down":
            self.RightDownJoint()
        else:
            print("none type")
        # Joint Axis
        jointAxisType = random.randint(1, 2)
        if jointAxisType == 0:
            self.jointAxis = "0 0 1"
        if jointAxisType == 1:
            self.jointAxis = "0 1 0"
        if jointAxisType == 2:
            self.jointAxis = "1 0 0"

        # Joint Type
        jointTypes = ["revolute", "floating", "planar"]
        self.jointType = jointTypes[random.randint(0, 2)]
        self.jointType = "revolute"

    def SpineJoint(self, length, height, first):
        # Joint Position
        if first:
            self.x = length / 2
            self.y = 0
            self.z = height / 2 + 3
        else:
            self.x = length
            self.y = 0
            self.z = 0

    def LeftJoint(self):
        self.x = self.parent.Size["length"] / 2
        self.y = self.parent.Size["width"] / 2
        self.z = 0

    def RightJoint(self):
        self.x = self.parent.Size["length"] / 2
        self.y = -self.parent.Size["width"] / 2
        self.z = 0

    def LeftDownJoint(self):
        self.x = 0
        self.y = self.parent.Size.width
        self.z = -self.parent.Size.height/2

    def RightDownJoint(self):
        self.x = 0
        self.y = -self.parent.Size.width
        self.z = -self.parent.Size.height/2

    def SetTempId(self, parentId, childId):
        self.tempParentId = parentId
        self.tempChildId = childId
        self.tempParentName = f"Body{self.tempParentId}"
        self.tempChildName = f"Body{self.tempChildId}"
        self.tempJointName = f"Body{self.tempParentId}_Body{self.tempChildId}"
