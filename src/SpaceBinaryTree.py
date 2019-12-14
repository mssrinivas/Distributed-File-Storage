#!/usr/bin/env python
# -*- coding: utf-8
from src.TreeNode import TreeNode
from sortedcontainers import SortedDict

class SpaceBinaryTree:
    '''
    Atrributes
    '''

    head = None
    sorted_dict = None


    '''
    Methods
    '''

    # Constructor
    def __init__(self, size, free_pages):
        # define the attributes
        free_pages = [x for x in range(free_pages)]
        self.head = TreeNode(node_left=None, node_right=None, size=size, free_pages=free_pages)
        self.sorted_dict = SortedDict({size: TreeNode(node_left=None,
                                                      node_right=None,
                                                      size=size,
                                                      free_pages=[[free_pages]])})

    def set_empty_space(self, num_of_slots, free_pages):
        if self.sorted_dict.get(num_of_slots):
            self.sorted_dict.get(num_of_slots).set_free_pages(free_pages)
        # If the key does not exist, then we create a new node and add
        # the list to a new node
        else:
            self.sorted_dict[num_of_slots] = TreeNode(node_left=None,
                                                       node_right=None,
                                                       size=num_of_slots,
                                                       free_pages=[[free_pages]])

    # else:
    # print("Index Error, the node has no list remaining")



    def get_available_space(self, number_of_chunks):
        #number of spaces is available in sorted dict
        '''
        :param number_of_chunks:
        :return:
        '''

        '''
        The data structure can find the exact number of pages requested
        if it does find a spot that fits, it can allocate that space
        '''
        print("[SpaceBinaryTree] Number of chunks needed = {}".format(number_of_chunks))
        #print("[SpaceBinaryTree] resultado del if = {}".format(self.sorted_dict.get(number_of_chunks)))
        if self.sorted_dict.get(number_of_chunks):
            print("[SpaceBinaryTree] inside if number of chunks matches available")
            ret_list = self.sorted_dict.get(number_of_chunks).free_pages.pop(0)
            return ret_list
        else:
            '''
            Either the chunck is largest or smallest than the chunks available.
            '''
            try:
                #print("[SpaceBinaryTree] chunks needed are not found in list, has to be built")
                # Get the largest space available from sorted dict
                largest_chuck = self.sorted_dict.keys()[-1]
                #print("[SpaceBinaryTree] largest chunk is = {}".format(largest_chuck))
                # Find if the number of chunks needed is lower than the largest available
                if number_of_chunks < largest_chuck:
                    # if it is, we need to take one of those chunks and break it down
                    #first we get the whole node out of the sorted dict
                    temp_node = self.sorted_dict.pop(largest_chuck)
                    #print("[SpaceBinaryTree] Temp node popped out of list = {}".format(temp_node.get_size()))
                    #find if the node free pages list is not empty
                    #print("[SpaceBinaryTree] Temp node is empty = {}".format(temp_node.is_node_empty()))
                    if not temp_node.is_node_empty():
                        # pop the first list of pages available in the free_pages list.
                        # remember that free pages is a list if list of pages
                        # The structure is to be able to keep list of pages that are the same size under
                        # a single dictionary with key number of free pages
                        #print("[spaceBinaryTree] inside the not empty node")
                        # temp_node.print_free_pages()
                        temp_list = temp_node.get_free_pages()
                        #print("[SpaceBinaryTree] Temp list is = {}".format(len(temp_list)))
                        # Once we have the new list, we need to split it into the pages
                        # needed nad the remaining ones.
                        ret_list = temp_list[:number_of_chunks]
                        #print("Return list found = {}".format(len(ret_list)))
                        # Then we store the remaining list in an existing key
                        rem_list = temp_list[number_of_chunks:]
                        #print("Remaining list left = {}".format(len(rem_list)))
                        self.set_empty_space(len(rem_list), rem_list)
                        return ret_list
                    else:
                        err_message = "You got an empty node"
                        raise Exception(err_message)
                else:
                    # Get the smallest space available from sorted dict
                    smallest_chuck = self.sorted_dict.keys()[0]
                    # Take smallest pieces and get as many until enough chunks
                    # meet the chunks needed
                    temp_node = self.sorted_dict.pop(smallest_chuck)
                    #number of chunks is larger than largest spot available.
                    enough_pages = False
                    ret_list = []
                    free_pages_needed = number_of_chunks
                    ret_list = None
                    # We are going to start looking at the smallest set of page lists
                    # and we are going to add as many pages needed for the chunks to fit in
                    while not enough_pages:
                        # The list of pages is smaller than needed at this point
                        if free_pages_needed[0] > smallest_chuck:
                        # Cycle through all the pages in the node and try to fill the gap
                            for lp in self.sorted_dict.get(smallest_chuck).get_all_free_pages():
                                if free_pages_needed > len(lp):
                                    ret_list = ret_list + lp
                                    free_pages_needed = free_pages_needed - len(ret_list)

                                else:
                                    ret_list = ret_list + lp[:free_pages_needed]
                                    free_pages_left = free_pages_needed - len(ret_list)
                                    #if there are any pages left after the split
                                    if free_pages_left > 0:
                                        self.set_empty_space(len(free_pages_needed), lp[free_pages_needed:])

                                    enough_pages = True

                                if enough_pages == True:
                                    self.sorted_dict.pop[0]
                                    return ret_list
                                else:
                                    self.sorted_dict.pop(0)
                                    continue

            except Exception as e:
                print(str(e))
                raise






