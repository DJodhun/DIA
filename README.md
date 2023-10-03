# Designing Intelligent Agents

This project compared the performance of the Genetic Algorithm to the A* Search Algorithm when trying to maximise the dirt collected by an autonomous robotic vacuum cleaner. This was tested across three different environments, or maps: a clear room, a living room and a bedroom. The robot is considered to be an intelligent agent, capable of moving forwards, backwards, left and right, as well as turning 360 degrees. The dimensions are 60 × 60 square body, with 2 sensors and 2 wheels, operating a differential drive system.

Experiment design:
  -Running 30 generations on the Genetic Algorithm, and 400 runs for the A* Search Algorithm, per map.
  -Gather statistics, in particular the average dirt collected per map per algorithm. 
  -Perform statistical analysis.
  -Find significant results.

The results from this project showed that the Genetic Algorithm was superior to the A* Search Algorithm in all cases, having a higher average amount of dirt collected, using a t-test at the 5% significance level. 

