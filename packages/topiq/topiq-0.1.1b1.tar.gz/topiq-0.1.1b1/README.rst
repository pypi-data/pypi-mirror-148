Lightweigt embedded topics (based on kafka ideas)
=================================================

The sample:

.. code:: python

    from topiq import Message, Subscriber, Topic


    class Worker:

        def __init__(self, message: Message):
            self.message = message

        async def run(self):
            id = self.message.as_int()
            ...


    # Test subscriber
    async def test_subscriber(self):
        subscriber = Subscriber(Topic('name'), Worker)
        await subscriber.send_int_message(1)
