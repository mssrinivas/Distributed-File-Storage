# Distributed File Storage System

## System Architecture

![Alt text](ScreenShots/mesh-architecture.png?raw=true "Architecture")


### Reason for a three-phase replication :

The initial idea was having the replicas in the best suited neighboring nodes. However, this
could create hotspots in the system which might lead to complete data loss if the path to the
node is blocked, or if there is a network partition in the system. Selecting random nodes spread
across the system solves that problem. Also, since the read requests were being forwarded in a
random fashion by the chunk server, the probability of hitting the right node that has the value is
higher. Thus, spreading the data replicas to further nodes allows faster reads.

Replication in the 2D Mesh File storage system is held in three phases :

1. Gossip About Gossip:
This is not a Master-Slave architecture with a single node dependency for
accepting the writes. Also, in the 2D Mesh architecture, all nodes are not connected to
others in the system, gossiping was the best way for the team to pass information.
Idea : In Gossip about Gossip, not only a random node is selected to pass some
information but the information being passed is the history of the Gossip itself. A node not
only passes the value that it knows but also passes what it heard from others.

2. Virtual Voting : 
A node after receiving a value will compute locally to find the best node to replicate in the system. The computation is a comparison of the already existing local value and the newly received value. The node that receives a request (write/update/delete) initiates a gossip where it compares the capacities of its neighboring nodes and the broadcasts the lowest-capacity node that can handle the data. A convergence criteria of 50% of the nodes agreeing to a value stops the gossip and gives the initiator a node value to replicate. When a node receives the same value more than 10 times, it gets added to the Blacklist and stops gossiping.

3. Creation of a logical snapshot of the network
After receiving the coordinates of the alive nodes, the replication initiator creates a logical snapshot of the grid that helps it traverse to the node it wants to replicate at.
	

4. Traversal 
A Breadth-first traversal leads the data to the soon to be a replica node. The best thing about this implementation was the shortest path calculation with failure detection. That ensures that the initiating replica receives an acknowledgment from the replicating server.


![Alt text](ScreenShots/Picture1.png?raw=true "Architecture")


