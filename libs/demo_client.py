#!/usr/bin/env python
# -*- coding: utf-8

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    channel.basic_consume(callback, queue='hello', no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e