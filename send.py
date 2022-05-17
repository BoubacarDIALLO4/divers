##!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='Test')

channel.basic_publish(exchange='camera_input',
                      routing_key='',
                      body="112333")
print(" [x] Sent 'Hello World!'")
connection.close()