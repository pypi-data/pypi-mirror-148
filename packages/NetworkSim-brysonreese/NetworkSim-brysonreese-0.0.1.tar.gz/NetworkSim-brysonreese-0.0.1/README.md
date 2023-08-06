## NetworkSim
NetworkSim is a project I wrote for CPE 400 (Computer Networking) and have implemented testing and CI/CD for as a part of CS 491 (DevOps and Testing).

NetworkSim generates random double-weighted graphs and finds the shortest distance between each node to every other node in the graph. The user can specify the number of simulations they want to run and the program will create a directory of directories representing each simulation. In each simulation directory exists a .png picture of the graph and a text file that has a list of the shortest path between every node to every other node, along with the weight of taking that path.

This program simply brute forces all of these calculations, so I would recommend playing with it a bit before going and running a million simulations on a Core 2 Duo. YMMV!
___
I would recommend using a virtual environment to run this package.

To initialize, simply run:

    python3 -m venv env
    
    source env/bin/activate
Then to install the required packages, simply run:

    pip install -r requirements.txt
Once all required libraries are installed, simply run:

    python NetworkSim.py
___
After reading all of the initial prompts, please input the parameters that one would like to use to run the simulations. Some lightweight parameters that one can use to test the functionality can be found below:

Number of simulations: __ (Up to the user)

Estimated number of nodes: 15 (Takes usually less than 3 seconds per sim on 2017 Macbook Pro i7)

Edge creation probability: 0.2 (0.3 can be fine too, but expect longer time per simulation iteration)

Min/max weights for nodes/edges: __ (Up to the user, just arithmetic, doesn't affect performance)
