from io import BufferedIOBase
from mmap import ACCESS_READ, ACCESS_WRITE, mmap
from os import chmod, stat
from os.path import exists

DEFAULT_NEXT_BLOCK_SIZE = 65535


def _truncate_to(file_path: str, new_file_size: int):
    with open(file_path, 'a') as writer:
        writer.truncate(new_file_size)


def _get_stop_offset_and_truncate(file_path):
    file_size = stat(file_path).st_size if exists(file_path) else 0
    if file_size < DEFAULT_NEXT_BLOCK_SIZE:
        _truncate_to(file_path, DEFAULT_NEXT_BLOCK_SIZE)
    with open(file_path, 'r+') as reader:
        offset = 0
        buffer = reader.buffer.read(8)
        payload_length = int.from_bytes(buffer, 'big')
        if (payload_length < 8):
            return 0
        while payload_length > 8 and payload_length < file_size:
            offset += payload_length
            reader.seek(payload_length - 8)
            buffer = reader.buffer.read(8)
            payload_length = int.from_bytes(buffer, 'big')
        return offset
