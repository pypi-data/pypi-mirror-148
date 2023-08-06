from os.path import join
from tempfile import TemporaryDirectory, gettempdir
from unittest import TestCase

from topiq._topic_reader import _TopicReader
from topiq._topic_writer import _TopicWriter
from topiq.message import Message
from topiq.message_type import MessageType


class TopicTest(TestCase):

    def setUp(self):
        self.temporary_folder = TemporaryDirectory()
        message = Message(MessageType.BYTES, b'\x01')
        self.topic_file_path = join(self.temporary_folder.name, 'topic1.et')
        with open(self.topic_file_path, 'wb') as writer:
            writer.write(message.to_bytes())

    def tearDown(self):
        self.temporary_folder.cleanup()

    def test_reader(self):
        _topic_reader = _TopicReader(topic_file_path=self.topic_file_path)
        self.assertIsNotNone(_topic_reader)

    def test_writer(self):
        with open(self.topic_file_path, 'wb') as writer:
            writer.truncate()
        _topic_writer = _TopicWriter(topic_file_path=self.topic_file_path)
        self.assertIsNotNone(_topic_writer)
