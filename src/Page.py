#!/usr/bin/env python
# -*- coding: utf-8

class Page:
    """
    Atrributes
    """

    size_available = 0
    size_used = 0
    total_capacity = 0

    # stored as bytes
    data = ""

    '''
    Methods
    '''

    # Constructor
    def __init__(self, total_capacity):
        self.total_capacity = total_capacity
        pass

    def put_data(self, data):
        self.data = data

    def get_data(self):
        return self.data.buffer




