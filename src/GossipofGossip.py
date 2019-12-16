from threading import Lock, Thread
import math
import timeit
import json
import os
import random
import socket
from threading import Thread
import time
from enum import Enum
import sys
import grpc
import ast

sys.path.append('./proto')
sys.path.append('./service')
import grpc
import time
import math
from threading import Lock, Thread
import collections
import numpy as np


class GossipProtocol:
    capacity_of_neighbors_fixed = [1200, 3100, 7000, 5558]  # maintains the list of nodes
    totalNodes = [1234, 3456, 7899, 7543]
    sys.setrecursionlimit(200000)
    localMinimumCapacity = -sys.maxsize - 1
    local_message = None
    bufferSize = 1024
    # Create a datagram socket
    blacklisted_nodes = []
    minimum_IP_one = None
    minimum_Capacity_one = None
    minimum_IP_two = None
    minimum_Capacity_two = None
    listofNeighbors = []
    path = ["(0,0)", "(0,1)", "(0,2)"]
    counter = 1
    IPaddress = "169.105.246.3"
    localPort = 21000
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((IPaddress, localPort))
    stopReceiving = False

    def __init__(self):
        # self.initiateReplication()
        global best_nodes_to_replicate
        best_nodes_to_replicate = []
        print("HERE")
        self.start_threads()

    def input_message(self):
        message_to_send = "message"

    def checkforConvergence(self, Dictionary, BlackListedNodes, address):
        print("data = ", Dictionary)
        message_received = Dictionary
        print("SET OF BLACK LISTED NODES = ", self.blacklisted_nodes)
        print("MG  = ", message_received)
        print("LM  = ", self.local_message)

        if BlackListedNodes == None:
            if self.local_message == message_received:
                print("COUNTER =", self.counter)
                time.sleep(1)
                self.counter += 1
                if self.counter >= 5:
                    BlackListedNodes = []
                    BlackListedNodes.append(self.IPaddress)
                    BlackListedNodes = set(BlackListedNodes)
                    listofNeighbors = self.fetch_all_neighbors()
                    print("listofNeighbors", listofNeighbors)
                    print("BL NODES = ", BlackListedNodes)
                    # for ip in range(len(listofNeighbors)):
                    #     if ip in BlackListedNodes:
                    #         continue
                    #     else:
                    #         BlackListedNodes.append(listofNeighbors[ip])
                    #         #self.blacklisted_nodes = set(BlackListedNodes)
                    #BlackListedNodes = set(BlackListedNodes)
                    self.blacklisted_nodes = self.blacklisted_nodes + BlackListedNodes
                    self.blacklisted_nodes = set(self.blacklisted_nodes)
                    self.blacklisted_nodes = list(self.blacklisted_nodes)
                    if len(self.blacklisted_nodes) >= 3:
                        self.counter = 1
                        return True
                return False
            else:
                self.local_message = {}
                self.local_message = message_received.copy()
                print("ASSIGNED message", message_received , "from = ", address)
                time.sleep(1)
                self.counter = 1
                return False

        if BlackListedNodes != None:
            if self.local_message == message_received:
                print("COUNTER =", self.counter)
                time.sleep(1)
                self.counter += 1
                if self.counter >= 5:
                    if self.IPaddress not in BlackListedNodes:
                        BlackListedNodes.append(self.IPaddress)
                    print("listofNeighbors", self.listofNeighbors)
                    # listofNeighbors = self.fetch_all_neighbors()
                    # for ip in range(len(listofNeighbors)):
                    #     if ip in BlackListedNodes:
                    #         continue
                    #     else:
                    #         BlackListedNodes.append(listofNeighbors[ip])
                            #self.blacklisted_nodes = set(BlackListedNodes)
                    self.blacklisted_nodes = self.blacklisted_nodes + BlackListedNodes
                    self.blacklisted_nodes = set(self.blacklisted_nodes)
                    self.blacklisted_nodes = list(self.blacklisted_nodes)
                    print("NEW BL", BlackListedNodes)
                    # if len(self.blacklisted_nodes) >= 0.75 * len(self.totalNodes):
                    if len(self.blacklisted_nodes) >= 3:
                        self.counter = 1
                        return True
                return False
            else:
                self.local_message = {}
                self.local_message=message_received.copy()
                print("ASSIGNED message", message_received , "from = ", address)
                time.sleep(1)
                self.counter = 1
                return False

    def updated_message_util(self, data, minimum_capacity_one,minimum_capacity_two, leastUsedIP_one, leastUsedIP_two, gossip_phase):
        # update message
        Dictionary = {leastUsedIP_one: minimum_capacity_one, leastUsedIP_two: minimum_capacity_two}
        IPaddress = data.get("IPaddress")
        gossip = gossip_phase
        return IPaddress, gossip, Dictionary

    def find_minimum_in_dictionary(self, dictionary):
        print("SICT = ", dictionary)
        mini_one = min(dictionary, key=lambda k: dictionary[k])
        print("MINIMUM ONE= ", [mini_one, dictionary[mini_one]])
        self.minimum_IP_one = mini_one.strip('\n')
        self.minimum_Capacity_one = dictionary[mini_one]
        del dictionary[mini_one]
        mini_two = min(dictionary, key=lambda k: dictionary[k])
        print("MINIMUM TWO= ", [mini_two, dictionary[mini_two]])
        self.minimum_IP_two = mini_two.strip('\n')
        self.minimum_Capacity_two = dictionary[mini_two]
        return [self.minimum_IP_one, self.minimum_Capacity_one], [mini_two.strip('\n'), dictionary[mini_two]]

    def find_one_minimum_in_dictionary(self, dictionary):
        print("SICT = ", dictionary)
        mini_one = min(dictionary, key=lambda k: dictionary[k])
        print("MINIMUM ONE= ", [mini_one, dictionary[mini_one]])
        self.minimum_IP_one = mini_one.strip('\n')
        self.minimum_Capacity_one = dictionary[mini_one]
        return [self.minimum_IP_one, self.minimum_Capacity_one], None

    def fetch_all_neighbors(self):
        list_of_neigbors = []
        filepath = '../metadata/neighbors.txt'
        with open(filepath, "r") as ins:
            for line in ins:
                print(line)
                line = line.strip('\n')
                list_of_neigbors.append(line)
        return list_of_neigbors

    def get_minimum_capacity_neighbors(self, initalReplicaServer):
        list_of_neigbors = []
        capacity_of_neighbors = {}
        filepath = '../metadata/neighbors.txt'
        with open(filepath, "r") as ins:
            for line in ins:
                print(line)
                line = line.strip('\n')
                list_of_neigbors.append(line)
        counter = 0
        self.listofNeighbors = list_of_neigbors
        if initalReplicaServer in list_of_neigbors:
            list_of_neigbors.remove(initalReplicaServer)
        while len(list_of_neigbors) > 0:
            print("number of neighbours: ", len(list_of_neigbors))
            forwardIP = random.choice(list_of_neigbors)
            print("SENDING NEXT TO = ", forwardIP)
            hostname = str.encode(forwardIP)
            hostname2 = forwardIP
            print("HOSTNAME = ", hostname2, "INT REPL =", initalReplicaServer)
            if hostname2 != initalReplicaServer:
                print("ping -c 1 " + hostname.decode("utf-8"))
                response = os.system("ping -c 1 " + hostname.decode("utf-8"))
                # and then check the response
                if response == 0:
                    print(hostname, 'up')
                    # Call to check capacity
                    if hostname2 == "169.105.246.6":
                        coordinates = "(1,1)"
                    elif hostname2 == "169.105.246.7":
                        coordinates = "(0,0)"
                    else:
                        coordinates = "(0,2)"
                    print("GET COORDINATES CAP OF", coordinates)
                    IPaddress, capacity = self.getneighborcapacity(coordinates)
                    print("GET CAPACITY OF NEIGHBORS = ", IPaddress, capacity)
                    capacity_of_neighbors[IPaddress] = capacity
                    counter += 1
                    list_of_neigbors.remove(hostname2)
                else:
                    print(hostname, 'down')
                    counter += 1
                    list_of_neigbors.remove(hostname2)

        if len(capacity_of_neighbors) == 0:
            return None, None
        if len(capacity_of_neighbors) == 1:
            print("capacity_of_neighbors = ", capacity_of_neighbors)
            minimum, blank = self.find_one_minimum_in_dictionary(capacity_of_neighbors)
            return [minimum[0], minimum[1]], ["255.255.255",sys.maxsize]
        else:
            print("capacity_of_neighbors = ", capacity_of_neighbors)
            first_minimum, second_minimum = self.find_minimum_in_dictionary(capacity_of_neighbors)
            return [first_minimum[0], first_minimum[1]],[second_minimum[0], second_minimum[1]]

    def receive_message(self):
        while True:
            messageReceived, address = self.UDPServerSocket.recvfrom(1024)
            print(messageReceived)
            print("local message=", self.local_message)
            data = json.loads(messageReceived.decode())
            print("GOT DATA ", data, " FROM", address[0])
            IPaddress = data.get("IPaddress")
            gossip_flag = data.get("gossip")
            Dictionary = data.get("Dictionary")
            BlackListedNodes = data.get("BlackListedNodes")
            if len(BlackListedNodes) >= 3:
                continue
            if str(IPaddress) == self.IPaddress and gossip_flag == False:
                print("Faaaaaaaaaaaaaaaaaakkkkkk")
                self.blacklisted_nodes=[]
                time.sleep(1)
                list_of_neighbors = self.fetch_all_neighbors()
                minimum_capacity_neighbor_one, minimum_capacity_neighbor_two = self.get_minimum_capacity_neighbors(IPaddress)
                if minimum_capacity_neighbor_one == None and minimum_capacity_neighbor_two == None:
                    continue
                max_size = sys.maxsize
                minimum_capacity_one = min(minimum_capacity_neighbor_one[1], max_size)
                minimum_capacity_two = min(minimum_capacity_neighbor_two[1], max_size)
                self.counter = 1
                IPaddress, gossip, Dictionary = self.updated_message_util(data, minimum_capacity_one, minimum_capacity_two,  minimum_capacity_neighbor_one[0], minimum_capacity_neighbor_two[0], True)
                print("Inside-If", IPaddress, gossip, Dictionary)
                for ip in range(len(list_of_neighbors)):
                    response = os.system("ping -c 1 " + list_of_neighbors[ip].strip('\n'))
                    if response == 0:
                        IPaddressOne = list_of_neighbors[ip].strip('\n')
                        print("--------------------")
                        print(IPaddressOne, IPaddress, True, Dictionary, BlackListedNodes)
                        print("--------------------")
                        self.transmit_message(IPaddressOne, IPaddress, False, Dictionary, BlackListedNodes)
                    else:
                        continue
            elif gossip_flag:
                print("local message inside gossip_flg=", self.local_message)
                Convergence_Value = self.checkforConvergence(data.get("Dictionary"), BlackListedNodes, address[0])
                print(" CONVERGENCE = ", Convergence_Value)
                time.sleep(1)
                if Convergence_Value == True:
                    continue
                else:
                    list_of_neighbors = self.fetch_all_neighbors()
                    minimum_capacity_neighbor_one, minimum_capacity_neighbor_two = self.get_minimum_capacity_neighbors(IPaddress)
                    print("MINIMUM of minimum_capacity_neighbors = ", minimum_capacity_neighbor_one, " ------ ", minimum_capacity_neighbor_two)
                    Temp = data.get("Dictionary")
                    if minimum_capacity_neighbor_one == None and minimum_capacity_neighbor_two == None:
                        continue
                    Local_Dict = {minimum_capacity_neighbor_one[0]:minimum_capacity_neighbor_one[1] , minimum_capacity_neighbor_two[0]:minimum_capacity_neighbor_two[1]}
                    Temp.update(Local_Dict)
                    New_Dict = {}
                    New_Dict.update(sorted(Temp.items(), key=lambda x: x[1]))
                    print("NEW DICT", New_Dict)
                    first_minimum = New_Dict[list(New_Dict.keys())[0]]
                    second_minimum = New_Dict[list(New_Dict.keys())[1]]
                    Temp_Dict = {list(New_Dict.keys())[0]:first_minimum, list(New_Dict.keys())[1]:second_minimum}
                    print(Temp_Dict, Local_Dict)
                    if Temp_Dict != Local_Dict:
                        IPaddress, gossip, Dictionary_updated = self.updated_message_util(data, first_minimum, second_minimum,
                                                                                  list(New_Dict.keys())[0],
                                                                                  list(New_Dict.keys())[1], True)
                        print("Inside If", IPaddress, gossip, Dictionary_updated)
                        for ip in range(len(list_of_neighbors)):
                            response = os.system("ping -c 1 " + list_of_neighbors[ip].strip('\n'))
                            if response == 0:
                                IPaddressOne = list_of_neighbors[ip].strip('\n')
                                print("--------------------")
                                print(IPaddressOne, IPaddress, True, Dictionary_updated, self.blacklisted_nodes)
                                print("--------------------")
                                self.transmit_message(IPaddressOne, IPaddress, True, Dictionary_updated, self.blacklisted_nodes)
                            else:
                                continue
                    else:
                        for ip in range(len(list_of_neighbors)):
                            response = os.system("ping -c 1 " + list_of_neighbors[ip].strip('\n'))
                            if response == 0:
                                IPaddressOne = list_of_neighbors[ip].strip('\n')
                                Dictionary = data.get("Dictionary")
                                print("--------------------")
                                print(IPaddressOne, IPaddress, True, Dictionary, self.blacklisted_nodes)
                                print("--------------------")
                                self.transmit_message(IPaddressOne, IPaddress, True, Dictionary, self.blacklisted_nodes)
                            else:
                                continue

            elif gossip_flag == False and self.IPaddress != IPaddress:
                print("inside false=", self.local_message)
                self.blacklisted_nodes = []
                list_of_neighbors = self.fetch_all_neighbors()
                minimum_capacity_neighbor_one, minimum_capacity_neighbor_two = self.get_minimum_capacity_neighbors(
                    IPaddress)
                print("MINIMUM of minimum_capacity_neighbors = ", minimum_capacity_neighbor_one, " ------ ",
                      minimum_capacity_neighbor_two)
                Temp = data.get("Dictionary")
                if minimum_capacity_neighbor_one == None and minimum_capacity_neighbor_two== None:
                    continue
                Local_Dict = {minimum_capacity_neighbor_one[0]: minimum_capacity_neighbor_one[1], minimum_capacity_neighbor_two[0]: minimum_capacity_neighbor_two[1]}
                Temp_Dict.update(Local_Dict)
                New_Dict = {}
                New_Dict.update(sorted(Temp.items(), key = lambda x : x[1]))
                print("NEW DICT", New_Dict)
                first_minimum = New_Dict[list(New_Dict.keys())[0]]
                second_minimum = New_Dict[list(New_Dict.keys())[1]]
                Temp_Dict = {list(New_Dict.keys())[0]:first_minimum, list(New_Dict.keys())[1]:second_minimum }
                print(Temp_Dict,Local_Dict)
                if Temp_Dict != Local_Dict:
                    IPaddress, gossip, Dictionary_updated = self.updated_message_util(data, first_minimum, second_minimum,
                                                                              list(New_Dict.keys())[0],
                                                                              list(New_Dict.keys())[1], True)
                    print("Inside If", IPaddress, gossip, Dictionary_updated)
                    for ip in range(len(list_of_neighbors)):
                        response = os.system("ping -c 1 " + list_of_neighbors[ip].strip('\n'))
                        if response == 0:
                            IPaddressOne = list_of_neighbors[ip].strip('\n')
                            print("--------------------")
                            print(IPaddressOne, IPaddress, True, Dictionary_updated, self.blacklisted_nodes)
                            print("--------------------")
                            self.transmit_message(IPaddressOne, IPaddress, True, Dictionary_updated, self.blacklisted_nodes)
                        else:
                            continue
                else:
                    for ip in range(len(list_of_neighbors)):
                        response = os.system("ping -c 1 " + list_of_neighbors[ip].strip('\n'))
                        if response == 0:
                            IPaddressOne = list_of_neighbors[ip].strip('\n')
                            Dictionary = data.get("Dictionary")
                            print("--------------------")
                            print(IPaddressOne, IPaddress, True, Dictionary, self.blacklisted_nodes)
                            print("--------------------")
                            self.transmit_message(IPaddressOne, IPaddress, True, Dictionary, self.blacklisted_nodes)
                        else:
                            continue


    def transmit_message(self, hostname, IPaddress, gossip, Dictionary, BlackListedNodes):
        serverAddressPort = (hostname, 21000)
        bufferSize = 1024
        # message = json.dumps(message_to_be_gossiped)
        message = json.dumps(
            {"IPaddress": IPaddress, "gossip": gossip, "Dictionary": Dictionary,
             "BlackListedNodes": self.blacklisted_nodes})
        print("Sending message to", message)
        self.UDPServerSocket.sendto(message.encode(), serverAddressPort)

    def getneighbordata(self, next_node):
        with open('../metadata/metadata.json', 'r') as f:
            metadata_dict = json.load(f)
        nodes = metadata_dict['nodes']
        return nodes[next_node]

    def getneighborcapacity(self, next_node):
        with open('../metadata/metadata.json', 'r') as f:
            metadata_dict = json.load(f)
        nodes = metadata_dict['capacities']
        print("all nodes", nodes[next_node])
        return nodes[next_node][0], nodes[next_node][1]

    def start_threads(self):
        # Thread(target=self.replicateContent()).start()
        # Thread(target=self.retries).start()
        Thread(target=self.receive_message).start()
