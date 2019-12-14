import sys
sys.path.append('./service')
sys.path.append('./proto')
sys.path.append('./')
from StorageManager import StorageManagerServer
import grpc
import time
import chunk_pb2, chunk_pb2_grpc
from concurrent import futures
from proto import fileService_pb2, fileService_pb2_grpc
from ReplicationService import ReplicationService

if __name__ == '__main__':
    print("Starting Storage Manager.")
    server_grpc = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    total_memory_node_bytes = 1 * 1024 * 1024 * 1024  # start with 1 GB
    CHUNK_SIZE_ = 1024
    total_page_memory_size_bytes = CHUNK_SIZE_
    chunk_pb2_grpc.add_FileServerServicer_to_server(StorageManagerServer(total_memory_node_bytes, total_page_memory_size_bytes), server_grpc)
    fileService_pb2_grpc.add_FileserviceServicer_to_server(ReplicationService(), server_grpc)
    port = 5555
    server_grpc.add_insecure_port(f'[::]:{port}')
    server_grpc.start()

    print("Storage Manager is READY.")

    try:
        while True:
            time.sleep(60 * 60 * 24)  # should infinity
    except KeyboardInterrupt:
        server_grpc.stop(0)
