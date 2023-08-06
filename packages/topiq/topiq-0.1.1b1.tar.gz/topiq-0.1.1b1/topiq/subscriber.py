from .message import Message
from .message_type import MessageType
from .topic import Topic


class Subscriber:

    def __init__(self, topic: Topic):
        self.topic = topic

    async def send_int_message(self, value: int):
        await self.topic.send(Message.from_int(value))

    def close(self):
        ...
