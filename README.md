# ludobots - Assignment 6

# Button
Run search.py to run the evolutions and see the evolved robot. Or you can run button.py
Example: >python3 search.py

# What I did

Assignment 6:

Created a random number of links with random sizes

Added an array storing my sensor bodies in the constructor

Created a brain that connected selected sensors with all motors

Assigment 5:

I did three things in the assignment.

First, I implemented braniac and connected 4 hidden layers between my sensor neurons (feet and torso) and motor neurons. I created two sets of matrices that I updated everytime in self.mutate().

Second, I built a bipedal robot on top of a raised platform.

Third, I implemented a fitness function that would help the robot learn how to walk forward and balance. My fitness function was torsoX + 3 * torsoZ which is a weighted sum of the distance traveled as well as how upright the torso is - giving extra emphasis to keeping the torso upright so that the robot does not fall over in an attempt to maximize distance travel. I also implemented a penalty that reduced the fitness of each robot by 3 everytime it fell over (torsoZ < 1)
