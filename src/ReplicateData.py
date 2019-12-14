import sys
sys.path.append('./proto')
sys.path.append('./service')
import numpy as np
import collections
import grpc
from proto import fileService_pb2, fileService_pb2_grpc
import time
import math
import numpy as np

class ReplicateData :

    def __init__(self):
        # self.start_threads()
        pass
    
    def ReplicateFile(self, request, context):
        print("request", request.shortest_path)
        # next_node = request.shortest_path[request.currentpos]
        if request.currentpos == len(request.shortest_path) - 1:
            #cache.set(request, request)
            #Call upload
            return fileService_pb2.ack(success=True, message="Data Replicated.")
        else:
            forward_server_addr = "169.105.246.6"
            forward_port = 50051
            forward_channel = grpc.insecure_channel(forward_server_addr + ":" + str(forward_port))
            forward_stub = fileService_pb2_grpc.FileserviceStub(forward_channel)
            request.currentpos += 1
            rList = [1, 2, 3, 4, 5]
            arr = bytearray(rList)
            updated_request = fileService_pb2.FileData(initialReplicaServer=request.initialReplicaServer,
                                                        bytearray=request.bytearray, vClock=request.vClock,
                                                        shortest_path=request.shortest_path,
                                                        currentpos=request.currentpos + 1)
            forward_resp = forward_stub.ReplicateFile(updated_request)
            print("forward_resp", forward_resp)
            return fileService_pb2.ack(success=True, message="Data Forwarded.")

    def initiateReplication(self):
        serverAddress = "169.105.246."
        serverPort = 50051
        rList = [1, 2, 3, 4, 5]
        arr = bytes(rList)
        channel = grpc.insecure_channel(serverAddress + ":" + str(serverPort))
        replicate_stub = fileService_pb2_grpc.FileserviceStub(channel)
        request = fileService_pb2.FileData(initialReplicaServer="169.105.246.4", bytearray=arr,
                                            vClock="My V Clock", shortest_path=self.path, currentpos=0)
        resp = replicate_stub.ReplicateFile(request)
        print("Replication response", resp)

    def getPath(self):
        my_list = [(1, -1), (1, 0), (-1, 0), (0, 0), (0, 1), (1, 1)]
        my_list = sorted(my_list, key=lambda k: [k[1], k[0]])
        my_list = sorted(my_list, key=lambda k: [k[0], k[1]])
        # print(my_list)
        dicty = {}
        counter = 0
        listy = []
        for i in my_list:
            dicty[counter] = i
            listy.append(counter)
            counter += 1
        # print(dicty)
        x = np.array(listy)
        a = np.reshape(x, (2, 3))
        string_list = []
        for i in range(len(a)):
            temp = ""
            for j in range(len(a[i])):
                temp += str(a[i][j])
            string_list.append(temp)
        col = 0
        row = 0
        goal = "5"
        columns = 3
        rows = 2

        def bfs(self, grid, start):
            queue = collections.deque([[start]])
            seen = set([start])
            while queue:
                path = queue.popleft()
                x, y = path[-1]
                if grid[y][x] == goal:
                    return path
                for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= x2 < columns and 0 <= y2 < rows and grid[y2][x2] != -1 and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

        path = self.bfs(string_list, (col, row))
        print("PATHHHH==", path)