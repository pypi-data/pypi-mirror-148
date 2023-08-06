from enum import Enum
from typing import Any


class MessageType(Enum):
    BYTES = 65
    INT = 73
    STR = 83
    FLOAT = 70
    BOOL = 66

    @staticmethod
    def to_bytes(message_type) -> bytes:
        return int(message_type.value).to_bytes(1, 'big')

    @staticmethod
    def from_bytes(message_type: bytes) -> Any:
        value = int.from_bytes(message_type, 'big')
        if MessageType.BYTES.value == value:
            return MessageType.BYTES
        if MessageType.INT.value == value:
            return MessageType.INT
        if MessageType.STR.value == value:
            return MessageType.STR
        if MessageType.FLOAT.value == value:
            return MessageType.FLOAT
        if MessageType.BOOL.value == value:
            return MessageType.BOOL
        return None
