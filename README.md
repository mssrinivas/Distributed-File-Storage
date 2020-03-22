# Replication in a distributed file storage system

![Alt text](ScreenShots/replication.png?raw=true "Architecture")

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


### Implementation Overview

### Stage - 1:

When a “write request” or an “update request” is performed, middleware redirects the request to one of the nodes in the underlying architecture. 

Let us assume  Node - p gets the request.


![Alt text](ScreenShots/diagram-01.png?raw=true "Architecture")
		
				Figure.  The initial state of the system


### Stage - 2:

On Node - p “Best nodes for replication” module gets triggered for picking the best nodes to perform replication which are spread across the network. This method avoids the hotspots around the nodes that have taken the “write requests”. This methodology also helps in “read requests”. When a random node receives a read request, there are higher chances of nodes (holding the required data) encountered in a quick time when there is a spread of replica nodes. 


![Alt text](ScreenShots/diagram-2.png?raw=true "Architecture")

			Figure. Trigger “Best nodes for replication” for picking 2 nodes






### Stage - 3:

Gossip of Gossip is triggered to find the best nodes. In every gossip call, three different evaluations are performed:

Check for convergence
Calculate the best capacity of neighbors
Evaluate Incoming best capacity with the local best capacity 

Gossip the evaluations accordingly to all the neighbors
This is performed until the convergence is met.

![Alt text](ScreenShots/diagram-03.png?raw=true "Architecture")
				
				Figure.  Gossip of Gossip convergence

### Stage - 4: 

Based on the metadata that gets exchanged on a network level, we build a logical snapshot of the network for finding a path to the agreed nodes for replication. Assume node-x and node-y are picked as the best nodes for the replication. As shown in the matrix if a node is down we mark it as 0 and if it is up we mark it as 1 and create a logical mesh out of the available data.

![Alt text](ScreenShots/diagram-05.png?raw=true "Architecture")

				Figure.  Generation of logical snapshot


### Stage - 5:

After performing “Gossip of Gossip” to achieve virtual consensus and generating a logical snapshot of the underlying network, we now calculate the shortest path with failure nodes from the replication initiation node (node - p) to destination replica-nodes (node-x and node-y). All these calculations are performed on the node that has initiated the replication. 


### Stage - 6: 

Once the shortest path gets established. Data has to be packed into objects  and passed on to the neighbor nodes listed in the path. Every time a node gets the data to be replicated, two operations are performed

If the node is the destination node, it triggers the upload function which writes to the memory
If the node is not the destination node, it evaluates the forwared_to node using the metadata and passes on the data object until step 1 is satisfied.



![Alt text](ScreenShots/diagram-06.png?raw=true "Architecture")

				Figure.  Replication path to node x
				



				
				
![Alt text](ScreenShots/diagram-07.png?raw=true "Architecture")




Data is replicated successfully on two nodes.

## Pseudo code : 

### Virtual Consensus : 

~~~ Gossip Receive

def receive_gossip(self, gossip_received):
       check_for_convergence = convergence(gossip_received)
       if check_for_convergence == False:
         best_known = max(capacities_of_neigbors)
         best_capacity_node = max(gossip_received, best_known)
         transmit_gossip(best_capacity_node)
       else:
         #wait for other gossip

# Gossip Transmit
 def transmit_gossip(self, gossip_trasmit):
       all_neighbors = fetch_neighbors(self.IPaddress)
       transmit(all_neighbors)

# Gossip Convergence Check ( Simplest way )

def convergence(self, gossip_received):
 if gossip_received == gossip_known:
   counter=counter+1
   
 if counter == 10:
   black_listed_nodes.append(self.IPaddress)
   
# Optimization

   all_neighbors = fetch_neighbors(self.IPaddress)
   black_listed_nodes.append(all_neighbors)
   if len(black_listed_nodes) >= 0.5 *  (total_network_length):
   return True
 return False
~~~
### Logical Mesh generation : 

~~~

create_2D_grid(self, metadata):
   metadata = sort_list_on_y(metadata)
   metadata = sort_list_on_x(metadata) 
   dictionary = {} 
   map each element in dictionary to a key
   number_of_rows = absolute(min(x)) + max(x) 
   number_of_cols = absolute(min(y)) + max(y)
   list = reshape(metadata, number_of_rows, number_of_cols)
   call_bfs(list)

~~~

### Breadth-First : 

~~~

# Breadth First Search
bfs(grid,start_node, target_node):
 queue: to append the path
 set: to keep track of visited nodes

 Append start_node to the queue
 Iterate until the queue is Empty
   path = Pop from queue
   last_ele = last element(node) in path
    if last_ele of path equal to target node
      return path
    else
      iterate over every neighboring element of last_ele in the path
        if neighboring element not in set
            append the neighboring element to the path and queue
            add the neighboring element to the set

~~~

## References : 

[1] Gossip Based Computation of Aggregate Information 

[2] The Promise, And Limitations, of Gossip Protocols 

[3] Epidemic Algorithms for Replicated Database Maintenance 

[4] Gossip Protocols 

[5] Implementation of Gossip Protocol Using Elixir 

[6] Estimate Aggregates on a Peer-to-Peer Network 

[7] Gossip and Epidemic Protocol

[8] A General Explanation of Gossip about Gossip and How It Works

[9] Breadth First Search Tutorials & Notes: Algorithms

[10] Vector Clocks

[11] The SWIRLDS Hashgraph Consensus Algorithm: Fair, Fast, Byzantine Fault Tolerance 

[12] Hashgraph the Future of Decentralized Technology and the End of Blockchain





