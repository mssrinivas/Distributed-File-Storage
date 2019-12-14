#!/usr/bin/env python
# -*- coding: utf-8
import math
import time

from src.Page import Page
from src.SpaceBinaryTree import SpaceBinaryTree


class MemoryManager:
    '''
    Atrributes
    '''

    memory_tracker = {}  # key: memory_hash_id, value: list_of_pages_ids>
    list_of_all_pages = []
    total_number_of_pages = 0
    total_memory_size = 0
    page_size = 0
    list_of_pages_used = []
    fragmentation_threshold = 0
    pages_free = None

    '''
    Methods
    '''

    # Constructor
    def __init__(self, total_memory_size, page_size):
        # define the attributes
        self.total_memory_size = total_memory_size
        self.page_size = page_size

        self.total_number_of_pages = math.floor(self.total_memory_size / self.page_size)

        for i in range(self.total_number_of_pages):
            self.list_of_all_pages.append(Page(self.page_size))

        self.pages_free = SpaceBinaryTree(self.total_memory_size, self.total_number_of_pages)
        print("[MemoryManager] Number of pages available in memory %s of size %s bytes." % (len(self.list_of_all_pages),
                                                                                           self.page_size))

    # def put_data(self, memory_id, data_chunks, num_of_chunks):
    def put_data(self, data_chunks, hash_id, number_of_chunks, is_single_chunk):
        '''
        :param data_chunks:
        :param hash_id:
        :param chunk_size:
        :param data_size:
        :return:
        '''

        if hash_id in self.memory_tracker:
            print("[MemoryManager] The following hash_id exist and it will be overwritten: %s." % hash_id)
            # delete data associated this this hash_id before we save the new one
            self.delete_data(hash_id)
        else:
            print("\n[MemoryManager] Writing new data with hash_id: %s." % hash_id)

        pages_needed = number_of_chunks #self.get_number_of_pages_needed(chunk_size, number_of_chunks)
        # find available blocks of pages to save the data
        target_list_indexes = self.find_n_available_pages(pages_needed)
        #print("[MemoryManager] Number of Pages requested = {}".format(pages_needed))
        #print("[MemoryManager] List of pages that it got = {}, Number of pages received = {}".format(len(target_list_indexes), len(target_list_indexes)))
        start_write_data = time.time()

        # save the data in pages
        index_counter = 0
        if not is_single_chunk:
            for c in data_chunks:
                self.list_of_all_pages[target_list_indexes[index_counter]].put_data(c)
                index_counter = index_counter + 1
        else:
            self.list_of_all_pages[target_list_indexes[index_counter]].put_data(data_chunks)
            index_counter = index_counter + 1

        total_time_write_data = round(time.time() - start_write_data, 6)

        assert index_counter == pages_needed  # make sure we use all the pages we needed

        # update the list with used pages
        self.list_of_pages_used.extend(target_list_indexes)
        # update memory dic
        self.memory_tracker[hash_id] = target_list_indexes
        print("[MemoryManager] Successfully saved the data in %s pages. Bytes written: %s. Took %s seconds." %
              (pages_needed, pages_needed * self.page_size, total_time_write_data))
        print("[MemoryManager] Free pages left: %s. Bytes left: %s" % (self.get_number_of_pages_available(), self.get_available_memory_bytes()))
        return True

    # def get_number_of_pages_needed(self, chunk_size, data_size):
    #     if self.page_size != chunk_size:
    #         message = "[MemoryManager] Page set in the server is different than the chunk size specified. Please send the data with " \
    #                   "the correct chunk from the client side. This will be supported in the future."
    #         raise Exception(message)
    #     else:
    #         return math.ceil(data_size / chunk_size)  # taking ceiling to account for last page being partially occupied

    def get_number_of_pages_available(self):
        return self.total_number_of_pages - len(self.list_of_pages_used)

    def get_available_memory_bytes(self):
        return self.get_number_of_pages_available() * self.page_size

    def get_data(self, hash_id):
        '''
        :param hash_id:
        :return:
        '''

        pages_to_return = []

        data_pages = self.memory_tracker[hash_id]
        start_read_data = time.time()

        for index in data_pages:
            pages_to_return.append(self.list_of_all_pages[index].get_data())

        total_time_read_data = round(time.time() - start_read_data, 6)

        print("[MemoryManager] Returning: data for %s composed of %s pages. Took %s sec" %
              (hash_id, str(len(pages_to_return)), total_time_read_data))

        return pages_to_return

    def update_data(self, data, memory_id):
        '''
        :param data:
        :param memory_id:
        :return:
        '''
        # TODO
        pass

    # this function is very slow, we need to improve it. (This will use a tree)
    def find_n_available_pages(self, n):
        start = time.time()

        print("[MemoryManager] Looking for %s available pages... " % n)
        list_indexes_to_used = []

        list_indexes_to_used = self.pages_free.get_available_space(n)
        # for i in range(0, len(self.list_of_all_pages)):
        #     if i not in self.list_of_pages_used:
        #         list_indexes_to_used.append(i)
        #         if len(list_indexes_to_used) == n:
        #             break
        #
        total_time = round(time.time() - start, 6)

        if len(list_indexes_to_used) != n:
            raise Exception("[MemoryManager] Not enough pages available to save the data. Took %s seconds." % total_time)
        else:
            print("[MemoryManager] Enough pages available to save the data. Took %s seconds." % total_time)

        return list_indexes_to_used

    def delete_data(self, hash_id):
        '''
        :param hash_id:
        :return:
        '''

        old_pages_list = self.memory_tracker[hash_id]
        del self.memory_tracker[hash_id]  # delete the mapping
        self.list_of_pages_used = [x for x in self.list_of_pages_used if x not in old_pages_list]

        # we may also need to delete the data from the actual Pages() in list_of_all_pages
        print("[MemoryManager] Successfully deleted hash_id: %s." % hash_id)

    def get_stored_hashes_list(self):
        return list(self.memory_tracker.keys())

    def hash_id_exists(self, hash_id):
        if hash_id in self.memory_tracker:
            return True
        else:
            return False

    def defragment_data(self):
        '''
        :param data:
        :param list_of_pages:
        :return:
        '''
        # TODO
        pass

    def partition_data(self, data, list_of_pages):
        '''
        :param data:
        :param list_of_pages:
        :return:
        '''
        # TODO
        pass

    def update_binary_tree(self):
        '''
        :return:
        '''
        # TODO
        pass
