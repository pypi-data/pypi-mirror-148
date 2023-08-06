from io import BufferedIOBase
from mmap import ACCESS_READ, ACCESS_WRITE, mmap
from os import stat
from os.path import exists
from typing import Optional

from lxg import Loggable

from ._topic_event import _TopicEvent
from ._topic_utils import _get_stop_offset_and_truncate


class _TopicReader(Loggable):

    def __init__(self, topic_file_path: str, offset_event: _TopicEvent = None, offset: int = 0):
        self.topic_file_path: str = topic_file_path
        self._stream: BufferedIOBase = None
        self._mmapio: mmap = None
        self._offset = offset
        self._offset_event = offset_event
        self._stop_offset = None

    def __enter__(self):
        try:
            self._stop_offset = _get_stop_offset_and_truncate(
                self.topic_file_path)
            self._stream = open(self.topic_file_path, 'r+')
            self._mmapio = mmap(self._stream.fileno(),
                                length=0, access=ACCESS_READ)
            self._mmapio.seek(self._offset)
            return self
        except BaseException as e:
            self.error(e)
            self.info(f'Topic file path {self.topic_file_path}')
            raise e

    def __exit__(self, *args, **kwargs):
        try:
            self._mmapio.close()
            self._stream.close()
        except BaseException as e:
            self.error(e)
            raise e
        finally:
            if len(args) > 0 and isinstance(args[0], BaseException):
                raise args[0].with_traceback(args[1])
        return self

    async def change_offset_event(self, offset: int):
        self._offset = offset
        self._offset_event.set()

    async def read_the_message(self, offset: int):
        self.info('read the message')
        
        # READ 8 BYTES
        self._mmapio.seek(offset)
        buffer = self._mmapio.read(8)
        payload_length = int.from_bytes(buffer, 'big')
        if payload_length > 8:
            return buffer + self._mmapio.read(payload_length - 8)
        return None

    async def read(self) -> Optional[bytes]:

        if self._stop_offset and self._offset < self._stop_offset:
            message = await self.read_the_message(self._offset)
            self._offset += len(message)
            return message

        await self._offset_event.async_wait()
        self._offset_event.clear()
        
        message = await self.read_the_message(self._offset)
        self._offset += len(message)
        return message
