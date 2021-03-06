import pika


class GenericConsumer(object):
    def __init__(self, channel, consume_queue_name, callback):
        self.channel = channel
        self.callback = callback

        self.properties = pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )

        self.channel.queue_declare(queue=consume_queue_name, durable=True)

        self.channel.basic_consume(self.on_message,
                                   queue=consume_queue_name,
                                   auto_ack=False)

        self.channel.start_consuming()

    def on_message(self, ch: pika.adapters.blocking_connection.BlockingChannel, method, properties, body):
        if self.callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # failed to handle message
            pass


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    def callback(ch, method, properties, body):
        print(body)
        return True

    consumer = GenericConsumer(connection.channel(), 'queue_name', callback)