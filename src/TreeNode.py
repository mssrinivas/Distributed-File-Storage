#!/usr/bin/env python
# -*- coding: utf-8

class TreeNode:
    node_left = None
    node_right= None
    size = 0
    free_pages = []

    def __init__(self, node_left=None, node_right=None, size=0, free_pages=[]):
        self.node_left = node_left
        self.node_right = node_right
        self.size = size
        self.free_pages = free_pages

    def insert_left_node(self, node):
        self.node_left = node

    def insert_right_node(self, node):
        self.node_right = node

    def set_size(self, size):
        self.size = size

    def set_free_pages(self, pages):
        self.free_pages.append(pages)

    def get_left_node(self):
        return self.node_left

    def get_right_node(self):
        return self.node_right

    def get_size(self):
        return self.size;

    def get_all_free_pages(self):
        return self.free_pages

    def get_free_pages(self):
        if self.is_node_empty():
            return []
        else:
            ret_val = self.free_pages.pop()[0]
            return ret_val

    def is_node_empty(self):
        if self.free_pages == []:
            return True
        else:
            return False

    def print_free_pages(self):
        max_numbers = 5
        for i, set_of_pages in enumerate(self.free_pages):
            if isinstance(set_of_pages, list):
                temp_list = []
                for j, element in enumerate(set_of_pages):
                    temp_list.append(element)
                    if j > max_numbers:
                        break
                print("[TreeNode] list {}: {}".format(i, temp_list))
