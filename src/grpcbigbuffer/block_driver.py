import json
import os.path
from typing import Union, List, Tuple, Dict, Generator

from grpcbigbuffer.validate_lengths_tree import validate_lengths_tree
from grpcbigbuffer.buffer_pb2 import Buffer
from grpcbigbuffer.utils import BLOCK_LENGTH, METADATA_FILE_NAME, WITHOUT_BLOCK_POINTERS_FILE_NAME, Enviroment, \
    create_lengths_tree, encode_bytes, get_varint_at_position, get_pruned_block_length


def compute_wbp_lengths(tree: Dict[int, Union[Dict, str]], file_list: List[str]) -> Dict[int, int]:
    def __rec_compute_wbp_lengths(_tree: Dict[int, Union[Dict, str]], _file_list: List[str]) \
            -> Dict[int, Tuple[int, int]]:  # Tuple is wbp length and augmented pruned length.
        lengths: Dict[int, Tuple[int, int]] = {}
        for key, value in _tree.items():
            position_length: int = get_varint_at_position(key, _file_list)
            if isinstance(value, Dict):
                pruned_length: int = 0
                for k, v in __rec_compute_wbp_lengths(
                        _tree=value,
                        _file_list=_file_list
                ).items():
                    pruned_length += v[1]
                    lengths[k] = (v[0], 0)

            else:
                pruned_length: int = get_pruned_block_length(value)

            if pruned_length > position_length:
                raise Exception("gRPCbb on block_driver compute_wbp_lengths method, "
                                "the pruned_length can't be greater than the real length.")
            lengths[key] = (
                position_length - pruned_length,
                pruned_length + len(encode_bytes(position_length)) - len(encode_bytes(position_length - pruned_length))
            )
        return lengths

    return {k: v[0] for k, v in __rec_compute_wbp_lengths(_tree=tree, _file_list=file_list).items()}


def set_varint_value(varint_pos: int, buffer: List[Union[bytes, str]], new_value: int):
    def __set_varint_value(_varint_pos: int, _buffer: bytes, _new_value: int) -> bytes:
        """
        Sets the value of the varint at the given position in the Protobuf buffer to the given value and returns
        the modified buffer.
        """
        # Convert the given value to a varint and store it in a bytes object
        varint_bytes = []
        while True:
            byte = _new_value & 0x7F
            _new_value >>= 7
            varint_bytes.append(byte | 0x80 if _new_value > 0 else byte)
            if _new_value == 0:
                break
        varint_bytes = bytes(varint_bytes)

        # Calculate the number of bytes to remove from the original varint
        original_varint_bytes = _buffer[_varint_pos:]
        original_varint_length = 0
        while (original_varint_bytes[original_varint_length] & 0x80) != 0:
            original_varint_length += 1
        original_varint_length += 1

        # Remove the original varint and append the new one
        return _buffer[:_varint_pos] + varint_bytes + _buffer[_varint_pos + original_varint_length:]

    """
    Modify the varint at the given position in the buffer which is composed by a list of bytes and binary files. 
    The position is based on the concatenation of all the bytes and binary files in the buffer.
    The function modify the buffer.
    """
    offset: int = 0
    for index, value in enumerate(buffer):
        if type(value) == bytes:
            obj_size = len(value)
            if offset <= varint_pos < offset + obj_size:
                buffer[index] = __set_varint_value(
                        _varint_pos=varint_pos-offset,
                        _buffer=value,
                        _new_value=new_value
                    )
                return
            offset += obj_size
        else:
            offset += os.path.getsize(value)

    raise Exception('gRPCbb block driver error on set varint value')


def regenerate_buffer(lengths: Dict[int, int], buffer: List[Union[bytes, str]]) -> Generator[bytes, None, None]:
    """
    Replace real lengths with wbp lengths.
    """
    for varint_pos, new_value in sorted(lengths.items(), key=lambda x: x[0], reverse=True):
        set_varint_value(
                varint_pos=varint_pos,
                buffer=buffer,
                new_value=new_value,
            )

    for b in buffer:
        if type(b) == bytes:
            yield b
        else:
            block_buff = Buffer.Block(
                hashes=[
                    Buffer.Block.Hash(
                        value=bytes.fromhex(str(b.split('/')[-1]))
                    )
                ]
            ).SerializeToString()
            if len(block_buff) != BLOCK_LENGTH:
                raise Exception("gRPCbb regenerate buffer method, incorrect block format.")
            yield block_buff


def generate_wbp_file(dirname: str):
    with open(dirname + '/' + METADATA_FILE_NAME, 'r') as f:
        _json: List[Union[
            int,
            List[str, List[int]]
        ]] = json.load(f)

    buffer: List[Union[bytes, str]] = []
    file_list: List[str] = []
    for e in _json:
        if type(e) == int:
            file_list.append(dirname + '/' + str(e))
            with open(dirname + '/' + str(e), 'rb') as file:
                buffer.append(file.read())
        else:
            if type(e) != list or type(e[0]) != str:
                raise Exception('gRPCbb: Invalid block on _.json file.')
            file_list.append(Enviroment.block_dir + e[0])
            buffer.append(Enviroment.block_dir + e[0])

    blocks: Dict[str, List[List[int]]] = {}
    for _t in _json:
        if type(_t) == list:
            if _t[0] not in blocks:
                blocks[_t[0]] = []
            blocks[_t[0]].append(_t[1])  # _t[1] is a List[int] always.

    if not validate_lengths_tree(blocks=blocks, file_list=file_list):
        exit()

    tree: Dict[int, Union[Dict, str]] = create_lengths_tree(blocks)

    recalculated_lengths: Dict[int, int] = compute_wbp_lengths(tree=tree, file_list=file_list)

    with open(dirname + '/' + WITHOUT_BLOCK_POINTERS_FILE_NAME, 'wb') as f:
        for c in regenerate_buffer(recalculated_lengths, buffer):
            f.write(c)
