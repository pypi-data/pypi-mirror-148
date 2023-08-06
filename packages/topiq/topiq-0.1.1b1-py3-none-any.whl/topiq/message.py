from struct import pack, unpack
from typing import Any

from .topic_error import TopicError
from .message_type import MessageType


class Message:

    def __init__(self, message_type: MessageType = None, payload: bytes = None):
        self.message_type: MessageType = message_type
        self.payload: bytes = payload

    def to_bytes(self) -> bytes:
        entry = MessageType.to_bytes(self.message_type) + self.payload
        message_length = len(entry) + 16
        return message_length.to_bytes(8, 'big') + entry + message_length.to_bytes(8, 'little')

    @staticmethod
    def parse(message: bytes) -> Any:
        if len(message) < 16:
            raise TopicError('Not valid message, length less then 16')
        message_length_option_one = int.from_bytes(message[:8], 'big')
        message_length_option_two = int.from_bytes(message[-8:], 'little')
        if message_length_option_one != message_length_option_two:
            raise TopicError(
                'Not valid message, lengths are different (big-endian from the start and little-endian from the end)')
        if len(message) == 16:
            return Message()
        message_type = MessageType.from_bytes(message[8:9])
        if not(message_type is None):
            return Message(message_type, message[9:len(message) - 8])
        raise TopicError('Not valid message, unknown message type')

    @staticmethod
    def from_bytes(payload: bytes) -> Any:
        return Message(MessageType.BYTES, payload)

    @staticmethod
    def from_int(payload: int) -> Any:
        return Message(MessageType.INT, int(payload).to_bytes(8, 'big', signed=True))

    @staticmethod
    def from_str(payload: str) -> Any:
        return Message(MessageType.STR, payload.encode('utf-8'))

    @staticmethod
    def from_float(payload: float) -> Any:
        return Message(MessageType.FLOAT, bytearray(pack('f', payload)))

    @staticmethod
    def from_bool(payload: bool) -> Any:
        return Message(MessageType.BOOL, bytearray(pack('f', payload)))

    def as_int(self) -> int:
        if self.message_type in { MessageType.INT, MessageType.FLOAT }:
            if self.message_type == MessageType.INT:
                return int.from_bytes(self.payload, 'big', signed=True)
            if self.message_type == MessageType.FLOAT:
                return int(unpack('f', self.payload))
        raise TopicError(f'Sorry, but I can\'t read not number message. Message type is {self.message_type}')
