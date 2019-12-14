import os
import sys
import hashlib
import math
from StorageManager import StorageManagerClient
import chunk_pb2


def generate_hash_id(app_name, file_name):
    name_path = app_name + file_name
    hash_object = hashlib.sha1(name_path.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def get_file_chunks(filename, chunk_size):
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                return
            yield chunk_pb2.Chunk(buffer=chunk)


def save_chunks_to_file(filename, chunks):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)


if __name__ == '__main__':
    send_node = StorageManagerClient('localhost:5555')

    if len(sys.argv) == 1:
        print("Please pass in at least one argument")
        sys.exit()

    file_p = sys.argv[1]
    file_n = os.path.basename(file_p)
    file_size_bytes = os.path.getsize(file_p)
    chunk_size = 1024  # 1KB

    app_n = "dropbox_app"
    download_file = "false"

    if len(sys.argv) > 2:
        app_n = sys.argv[2]

    if len(sys.argv) > 3:
        download_file = sys.argv[3]

    ######### send (upload) file request as stream of bytes chunks #######
    hash_id = generate_hash_id(app_n, file_n)
    number_of_chunks = math.ceil(file_size_bytes / chunk_size)
    stream_of_bytes_chunks = get_file_chunks(file_p, chunk_size)

    print("Hash_id exists: ", send_node.hash_id_exists_in_memory(hash_id))  # at the beginning this hash should not exist
    send_node.upload_chunk_stream(hash_id, chunk_size, number_of_chunks, stream_of_bytes_chunks)
    assert send_node.hash_id_exists_in_memory(hash_id) == True # it should exist

    print("\nSize available in bytes ", send_node.get_node_available_memory_bytes())
    print("Hashes saved so far: ")
    # for hash_ in send_node.get_node_stored_hashes_list_iterator():
    #     print(hash_.hash_id)

    # download file request
    stream_of_bytes_chunks_downloaded = send_node.download_chunk_stream(hash_id)
    output_path = "data/test_out.txt"
    save_chunks_to_file(output_path, stream_of_bytes_chunks_downloaded)

    ######### send (upload) string request as 1 chunk of bytes #######

    message = "Hello my name is Gash".encode()
    message_chunk_bytes = chunk_pb2.Chunk(buffer=message)
    message_id = "1223"
    hash_id = hashlib.sha1(message_id.encode()).hexdigest()

    send_node.upload_single_chunk(hash_id, chunk_size, message_chunk_bytes)

    # download file request
    stream_of_bytes_chunks_downloaded = send_node.download_chunk_stream(hash_id)
    output_path = "data/test_out3.txt"
    save_chunks_to_file(output_path, stream_of_bytes_chunks_downloaded)
