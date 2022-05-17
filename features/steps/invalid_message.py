def test_that_consume_on_invalid_message_does_moves_message_to_dead_letter_queue(self):
    # publish a message
    self.channel.basic_publish(
        exchange='',
        routing_key=self.queue_name,
        body="dummymessage"
    )

    res = self.create_queue(self.queue_name, True)
    self.assertEqual(res.method.message_count, 1)

    message_callback = MagicMock(return_value=False)

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

    # assert that the message is not in the dead-letters-queue
    res = self.channel.queue_declare(queue=self.queue_name_dead_letters, passive=True)
    self.assertEqual(res.method.message_count, 1)

    message_callback.assert_called_once()

    # stop the consumer
    consumer.join()