#error handling
FULL_MEMORY = 2
MEM_TABLE_CORRUPTED = 3
from pprint import pprint as pp

class MemoryManager:
    '''
        Class to manage memory blocks to be used in distributed memory management

        We would use this class as a backbone to store and find memory allocated in the local server

        Attributes:
        memory: identification of the block of memory stored

        Methods:
        int: Description of return value

    '''
    mem_table = []
    server_id = None
    mem_size = None
    mem_size = None
    next_empty_block = None
    empty_blocks_left = None

    def __init__(self, server_id, size):
        self.mem_table = [MemoryBlock()] * size
        self.server_id = server_id
        self.mem_size = size
        self.next_empty_block = 0
        self.empty_blocks_left = size

    def find_empty_block(self):
        empty_block = None
        location = 0
        for index, block in enumerate(self.mem_table):
            # pp(dir(block))
            if block.free == True:
                empty_block = block
                location = index
                break
            else:
                continue

        if empty_block == None:
            print("empty block: {}".format(empty_block))
            raise Exception(FULL_MEMORY)

        if location == self.mem_size - 1:
            print("location: {}".format(empty_block))
            print("self.mem_size: {}".format(self.mem_size - 1))
            raise Exception(FULL_MEMORY)


        return location, empty_block

    def set_memory_block(self, data):
        location, new_block = self.find_empty_block()
        block_id = "{}_{}".format(self.server_id, location)
        new_block.set_data(block_id, data, next_block=None)
        return block_id


    def get_memory_block(self):
        pass

    def delete_memory_block(self):
        pass

    def get_data_allocated(self):
        pass

    def return_data_allocated(self):
        pass

    def serialize_data(self):
        pass

    def decode_data(self):
        pass

    def get_empty_spaces(self):
        pass




class MemoryBlock:
    '''
    Class to define a memory block to be used in distributed memory management

    We would use this class as a building block to store and find memory allocated in the local server

    Attributes:
    block_id: identification of the block of memory stored

    Methods:
    int: Description of return value

    '''
    mem_id = None
    data = None
    next_block = None
    free = True

    def __init__(self):
        self.mem_id = None
        self.data = None
        self.next_block = None
        self.free = True

    def get_data(self):
        pass

    def set_data(self, mem_id, data, next_block):
        self.free = False
        self.mem_id = mem_id
        self.data = data
        self.next_block = next_block



