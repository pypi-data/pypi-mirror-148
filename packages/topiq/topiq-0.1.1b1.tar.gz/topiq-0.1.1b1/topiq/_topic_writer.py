from io import BufferedIOBase
from mmap import ACCESS_READ, ACCESS_WRITE, mmap
from os import chmod, stat
from os.path import exists
from lxg import Loggable

from ._topic_utils import _get_stop_offset_and_truncate

DEFAULT_TOPIC_FILE_LIMIT = 1073741824
DEFAULT_NEXT_BLOCK_SIZE = 65535


class _TopicWriter(Loggable):

    def __init__(self, topic_file_path: str, topic_file_size_limit: int = DEFAULT_TOPIC_FILE_LIMIT):
        self.topic_file_path: str = topic_file_path
        self.topic_file_size_limit: int = topic_file_size_limit
        self._stream: BufferedIOBase = None
        self._mmapio: mmap = None
        self._map_size = None
        self._offset = 0
        self._initial_size = 0  # Update on enter phase from file_size variable

    def _resize(self, new_map_size: int):
        if self._mmapio:
            self._mmapio.flush()
            self._mmapio.close()
        self._stream.truncate(new_map_size)
        self._mmapio = mmap(self._stream.fileno(),
                            length=0, access=ACCESS_WRITE)
        self._mmapio.seek(self._offset)

    def _init(self):
        self._offset = _get_stop_offset_and_truncate(self.topic_file_path)
        self._stream = open(self.topic_file_path, 'w+')
        chmod(self.topic_file_path, 0o777)
        self._map_size = (1 + self._offset //
                          DEFAULT_NEXT_BLOCK_SIZE) * DEFAULT_NEXT_BLOCK_SIZE
        self._resize(self._map_size)

    def __enter__(self):
        self._init()
        return self

    def __exit__(self, *args, **kwargs):
        try:
            self._mmapio.flush()
            self._mmapio.close()
            # self._stream.flush()
            # File size tune
            if (self._map_size - self._offset) < DEFAULT_NEXT_BLOCK_SIZE or \
                    self._offset == self._initial_size:
                self._stream.truncate(self._offset)
            self._stream.close()
        finally:
            if len(args) > 0 and isinstance(args[0], BaseException):
                raise args[0].with_traceback(args[1])
        return self

    def write(self, message: bytes) -> int:
        if not message:
            return
        if self._map_size is None:
            self._init()
        intented_length = self._offset + len(message)
        if intented_length > self.topic_file_size_limit:
            # Reset write position to the begin of the file
            self._mmapio.seek(0)
            self._offset = 0
        elif intented_length > self._map_size:
            self._map_size = (1 + intented_length //
                              DEFAULT_NEXT_BLOCK_SIZE) * DEFAULT_NEXT_BLOCK_SIZE
            self._resize(self._map_size)

        self._mmapio.write(message)

        result = self._offset
        self._offset += len(message)
        return result
