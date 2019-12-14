#!/usr/bin/env python
# -*- coding: utf-8
from libs.storage import MemoryManager

FULL_MEMORY = 2
MEM_TABLE_CORRUPTED = 3


# def on_open(connection)
#
#
#
# conection = pika.SelectConnection(on_open_callback=on_open)





def main():
    """ Main program """
    # try:
        # conection.ioloop.start()
    # # Create a server
    # '''create a new instance of the connection object'''
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    #
    # '''
    # Create a new channel with the next available channel number or pass in a
    # channel number to use
    # '''
    # channel = connection.channel()
    #
    # '''
    # Declare queue, create if needed. This method creates or checks a queue.
    # When creating a new queue the client can specify various properties that
    # control the durability of the queue and its contents, and the level of
    # sharing for the queue.
    # '''
    # channel.queue_declare(queue='hello')
    # channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    # print("[x] Sent 'Hello World!'")
    # connection.close()

    #Handle server data
    mem = MemoryManager(1, 10)
    data = {"something": 1, "else":2}
    mem.set_memory_block(data)
    # pp(dir(mem))
    # except:
    #     conection.close()
    #     conection.ioloop.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error = e.args
        if error == FULL_MEMORY:
            print("error full memory: " + str(e))
        elif error == MEM_TABLE_CORRUPTED:
            print("error mem corrupted: " + str(e))
        else:
            print("unknown error: " + str(e))
