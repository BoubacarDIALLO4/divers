def wait_for_log_contains(self, text, level='info'):
    timeout = 1
    max_tries = 5
    while max_tries is not 0:
        if any(text in s for s in self.consumer_log_messages[level]):
            return True

        import time
        time.sleep(timeout)
        max_tries -= 1

    self.fail("Log message was not found %s" % text)