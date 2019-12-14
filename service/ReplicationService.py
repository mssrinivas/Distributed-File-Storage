import grpc
import sys

import json
sys.path.append('./proto')
sys.path.append('./service')
from proto import fileService_pb2_grpc, fileService_pb2


class ReplicationService(fileService_pb2_grpc.FileserviceServicer):

    def ReplicateFile(self, request, context):
            #print("request =", request.shortest_path[request.currentpos])
        # # next_node = request.shortest_path[request.currentpos]
        # if request.currentpos == len(request.shortest_path) - 1:
        #     cache.saveVClock(str(request), str(request))
        #     return fileService_pb2.ack(success=True, message="Data Replicated.")
        # else:
            # forward_server_addr = self.getneighbordata(next_node)
            #path = json.loads(request.shortest_path)
            forward_coordinates = request.shortest_path[request.currentpos]
            print("forward coord =", forward_coordinates)
            forward_server_addr = self.getneighbordata(forward_coordinates)
            print("forward IP =", forward_server_addr)
            forward_port = 5555
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

    def getneighbordata(self, next_node):
        print("CAME HERE")
        with open('data/metadata.json', 'r') as f:
            metadata_dict = json.load(f)
        print("'"+next_node+"'")
        nodes = metadata_dict['nodes']
        print(nodes)
        return nodes[next_node]