from os.path import join
from tempfile import TemporaryDirectory, gettempdir
from unittest import TestCase

from topiq import Message, MessageType, Subscriber, Topic


class Worker:

    def __init__(self, message: Message):
        self.message = message

    async def run(self):
        id = self.message.as_int()
        ...


class SubsriberTest(TestCase):

    def setUp(self):
        self.temporary_folder = TemporaryDirectory()
        message = Message(MessageType.BYTES, b'\x01')
        self.topic_file_path = join(self.temporary_folder.name, 'topic1.et')
        with open(self.topic_file_path, 'wb') as writer:
            writer.write(message.to_bytes())

    def tearDown(self):
        self.temporary_folder.cleanup()

    async def test_subscriber(self):
        subscriber = Subscriber(Topic('name'), Worker)
        await subscriber.send_int_message(1)
        self.assertIsNotNone(subscriber)
