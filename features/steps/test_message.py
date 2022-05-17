def test_that_consume_on_failure_message_does_reschedule_the_message(self):
    # publish a message
    self.channel.basic_publish(
        exchange='',
        routing_key=self.queue_name,
        body="dummymessage"
    )

    res = self.create_queue(self.queue_name, True)
    self.assertEqual(res.method.message_count, 1)

    message_callback = MagicMock(side_effect=Exception("Failed to process message"))

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

    # stop the consumer
    consumer.join()

    # assert that the message is still in the queue
    res = self.channel.queue_declare(queue=self.queue_name, passive=True)
    self.assertEqual(res.method.message_count, 1)

    # since the message is rescheduled it might be processed many times before we stop the consumer
    message_callback.assert_called()