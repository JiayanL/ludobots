# ludobots - Assignment 6

# Button
Run search.py to run the evolutions and see the evolved robot. 

Or you can run button.py

Example: 

```python3 search.py```

```python3 button.py ```

# Documentation
## Robot Structure
This ludobot project expands the morphospace of the 1D creature from assignment 6, allowing it to branch in 3D. Search.py can generate creatures in 1D, 2D, and 3D. Bodies are contiguous, fills in 3D space, and obeys the law of physics.

This is a general diagram of the structure of any robot. Each robot is contained of an initial backbone based on the structure of the snake from assignment 6. Each component of the backbone can then be extended into 1D, 2D, or 3D based on the number of appendages attached to each component of the backbone.
 ![Ass 7](https://user-images.githubusercontent.com/76187440/220261061-c3e776f3-330c-4159-8611-5fb4f549eaf0.jpeg)

### Body Generation
The backbone of my robot is built with the following code. The accompanying diagram explains its logic. Essentially, the LINK class encapsulates the position and size logic for each part of the backbone. 

**Backbone Construction**
![Ass 7](https://user-images.githubusercontent.com/76187440/220262770-e7443a34-a22a-4ad9-a4bb-d77304863f9e.jpeg)
The x, y, and z positions for each piece of the backbone is randomly generated, and the accompanying joint for the next part of the backbone is placed at the edge of the backbone (x/2, 0, z/2).

**Code**
```python3
cLink = LINK(link)
self.idToLink[cLink.id] = cLink

# ----------------------------------- Body ----------------------------------- #
# Link
pyrosim.Send_Cube(name=cLink.parent,
                  pos=[cLink.Pos["x"], cLink.Pos["y"], cLink.Pos["z"]],
                  size=[cLink.Size["length"],
                        cLink.Size["width"], cLink.Size["height"]],
                  colorString=cLink.colorString,
                  colorName=cLink.colorName)

# First joint (Absolute)
if cLink.id == 0 and self.linkCount > 1:
    pyrosim.Send_Joint(name=f"{cLink.parent}_{cLink.child}",
                       parent=cLink.parent,
                       child=cLink.child,
                       type=cLink.jointType,
                       position=[cLink.Size["length"] / 2,
                                 0, cLink.Size["height"] / 2 + 2],
                       jointAxis=cLink.jointAxis)

# All other joints (Relative)
elif cLink.id < self.linkCount - 1:
    pyrosim.Send_Joint(name=f"{cLink.parent}_{cLink.child}",
                       parent=cLink.parent, child=cLink.child,
                       type=cLink.jointType,
                       position=[cLink.Size["length"], 0, 0],
                       jointAxis=cLink.jointAxis)
```


**Link Class**
```python3
class LINK():
    def __init__(self, id):
        self.id = id
        # Link Info

        self.Size = {
            "length": random.uniform(.1, 1),
            "width": random.uniform(.1, 1),
            "height": random.uniform(.1, 1),
        }

        self.Pos = {
            "y": 0,
            "z": 0 if id > 0 else self.Size["height"] / 2 + 2,
            "x": 0 if id == 0 else self.Size["length"] / 2,
        }

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
            pass
            # self.legs = self.Create_Legs(dimension)

        # Sensor and Color
        self.sensorExists = random.randint(0, 1)
        if self.sensorExists == 1:
            self.colorString = "0 1.0 0 1.0"
            self.colorName = "Green"
        if self.sensorExists == 0:
            self.colorString = "0 0 1.0 1.0"
            self.colorName = "Blue"

        # Appendages
        self.legExists = random.choice([True, False])
        self.leftLimbs = random.randint(0, 2)
        self.rightLimbs = random.randint(0, 2)

```
#### Links
**Link to Link**
**Link to Appendage**
**Appendage to Foot**

#### Joints
Diagram

## Synapses

### Brain Generation
Diagram

### Sensor and Motors
What kind of brains are possible
Can a sensor on one side of the body affect a motor on the other side?

## Morphospace and Movements
This project can generate 1D, 2D, and 3D structures that can move in all dimensions due to the variability of joint types and joint axes. 

# Archive
Assignment 7:

## Robot Structure
<img width="637" alt="Screen Shot 2023-02-15 at 8 55 17 PM" src="https://user-images.githubusercontent.com/76187440/219256373-220d5a48-6f33-4c95-a6c1-6261e75091a6.png">

## Links and Joints
Links and Joints are generated by the following code. ```self.link_count``` is generated in the constructor and is a random number between 1 and 15. The length, width, and height are randomly generated at each step. The first link is positioned at (0, 0, height/2) with the length, width, and height. Each subsequent link is positioned length/2 away on the x-axis and positioned along the middle of the first link's height. Joints are positioned length away from the previous link with the first link absolutely positioned at the edge of the first link.

```python3
 for link in range(0, self.link_count):
            length = random.uniform(.1, 1)
            width = random.uniform(.1, .5)
            height = random.uniform(.1, .5)

            if link == 0:
                z = height / 2

            elif link > 0:
                x = length / 2
                z = 0

            parent = "Body" + str(link)
            child = "Body" + str(link+1)

            if self.sensor_list[link] == 1:
                colorString = "0 1.0 0 1.0"
                colorName = "Green"
            else:
                colorString = "0 0 1.0 1.0"
                colorName = "Blue"

            pyrosim.Send_Cube(name=parent, pos=[x, y, z], size=[
                              length, width, height], colorString=colorString, colorName=colorName)

            if link == 0:
                # absolute position
                print("absolute")
                pyrosim.Send_Joint(name=parent+"_"+child, parent=parent, child=child,
                                   type="revolute", position=[length / 2, 0, height / 2], jointAxis="0 0 1")
            elif link < self.link_count - 1:
                # relative position
                print("relative")
                pyrosim.Send_Joint(name=parent+"_"+child, parent=parent, child=child,
                                   type="revolute", position=[length, 0, 0], jointAxis="0 0 1")
```

## Synapses
Synapses are generated by the following code. Based on a randomly generated array of 0s and 1s the same length as self.link_count, we install random links. We then add a motor to every joint and connect every sensor to each motor.
```python3
pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensor_count = 0
        for link in range(0, self.link_count):
            if self.sensor_list[link] == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensor_count, linkName="Body" + str(link))
                sensor_count += 1

        motor_count = 0
        for link in range(0, self.link_count):
            if link < self.link_count - 1:
                pyrosim.Send_Motor_Neuron(
                    name=sensor_count + motor_count, jointName="Body" + str(link) + "_Body" + str(link+1))
                motor_count += 1

        print(sensor_count)
        print(motor_count)

        # connect sensors to motors
        for sensor in range(0, sensor_count):
            for motor in range(0, motor_count):
                pyrosim.Send_Synapse(
                    sourceNeuronName=sensor, targetNeuronName=motor + sensor_count, weight=random.uniform(-1, 1))
```

Assignment 6:

Created a random number of links with random sizes

Added an array storing my sensor bodies in the constructor

Created a brain that connected selected sensors with all motors

Assigment 5:

I did three things in the assignment.

First, I implemented braniac and connected 4 hidden layers between my sensor neurons (feet and torso) and motor neurons. I created two sets of matrices that I updated everytime in self.mutate().

Second, I built a bipedal robot on top of a raised platform.

Third, I implemented a fitness function that would help the robot learn how to walk forward and balance. My fitness function was torsoX + 3 * torsoZ which is a weighted sum of the distance traveled as well as how upright the torso is - giving extra emphasis to keeping the torso upright so that the robot does not fall over in an attempt to maximize distance travel. I also implemented a penalty that reduced the fitness of each robot by 3 everytime it fell over (torsoZ < 1)
