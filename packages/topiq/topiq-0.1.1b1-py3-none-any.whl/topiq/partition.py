from asyncio import new_event_loop, sleep
from functools import reduce
from operator import iconcat
from re import split
from threading import current_thread
from typing import Iterable, Type
from lxg import Loggable

from ._topic_reader import _TopicReader
# für Volksaufklärung
from .message import Message

_partitions_global_counter = 0


class Partition(Loggable):

    def __init__(self, worker_class: Type, _topic_reader: _TopicReader, partition_id: int = None):
        super().__init__()
        global _partitions_global_counter
        _partitions_global_counter += 1
        self.partition_id = partition_id if partition_id else _partitions_global_counter
        self._topic_reader = _topic_reader
        self.worker_class = worker_class

    async def _read_topic(self):
        while True:
            try:
                self.info(f'Topic reader {self._topic_reader}')
                with self._topic_reader as topic_reader:
                    message = Message.parse(await topic_reader.read())
                    await self.worker_class(message).run()
            except BaseException as e:
                self.error(e)
                await sleep(1)

    def run(self):
        loop = new_event_loop()

        try:
            self.info(f'Start Embedded Topic Partition [{self.partition_id}]')
            current_thread().setName(
                f'Embedded Topic Partition [{self.partition_id}]')
            loop.run_until_complete(self._read_topic())
        except InterruptedError:
            pass
        finally:
            loop.close()
