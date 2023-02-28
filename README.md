## Ludobots - Assignment 8
Citation: This project was built on top of information from r/ludobots (https://www.reddit.com/r/ludobots/comments/l86j8r/start_here/) and pyrosim (https://github.com/jbongard/pyrosim). The aim of this assignment is to expand on the structure from Assignment 7 to create a parallel hill climbing robot that can evolve morphology and brain for locomotion.

**Video:** https://www.youtube.com/watch?v=SbsmmTvQ7VM

**Plots:** https://docs.google.com/document/d/1a9HIz8jEoTmE7Z87z2EdnzLbEKmcnTYJZ8AMKB75wyM/edit

## Button

**Seeding the Robot:** The robot can be seeded to reproduce random results. To do so, run ```python3 search.py seed.``` The seed argument is optional and will be set to a default seed if not included.

**Running the Program:** Run search.py or button.py to run the evolutions and see the evolved robot. 

Example: ```python3 search.py``` or ```python3 button.py ```


## Robot Structure

**Solution Class**
The logic of each creature is generated in the solution constructor. The constructor initializes the number of links in the creature, which links have sensors, and which links are connected to which links, and stores this information for future mutation. The constructor leverages the LINK and Leg classes to calculate the joint position, size, and link position of each link, along with additional helpful information for mutation. Each section below dives into implementation on a deeper level.

**Links**
Spine.
Spine to Leg
Leg to foot.

**Joints**

**Link Evolution**

**Synapses**
The code for synapses and brain generation is as follows. Synapses and the brain is generated bottom-up. At each link and leg level, there's a 50% chance whether or not a synapse will be placed at that location. Sensors are placed on those points and connected to motor neurons - which every link in the robot contains.

**Brain Evolution**
                                                                                                                                        
**Sensor and Motors**
Every kind of brain is possible. Sensors are fully connected with motors with the potential for hidden layers. Every sensor can affect every motor.

**Morphospace and Movements**
This project can generate 1D, 2D, and 3D structures that can move in all dimensions due to the variability of joint types and joint axes. 
