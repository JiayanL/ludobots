# Jiayan's Evolving Ludobots (Artist)

Citation: This project was built on top of information from r/ludobots (https://www.reddit.com/r/ludobots/comments/l86j8r/start_here/) and pyrosim (https://github.com/jbongard/pyrosim). 
**Video:** https://www.youtube.com/watch?v=SbsmmTvQ7VM

**Plots:** https://docs.google.com/document/d/1a9HIz8jEoTmE7Z87z2EdnzLbEKmcnTYJZ8AMKB75wyM/edit

## Table of Contents
Deliverables
Citation

## Deliverables

## Running the Code as an Executable
There are four ways to execute the code depending on your goals.

**Seeding the Robot:** The robot can be seeded to reproduce random results. To do so, run ```python3 search.py seed desired_seed``` where desired_seed is the desired seed value you wish to see the robot with. This argument is optional and will be set to a default seed if not included.

**Running Engineer:** To run the engineer experiment (10 random seeds, 500 generations, 10 population size), run ```python3 search.py engineer```

**Loading a Saved Seed:** To load and view one of the saved examples, run ```python3 load_and_run.py seed``` where seed is the seed number of the robot you wish to load. All saved robots have been trained for 500 generations with a population size of 10.

**Tracking Lineage:** To track the evolution of a robot and view its performance at different stages of evolution, run ```python3 track_lineage.py seed generation``` where seed is the seed of the robot desired and generation is the generation you want to view the robot in. Currently, you can only run this code with generation values of ```0, 249, and 499```

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

**Leg.** Legs protrude from spines in the y-direction. Each leg is placed relative to a **joint** located in the center of its parent link with respect to length (x) and height (z). The length of the leg will not exceed the length of its parent element to prevent intersecting. A corresponding joint is placed at the bottom of each leg if a foot exists. The logic for the positioning, size, and joint position for each leg is encapsulated in the ```leg``` class.

<p align="center">
<img src="https://user-images.githubusercontent.com/76187440/221812985-2e52131c-6a55-48e5-bae7-4604d41f67a0.jpg" height="250" width="500">
</p>

**Foot** Feet protrude from under legs, if they exist. Each foot is placed at the bottom and towards the edge of each leg. The height of each foot will not exceed the height between the leg and the floor to prevent the robot from shooting out of the ground. There is one **joint** here between each foot and each leg and it is positioned such that the half the foot is under the leg in the y-direction and the foot touches the bottom of each leg with respect to the z-axis. The logic for the positioning, size, and joint position for each leg is encapsulated in the ```leg``` class.

<p align="center">
 <img src="https://user-images.githubusercontent.com/76187440/221813248-b9c74606-8dc3-4ad1-ad63-6b88fd1f316f.jpg" height="250" width="500">
 </p>

As a result of the architectural decisions, this project can generate 1D, 2D, and 3D structures that can move in all dimensions due to the variability of joint types and joint axes.

**Synapses**
In the constructor, I allocate a certain percentage of the total links generated to have synapses. This information is also encoded in the class containing the link information for each link and reflects in the color of each link. I add a sensor neuron to each of these sensor links and connect them to a motor neuron attached to every joint.

**Every kind of brain is possible**. Sensors are fully connected with motors with the potential for hidden layers, so that every sensor can affect every motor. Introducing hidden layers down the line would be a trivial task and allow for the robot to learn even more complex behavior. The 

## Evolution

Evolution of each creature during the mutate stage can be occur in 4 distinct ways. The workaround to make calculation of morphology mutations during each evolution easier the introduction of a new field to the Spine, Leg, and Foot classes called ```isActive```. In Assignment 7, I generated limbs randomly on the spot - making spontaneous decisions to generate 0-4 limbs at each spine link while after generating the respective spine link. In Assignment 8, to better keep track of my links and neurons, I generate the information for a creature of N spines with 4 limbs (2 legs, 2 feet) at each spine, but mark a certain proportion of the spines to be inactive, which means that they don't appear. This is a preset figure marked in a similar way to the array that stores whether or not a link contains a sensor. Each spine has corresponding information about whether or not it has legs, and how many. This makes the following mutations simpler to execute than doing spontaneous calculations to add, subtract, and modify links.
 
<p align="center">
<img src="https://user-images.githubusercontent.com/76187440/221823900-08381c8a-323d-46ea-82ad-28d1628f541f.jpeg" height="400" width="800">
</p>

**1.  Link Addition**

Link Addition is performed by taking a random link id from the number of total links (active and inactive), and marking it active if it is not active. If the current element I mark active is a foot link, I can also reference the parent field in the link to check whether or not the leg connecting it to the spine is active. If the leg is inactive, I also mark that link as active. Correspondingly, I add all the links I have active to a running array of active links so that I can render it in my Create_World function. I also add it to the tally of currently active links, so that my Create_Brain calculations can run smoothly. In this case, no new calculation has to be performed

**2.  Link Subtraction**

Similar to Link Addition, I perform link subtraction by finding a random link id from the number of total links (active and inactive) and marking it inactive if it is active. If the current element I mark is a leg link, I also mark the corresponding foot link inactive. I do not apply this mutation to spine link elements because I think it is unrealistic given what I know about biological evolution. Using information stored in the class, I remove it from the active links array, so that it does not get rendered and decrement the count of currently active links, adjusting the sensor array, so that the neurons are also properly adjusted for the loss of 0-2 links in the body.

**3.  Link Modification**

Link modification triggers a recalculation of a link's size and joint positioning. However, this is only performed on legs and feet due to the difficulties associated with adjusting the size of a spinal link. The way this is done is by recalculating the joint and link positions through the Leg constructor. By taking the id of the current link and replacing the reference to it in my link dictionary with a new Leg element, I'm able to swap out a new size constructor, that may also have a different sensor/color value without difficulty because the relative position to the spinal joint as well of the position of the joint to connect the newly sized link are calculated based off of size in the Leg class. The benefit of using the class is that it sets an upper limit to the size of each element to ensure that it won't overlap with other elements (i.e. max length is less than the length of its parent element, and the height is calculated such that it isn't taller than the creature, causing it to shoot out of the ground).

**4.  Update Weights (Brain Evolution)**

Evolving the brain is done the same way it was done in previous assignments. The mutate function chooses a random row and a random column and assigns a random value to the corresponding entry in the sensor to motor neuron weights.        

## Citations and Acknowledgements
This project was built on top of information from [r/ludobots](https://www.reddit.com/r/ludobots/comments/l86j8r/start_here/) and the python [pyrosim library](https://github.com/jbongard/pyrosim).

This project would not have been possible without the instruction and guidance of Professor [Sam Kriegman](https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/kriegman-sam.html). You can learn more about Professor Krigeman's groundbreaking research on Xenobots [here](https://www.xenobot.group/). Additionally, thank you to TA Donna Hooshmand and PM Jack Burdhardt for their help and flexibility. Their assistance throughout office hours, post-class discussions, and campuswire made the entire project process very smooth. Thank you for all the help throughout the course!
