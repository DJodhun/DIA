# Designing Intelligent Agents

## Background
Intelligent Agents can be used to simulate behaviours and systems that exist in the real world, such as flocks of birds (see the Boids algorithm) or, in this case, robotic vacuum cleaners. Using these systems, their performances via various algorithms can be compared and optimised without the cost of implementing and testing in the real world. 

This project compared the performance of the Genetic Algorithm to the A* Search Algorithm when trying to maximise the dirt collected by an autonomous robotic vacuum cleaner. This was tested across three different environments, or maps: a clear room, a living room and a bedroom. The Intelligent Agent in question is a robotic vacuum cleaner, capable of moving forwards, backwards, left and right, as well as turning 360 degrees. The dimensions (in pixels) are 60 × 60 square body, with 2 sensors and 2 wheels, operating a differential drive system.

## Experiment design:
  - Running 30 generations on the Genetic Algorithm, and 400 runs for the A* Search Algorithm, per map. This gets a similar number of iterations per algorithm per map.
  - Gather statistics, in particular the average dirt collected per algorithm per map.  
  - Perform statistical analysis.
  - Find significant results.

## Results
The results from this project showed that the Genetic Algorithm was superior to the A* Search Algorithm in all cases, having a higher average (and minimum) amount of dirt collected, using a t-test at the 5% significance level. Additionally, this was achieved in a faster run time. The results folder contains the boxplots illustrating the final results. 

## Future Work and Improvements
- An ideal run would not include a failed path, even if it had a high average amount of dirt. For example, if the robot ended up in a suboptimal destination or irretrievable, it would damage its lifetime amount of dirt collected. A pathfinding algorithm could be implemented to ensure it always ends at specfic location in the room would be useful.
- From the above point, in terms of results a failed path could result in the fitness function being multiplied by 0 if the robot did not arrive at the specified location at the end of the cleaning session. This could lead to the GA creating fewer 'all or nothing' robots and could potentially even the score.
- Adding in some more variation in objects and collisions: for example, allowing the robot to go underneath a table or sofa and potentially getting stuck.
- Use of Machine Learning (in particular Reinforcement Learning) to train the robot to detect, identify and avoid objects. This could be done by simulating a camera or similar technology, such as LiDAR or ultrasound as an array of beams that allow the robot to 'see'. 
