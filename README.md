# xerox

## System Architecture

![Alt text](ScreenShots/mesh-architecture.png?raw=true "Owner Home Page")


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

