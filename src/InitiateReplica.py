import json
import socket
import sys

import ReplicateData

sys.path.append('./proto')
sys.path.append('./service')
import time


class InitiateReplication:
    def __init__(self):
        pass

    def start_replica(self):
        print("CAME HERE too?")
        file_input = open('./data/test.txt')  # opens a file in reading mode
        data = file_input.read(1024)  # read 1024 bytes from the input file
        bytesToSend = str.encode(data)
        print(bytesToSend)
        serverAddressPort = ("169.105.246.3", 21000)
        bufferSize = 1024
        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        print(serverAddressPort)
        dict = {"169.105.246.3": 7129}
        message = json.dumps(
            {"IPaddress": "169.105.246.3", "gossip": False, "Dictionary": dict, "BlackListedNodes": []})
        UDPClientSocket.sendto(message.encode(), serverAddressPort)  # gossip initialtion
        # end of gossip
        sys.exit(0)
    # print(resp)
    # gp.initiateReplication()
    # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    # msg = "Message from Server {}".format(msgFromServer[0])
