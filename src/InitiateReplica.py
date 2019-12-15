import json
import socket
import sys
sys.path.append('./proto')
sys.path.append('./service')

def start_replica():
    serverAddressPort = ("169.105.246.3", 21000)
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket
    print(serverAddressPort)
    dict = {}
    message = json.dumps({"IPaddress": "169.105.246.3", "gossip": False, "Dictionary": dict, "BlackListedNodes": []})
    UDPClientSocket.sendto(message.encode(), serverAddressPort)