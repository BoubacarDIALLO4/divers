def test_that_consume_on_valid_message_are_consumed_from_the_queue(self):
    # publish a message
    self.channel.basic_publish(
        exchange='',
        routing_key=self.queue_name,
        body="dummymessage"
    )

    # see that the message is in the queue
    res = self.create_queue(self.queue_name, True)
    self.assertEqual(res.method.message_count, 1)

    # accept any message
    message_callback = MagicMock(return_value=True)

    consumer = BasicConsumer(self.rabbitmq_url,
                             self.queue_name,
                             self.queue_arguments,
                             message_callback
                             )
    # start consumer
    consumer.start()

    # wait for the consumer to be ready
    self.wait_for_log_contains(BasicConsumer.CONSUMER_READY)

    # wait for the consumer to signal that is has consumed a message
    self.wait_for_log_contains(BasicConsumer.CONSUMER_PROCESSED_MESSAGE)

    # assert that the queue is empty
    res = self.create_queue(self.queue_name, True)
    self.assertEqual(res.method.message_count, 0)

    message_callback.assert_called_once()

    # stop the consumer
    consumer.join()