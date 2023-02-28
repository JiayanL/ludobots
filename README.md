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

The logic of each creature is generated in the solution constructor. The constructor initializes the number of links in the creature, which links have sensors, and which links are connected to which links, and stores this information for future mutation. The constructor leverages the LINK and Leg classes to calculate the joint position, size, and link position of each link, along with additional helpful information for mutation. Each spine can connect to another spine. Each spine has the option of having up to two legs, and each leg can have one foot. Each section below dives into implementation on a deeper level.

<p float="left">
<img src="https://user-images.githubusercontent.com/76187440/221807572-e296921e-c900-41d8-b32c-6372d44b0679.jpeg" width="50%">
<img src="https://user-images.githubusercontent.com/76187440/221807658-28a1eaeb-f486-44e8-bb2d-0402bcf89ad5.jpg" width="40%">
</p>


**Links and Joints**

There are three kinds of links that extend the design of each creature from 1D to 2D and 3D. The core structure of each creature is a 1 dimensional chain of links called the spine. Each spine can have 0, 1, or 2 legs attached to its faces, extending its structure into 2D. Each leg, in turn can have an optional foot extended below it, which creates the option for the design to turn into 3D.


**Spine.** Spines are rectangles connected in a 1D chain by revolute, floating, or planar joints through any of the 3 joint axes. Each **joint** is relatively positioned at the end of the previous block's x value, in the middle of the y value, and in the middle of each respect to height. The positions of each joint are also dynamically sized based on the length (in the x direction) of each spine piece to make sure that the blocks do not overlap. The positional, size, and joint logic for each joint is encapsulated in the ```link``` class.

<p align="center">
<img src="https://user-images.githubusercontent.com/76187440/221807087-290633af-40f2-4272-ab6c-527a78138e05.jpeg" height="250" width="500">
</p>

**Leg.** Legs protrude from spines in. The logic for the positioning, size, and joint position for each leg is encapsulated in the ```leg``` class.


**Foot**

As a result of the architectural decisions, this project can generate 1D, 2D, and 3D structures that can move in all dimensions due to the variability of joint types and joint axes.

**Synapses**
The code for synapses and brain generation is as follows. Synapses and the brain is generated bottom-up. At each link and leg level, there's a 50% chance whether or not a synapse will be placed at that location. Sensors are placed on those points and connected to motor neurons - which every link in the robot contains.

**Every kind of brain is possible**. Sensors are fully connected with motors with the potential for hidden layers, so that every sensor can affect every motor. Introducing hidden layers down the line would be a trivial task and allow for the robot to learn even more complex behavior. The 

**Evolution**

Evolution of each creature during the mutate stage can be occur in 4 distinct ways. The workaround to make calculation of morphology mutations during each evolution easier the introduction of a new field to the Spine, Leg, and Foot classes called ```isActive```. In Assignment 7, I generated limbs randomly on the spot - making spontaneous decisions to generate 0-4 limbs at each spine link while after generating the respective spine link. In Assignment 8, to better keep track of my links and neurons, I generate the information for a creature of N spines with 4 limbs (2 legs, 2 feet) at each spine, but mark a certain proportion of the spines to be inactive, which means that they don't appear. This makes the following mutations simpler to execute than doing spontaneous calculations to add, subtract, and modify links.
 
1.  Link Addition
2.  Link Subtraction
3.  Link Modification
4.  Update Weights (Brain)
                                                                                                                                       
