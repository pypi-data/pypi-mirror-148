from asyncio import get_event_loop, new_event_loop
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Event
from os.path import join
from threading import Thread
from time import sleep
from typing import Type

from lxg import Loggable

from ._topic_event import _TopicEvent
from ._topic_reader import _TopicReader
from ._topic_writer import _TopicWriter
from .message import Message
from .partition import Partition


class Topic(Loggable):

    def __init__(self, topic_name: str, worker_class: Type, concurrency: int = 1):
        self.worker_class = worker_class
        self.topic_name = topic_name
        self.concurrency = concurrency
        self._topic_reader = None
        self._topic_writer = None
        self.thread = None

    async def initialize(self, topic_data_folder: str):
        self._topic_reader = _TopicReader(
            join(topic_data_folder, f'{self.topic_name}.et'),
            _TopicEvent()
        )
        self._topic_writer = _TopicWriter(
            join(topic_data_folder, f'{self.topic_name}.et'))

        # Only one partition for concurrency level 1
        if self.thread is None:
            thread = Thread(
                target=self.run, args=())
            thread.daemon = True
            thread.start()

    async def send(self, message: Message):
        self.debug('send message')
        offset = self._topic_writer.write(message.to_bytes())
        await self._topic_reader.change_offset_event(offset)

    def run(self):
        executor = ThreadPoolExecutor(
            max_workers=self.concurrency,
        )

        for i in range(0, self.concurrency):
            executor.submit(Partition(self.worker_class,
                            self._topic_reader, i + 1).run)
