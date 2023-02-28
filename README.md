# Ludobots - Assignment 8
Citation: This project was built on top of information from r/ludobots (https://www.reddit.com/r/ludobots/comments/l86j8r/start_here/) and pyrosim (https://github.com/jbongard/pyrosim).

**Video:**
**Plots:** https://docs.google.com/document/d/1a9HIz8jEoTmE7Z87z2EdnzLbEKmcnTYJZ8AMKB75wyM/edit

# Button
Run search.py or button.py to run the evolutions and see the evolved robot. 

Example: 

```python3 search.py```

```python3 button.py ```
**Seeding the Robot**
The robot can be seeded to reproduce random results. To do so, run ```python3 search.py seed.``` The seed argument is optional and will be set to a default seed if not included.

# Robot Structure
This ludobot project expands the morphospace of the 1D creature from assignment 6, allowing it to branch in 3D. Search.py can generate creatures in 1D, 2D, and 3D. Bodies are contiguous, fills in 3D space, and obeys the law of physics.

This is a general diagram of the structure of any robot. Each robot is contained of an initial backbone based on the structure of the snake from assignment 6. Each component of the backbone can then be extended into 1D, 2D, or 3D based on the number of appendages attached to each component of the backbone.
 ![Ass 7](https://user-images.githubusercontent.com/76187440/220261061-c3e776f3-330c-4159-8611-5fb4f549eaf0.jpeg)

### Seeding the robot
### Body Generation
The backbone of my robot is built with the following code. The accompanying diagram explains its logic. Essentially, the LINK class encapsulates the position and size logic for each part of the backbone. 

**Backbone Construction**
![Ass 7](https://user-images.githubusercontent.com/76187440/220262770-e7443a34-a22a-4ad9-a4bb-d77304863f9e.jpeg)
The x, y, and z positions for each piece of the backbone is randomly generated, and the accompanying joint for the next part of the backbone is placed at the edge of the backbone (x/2, 0, z/2).

**Link Class**

This class abstracts a lot of the logic for positioning and arranging each part of the backbone. It stores the parent and child for each block, the size, the position, the joint axis (which can be "0 0 1", "0 1 0", "1 0 0"), the joint type, whether or not each backbone is attached to a limb, and whether or not each part of the backbone has sensors.

**Backbone to Appendage - 1D to 2D**

Each part of the backbone can be attached to an appendage, called a leg to turn it into 3D. Each leg can be attached by any kind of joint (floating, planar, continous, revolute, prismatic, etc.) and be attached to any joint axis. The legs can be attached to the face and is positioned on the side of each block. The logic for leg is encapsulated in the LEG class. The diagram explaining this logic is below.
![Ass 7](https://user-images.githubusercontent.com/76187440/220264584-ade566db-af92-49dc-aa8f-d08d66ccda1e.jpeg)

**Appendage to Foot (3D to 2D)**
Each leg can be extended into 3D by attaching a foot to each appendage. In the Link class, it is determined how many appendages each side of the backbone cube should have. The calculations and diagram is demonstrated as follows. Similar to the appendage, each foot can be attached by any kind of joint (revolute, continuous, planar, prismatic, etc.) and by any joint axis to enable good movement.
![Ass 7](https://user-images.githubusercontent.com/76187440/220265724-45d048db-04a3-4e5c-86c1-621979cad332.jpeg)


#### Joints
Joints are built pretty logically and the logic for each joint is established in specific classes - Link and Leg. The logic for each link is that it takes the full length/width/height along the axis that I want to move it and either move it all the way to the end or halfway.

## Synapses
The code for synapses and brain generation is as follows. Synapses and the brain is generated bottom-up. At each link and leg level, there's a 50% chance whether or not a synapse will be placed at that location. Sensors are placed on those points and connected to motor neurons - which every link in the robot contains.

### Brain Generation
Following is a diagram of how sensors and motors are generated.
![Ass 7](https://user-images.githubusercontent.com/76187440/220268122-99ad40de-f6a0-4e4e-a191-f9f08a161395.jpeg)

Here is a logic connecting sensors (active and inactive to motors)
![Ass 7](https://user-images.githubusercontent.com/76187440/220268887-d5888829-719b-4883-9471-3586055f9667.jpeg)

### Sensor and Motors
Every kind of brain is possible. Sensors are fully connected with motors with the potential for hidden layers. Every sensor can affect every motor.

### Morphospace and Movements
This project can generate 1D, 2D, and 3D structures that can move in all dimensions due to the variability of joint types and joint axes. 

# Evolution
