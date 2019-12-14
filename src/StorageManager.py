import sys

sys.path.append('./')
sys.path.append('./proto')
sys.path.append('./service')
import grpc
import chunk_pb2, chunk_pb2_grpc
from src.MemoryManager import MemoryManager
from src.InitiateReplica import InitiateReplication

CHUNK_SIZE_ = 1024  # 1KB // the server (receiver node) must also be configured to take the same chunk size


class StorageManagerClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)

    def upload_chunk_stream(self, hash_id, chunk_size, number_of_chunks, stream_of_bytes_chunks):

        if str(CHUNK_SIZE_) != str(chunk_size):
            message = "Unable to save hash_id %s. Chunk size given %s and it should be %s" % (
                hash_id, chunk_size, CHUNK_SIZE_)
            raise Exception(message)

        metadata = (
            ('key-hash-id', hash_id),
            ('key-chunk-size', str(chunk_size)),
            ('key-number-of-chunks', str(number_of_chunks))
        )

        response = self.stub.upload_chunk_stream(stream_of_bytes_chunks, metadata=metadata)

        if response.success:
            print("Successfully saved the data with hash_id: ", hash_id)
        else:
            print("Failed saved the data with hash_id", hash_id)

        return chunk_pb2.Reply(success=response.success)

    def upload_single_chunk(self, hash_id, chunk_size, chunk_bytes):

        if str(CHUNK_SIZE_) != str(chunk_size):
            message = "Unable to save hash_id %s. Chunk size given %s and it should be %s" % (
                hash_id, chunk_size, CHUNK_SIZE_)
            raise Exception(message)

        metadata = (
            ('key-hash-id', hash_id),
            ('key-chunk-size', str(chunk_size)),
        )

        response = self.stub.upload_single_chunk(chunk_bytes, metadata=metadata)

        if response.success:
            print("Successfully saved the data with hash_id: ", hash_id)
        else:
            print("Failed saved the data with hash_id", hash_id)

    def download_chunk_stream(self, hash_id):
        response = self.stub.download_chunk_stream(chunk_pb2.Request(hash_id=hash_id))
        print("Successfully downloaded file with hash_id: ", hash_id)
        return response

    def get_node_available_memory_bytes(self):
        return self.stub.get_available_memory_bytes(chunk_pb2.Empty_request()).bytes

    def get_node_stored_hashes_list_iterator(self):
        return self.stub.get_stored_hashes_list_iterator(chunk_pb2.Empty_request())

    def hash_id_exists_in_memory(self, hash_id):
        return self.stub.hash_id_exists_in_memory(chunk_pb2.Request(hash_id=hash_id)).success


class StorageManagerServer(chunk_pb2_grpc.FileServerServicer):

    def __init__(self, memory_node_bytes, page_memory_size_bytes):
        self.memory_manager = MemoryManager(memory_node_bytes, page_memory_size_bytes)

    def upload_chunk_stream(self, request_iterator, context):
        hash_id = ""
        chunk_size = 0
        number_of_chunks = 0

        for key, value in context.invocation_metadata():
            if key == "key-hash-id":
                hash_id = value
            elif key == "key-chunk-size":
                chunk_size = int(value)
            elif key == "key-number-of-chunks":
                number_of_chunks = int(value)

        assert hash_id != ""
        assert chunk_size != 0
        assert number_of_chunks != 0

        success = self.memory_manager.put_data(request_iterator, hash_id, number_of_chunks, False)
        InitiateReplication.__init__()
        return chunk_pb2.Reply(success=success)

    def upload_single_chunk(self, request_chunk, context):
        hash_id = ""
        chunk_size = 0

        for key, value in context.invocation_metadata():
            if key == "key-hash-id":
                hash_id = value
            elif key == "key-chunk-size":
                chunk_size = int(value)

        assert hash_id != ""
        assert chunk_size != 0

        success = self.memory_manager.put_data(request_chunk, hash_id, 1, True)
        return chunk_pb2.Reply(success=success)

    def download_chunk_stream(self, request, context):
        chunks = self.memory_manager.get_data(request.hash_id)
        for c in chunks:
            yield chunk_pb2.Chunk(buffer=c)

    def get_available_memory_bytes(self, request, context):
        bytes_ = self.memory_manager.get_available_memory_bytes()
        return chunk_pb2.Reply_double(bytes=bytes_)

    def get_stored_hashes_list_iterator(self, request, context):
        list_of_hashes = self.memory_manager.get_stored_hashes_list()
        for hash_ in list_of_hashes:
            yield chunk_pb2.Reply_string(hash_id=hash_)

    def hash_id_exists_in_memory(self, request, context):
        hash_exists = self.memory_manager.hash_id_exists(request.hash_id)
        return chunk_pb2.Reply(success=hash_exists)

        # initiate_replication
        # 2 best nodes
        # paths to them
        # stream_of_bytes_chunks_downloaded = send_node.download_chunk_stream(hash_id)
