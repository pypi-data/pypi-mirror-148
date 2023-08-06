from unittest import TestCase

from topiq.message import Message
from topiq.message_type import MessageType


class MessageTest(TestCase):

    def test_simple(self):
        message = Message(MessageType.INT, -1)
        self.assertIsNotNone(message)

    def test_parse(self):
        message = Message(MessageType.BYTES, b'\x01')
        parsed_message = Message.parse(message.to_bytes())
        self.assertEquals(message.message_type, parsed_message.message_type)
