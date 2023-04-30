
# encoding: UTF-8

# Copyright 2016 Ivan Babintsev <alon.sage@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import struct


class InvalidMarkError(RuntimeError):
    pass


class BufferOverflowError(RuntimeError):
    pass


class BufferUnderflowError(RuntimeError):
    pass




def load_stream(data_str):
    data_list = []
    for i in range(0, len(data_str)-1, 2):
        tmp_str = f"0x{data_str[i]}{data_str[i + 1]}"
        tmp_int = int(tmp_str, 16)
        tmp_hex = hex(tmp_int)
        #print(f'{tmp_str} -> {tmp_int} -> {tmp_hex}')
        data_list.append(tmp_int)
    buff = ReadContext(bytearray(data_list),0,len(data_list))
    return buff

def load_bytearray(data_str):
    data_list = []
    for i in range(0, len(data_str)-1, 2):
        tmp_str = f"0x{data_str[i]}{data_str[i + 1]}"
        tmp_int = int(tmp_str, 16)
        tmp_hex = hex(tmp_int)
        #print(f'{tmp_str} -> {tmp_int} -> {tmp_hex}')
        data_list.append(tmp_int)
    buff = bytearray(data_list)
    return buff


def h2BFl32(hex):
    buff = load_stream(hex)
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    data = buff.get_BFloat32()
    try:
        data = buff.get_BFloat32()
    except:
        pass


def h2LFl32(hex):
    buff = load_stream(hex)
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    data = buff.get_LFloat32()
    try:
        data = buff.get_LFloat32()
    except:
        pass


def h2UBi32(hex):
    buff = load_stream(hex)
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    data =  buff.get_UBInt32()
    try:
        data = buff.get_UBInt32()
    except:
        pass

    return data
def h2SBi32(hex):
    buff = load_stream(hex)
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    data = buff.get_SBInt32()
    try:
        data = buff.get_SBInt32()
    except:
        pass

    return data
def h2UBi64(hex):
    buff = load_stream(hex)
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    #buff.get_UBInt32()

    return buff.get_UBInt64()

def h2SBi64(hex):
    buff = load_stream(hex)
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    #buff.get_UBInt32()

    return buff.get_SBInt64()


def h2ULi32(hex):
    buff = load_stream(hex)
    data = buff.get_ULInt32()
    try:
        data = buff.get_ULInt32()
    except:
        pass

    return data

def h2SLi32(hex):
    buff = load_stream(hex)
    data = buff.get_SLInt32()
    try:
        data = buff.get_SLInt32()
    except:
        pass

    return data

def h2ULi64(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_ULInt64()

def h2SLi64(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_SLInt64()
def h2ULi16(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_ULInt16()

def h2SLi16(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_SLInt16()

def h2UBi16(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_UBInt16()

def h2SBi16(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_SBInt16()

def h2ULi8(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_ULInt8()

def h2SLi8(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_SLInt8()

def h2UBi8(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_UBInt8()

def h2SBi8(hex):
    buff = load_stream(hex)
    #buff.get_ULInt32()
    # tmp_value = round((tmp_list.get_UBInt64() / (1000 * 1000 * 1000)))
    return buff.get_SBInt8()


def nsTOms(ns):
    return  round(ns / 1000000)

def nsTOs(ns):
    return round((ns / 1000000) / 1000)
def nsTos_v2(ns):
    return round(ns / 1e9)

def recv_timeout(the_socket,timeout=2):
    the_socket.setblocking(1)
    total_data=[];data='';begin=time.time()
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break
        try:
            data=the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)

End='something useable as an end marker'




def get_minutes(b):
    string = ""
    temp = b[-2:]
    temp = int(temp, 16)
    return str(temp)





class ByteBuffer(object):
    @classmethod
    def allocate(cls, capacity):
        if capacity < 0:
            raise ValueError('Negative buffer capacity')

        return cls(bytearray(capacity), 0, capacity)

    @classmethod
    def wrap(cls, array, offset=0, length=None):
        if not isinstance(array, bytearray):
            raise TypeError('Can wrap only bytearray')

        array_len = len(array)

        if not (0 <= offset <= array_len):
            raise ValueError('Offset out of range')

        if length is None:
            length = array_len - offset
        else:
            if not (0 <= length <= array_len - offset):
                raise ValueError('Length out of range')

        return cls(array, offset, length)

    def __init__(self, array, offset, length):
        self._array = array
        self._offset = offset
        self._length = length

        self._position = 0
        self._limit = length
        self._mark = None

    def get_capacity(self):
        return self._length

    def has_remaining(self):
        return self._limit > self._position

    def get_remaining(self):
        return self._limit - self._position

    def get_position(self):
        return self._position

    def set_position(self, value):
        if not (0 <= value <= self._limit):
            raise ValueError('Position out of range')

        self._position = value

        if self._mark is not None and self._mark > value:
            self._mark = None

    def get_limit(self):
        return self._limit

    def set_limit(self, value):
        if not (0 <= value <= self._length):
            raise ValueError('Limit out of range')

        self._limit = value

        if self._position > value:
            self._position = value

        if self._mark is not None and self._mark > value:
            self._mark = None

    def mark(self):
        self._mark = self._position

    def reset(self):
        if self._mark is None:
            raise InvalidMarkError('No mark was defined')

        self._position = self._mark

    def clear(self):
        self._position = 0
        self._limit = self._length
        self._mark = None

    def flip(self):
        self._limit = self._position
        self._position = 0
        self._mark = None

    def rewind(self):
        self._position = 0
        self._mark = None

    def compact(self):
        length = self._limit - self._position

        if length:
            self._array[0:length] = self._array[self._position:self._position + length]

        self._position = length
        self._limit = self._length
        self._mark = None

    def put(self, array, offset=0, length=None):
        if not isinstance(array, bytearray):
            raise TypeError('Can put only bytearray')

        array_len = len(array)

        if not (0 <= offset <= array_len):
            raise ValueError('Offset out of range')

        if length is None:
            length = array_len - offset
        else:
            if not (0 <= length <= array_len - offset):
                raise ValueError('Length out of range')

        if length > self._limit - self._position:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += length
        self._array[dst_offset:dst_offset + length] = array[offset:offset + length]

        return length

    def get(self, array, offset=0, length=None):
        if not isinstance(array, bytearray):
            raise TypeError('Can get only to bytearray')

        array_len = len(array)

        if not (0 <= offset <= array_len):
            raise ValueError('Offset out of range')

        if length is None:
            length = array_len - offset
        else:
            if not (0 <= length <= array_len - offset):
                raise ValueError('Length out of range')

        if length > self._limit - self._position:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += length
        array[offset:offset + length] = self._array[src_offset:src_offset + length]

        return length

    def put_buffer(self, buffer):
        if not isinstance(buffer, ByteBuffer):
            raise TypeError('Expected argument of ByteBuffer type')

        length = buffer._limit - buffer._position

        if length > self._limit - self._position:
            raise BufferOverflowError('Too many data to put')

        src_offset = buffer._offset + buffer._position
        dst_offset = self._offset + self._position
        buffer._position += length
        self._position += length
        self._array[dst_offset:dst_offset + length] = buffer._array[src_offset:src_offset + length]

        return length

    def put_bytes(self, array, offset=0, length=None):
        if not isinstance(array, bytes):
            raise TypeError('Can put only bytes')

        array_len = len(array)

        if not (0 <= offset <= array_len):
            raise ValueError('Offset out of range')

        if length is None:
            length = array_len - offset
        else:
            if not (0 <= length <= array_len - offset):
                raise ValueError('Length out of range')

        if length > self._limit - self._position:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += length
        self._array[dst_offset:dst_offset + length] = array[offset:offset + length]

        return length

    def get_bytes(self, length=None):
        if length is None:
            length = self._limit - self._position
        else:
            if length < 0:
                raise ValueError('Length out of range')

        if length > self._limit - self._position:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += length
        return bytes(self._array[src_offset:src_offset + length])

    def get_time4(self):
        if self._limit - self._position < 1:
            raise BufferOverflowError('Too many data to put')
        src_offset = self._offset + self._position
        self._position += 1
        return self._array.hex()[src_offset:2]

    def put_SBInt4(self, value):
        if self._limit - self._position < 1:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 1
        struct.pack_into('>b', self._array, dst_offset, value)

    def get_SBInt4(self):
        if self._limit - self._position < 1:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 1
        return struct.unpack_from('>b', self._array, src_offset)[0]


    def put_SBInt8(self, value):
        if self._limit - self._position < 1:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 1
        struct.pack_into('>b', self._array, dst_offset, value)

    def get_SBInt8(self):
        if self._limit - self._position < 1:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 1
        return struct.unpack_from('>b', self._array, src_offset)[0]

    def put_UBInt8(self, value):
        if self._limit - self._position < 1:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 1
        struct.pack_into('>B', self._array, dst_offset, value)

    def get_UBInt8(self):
        if self._limit - self._position < 1:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 1
        return struct.unpack_from('>B', self._array, src_offset)[0]

    def put_SLInt8(self, value):
        if self._limit - self._position < 1:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 1
        struct.pack_into('<b', self._array, dst_offset, value)

    def get_SLInt8(self):
        if self._limit - self._position < 1:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 1
        return struct.unpack_from('<b', self._array, src_offset)[0]

    def put_ULInt8(self, value):
        if self._limit - self._position < 1:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 1
        struct.pack_into('<B', self._array, dst_offset, value)

    def get_ULInt8(self):
        if self._limit - self._position < 1:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 1
        return struct.unpack_from('<B', self._array, src_offset)[0]

    def put_SBInt16(self, value):
        if self._limit - self._position < 2:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 2
        struct.pack_into('>h', self._array, dst_offset, value)

    def get_SBInt16(self):
        if self._limit - self._position < 2:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 2
        return struct.unpack_from('>h', self._array, src_offset)[0]

    def put_UBInt16(self, value):
        if self._limit - self._position < 2:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 2
        struct.pack_into('>H', self._array, dst_offset, value)

    def get_UBInt16(self):
        if self._limit - self._position < 2:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 2
        return struct.unpack_from('>H', self._array, src_offset)[0]

    def put_SLInt16(self, value):
        if self._limit - self._position < 2:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 2
        struct.pack_into('<h', self._array, dst_offset, value)

    def get_SLInt16(self):
        if self._limit - self._position < 2:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 2
        return struct.unpack_from('<h', self._array, src_offset)[0]

    def put_ULInt16(self, value):
        if self._limit - self._position < 2:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 2
        struct.pack_into('<H', self._array, dst_offset, value)

    def get_ULInt16(self):
        if self._limit - self._position < 2:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 2
        return struct.unpack_from('<H', self._array, src_offset)[0]

    def put_SBInt32(self, value):
        if self._limit - self._position < 4:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 4
        struct.pack_into('>i', self._array, dst_offset, value)

    def get_SBInt32(self):
        if self._limit - self._position < 4:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 4
        return struct.unpack_from('>i', self._array, src_offset)[0]

    def put_UBInt32(self, value):
        if self._limit - self._position < 4:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 4
        struct.pack_into('>I', self._array, dst_offset, value)

    def get_UBInt32(self):
        if self._limit - self._position < 4:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 4
        return struct.unpack_from('>I', self._array, src_offset)[0]

    def put_SLInt32(self, value):
        if self._limit - self._position < 4:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 4
        struct.pack_into('<i', self._array, dst_offset, value)

    def get_SLInt32(self):
        if self._limit - self._position < 4:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 4
        return struct.unpack_from('<i', self._array, src_offset)[0]

    def put_ULInt32(self, value):
        if self._limit - self._position < 4:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 4
        struct.pack_into('<I', self._array, dst_offset, value)

    def get_ULInt32(self):
        if self._limit - self._position < 4:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 4
        return struct.unpack_from('<I', self._array, src_offset)[0]

    def put_SBInt64(self, value):
        if self._limit - self._position < 8:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 8
        struct.pack_into('>q', self._array, dst_offset, value)

    def get_SBInt64(self):
        if self._limit - self._position < 8:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 8
        return struct.unpack_from('>q', self._array, src_offset)[0]

    def put_UBInt64(self, value):
        if self._limit - self._position < 8:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 8
        struct.pack_into('>Q', self._array, dst_offset, value)

    def get_UBInt64(self):
        if self._limit - self._position < 8:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 8
        return struct.unpack_from('>Q', self._array, src_offset)[0]

    def put_SLInt64(self, value):
        if self._limit - self._position < 8:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 8
        struct.pack_into('<q', self._array, dst_offset, value)

    def get_SLInt64(self):
        if self._limit - self._position < 8:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 8
        return struct.unpack_from('<q', self._array, src_offset)[0]

    def put_ULInt64(self, value):
        if self._limit - self._position < 8:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 8
        struct.pack_into('<Q', self._array, dst_offset, value)

    def get_ULInt64(self):
        if self._limit - self._position < 8:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 8
        return struct.unpack_from('<Q', self._array, src_offset)[0]

    def put_BFloat32(self, value):
        if self._limit - self._position < 4:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 4
        struct.pack_into('>f', self._array, dst_offset, value)

    def get_BFloat32(self):
        if self._limit - self._position < 4:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 4
        return struct.unpack_from('>f', self._array, src_offset)[0]

    def put_LFloat32(self, value):
        if self._limit - self._position < 4:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 4
        struct.pack_into('<f', self._array, dst_offset, value)

    def get_LFloat32(self):
        if self._limit - self._position < 4:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 4
        return struct.unpack_from('<f', self._array, src_offset)[0]

    def put_BFloat64(self, value):
        if self._limit - self._position < 8:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 8
        struct.pack_into('>d', self._array, dst_offset, value)

    def get_BFloat64(self):
        if self._limit - self._position < 8:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 8
        return struct.unpack_from('>d', self._array, src_offset)[0]

    def put_LFloat64(self, value):
        if self._limit - self._position < 8:
            raise BufferOverflowError('Too many data to put')

        dst_offset = self._offset + self._position
        self._position += 8
        struct.pack_into('<d', self._array, dst_offset, value)

    def get_LFloat64(self):
        if self._limit - self._position < 8:
            raise BufferUnderflowError('Not enough data to get')

        src_offset = self._offset + self._position
        self._position += 8
        return struct.unpack_from('<d', self._array, src_offset)[0]

    def put_bool(self, value):
        if value:
            self.put_ULInt8(1)
        else:
            self.put_ULInt8(0)

    def get_bool(self):
        if self.get_ULInt8():
            return True
        else:
            return False

    def read_from_file(self, f):
        chunk = f.read(self._limit - self._position)
        length = len(chunk)

        if length:
            dst_offset = self._offset + self._position
            self._position += length
            self._array[dst_offset:dst_offset + length] = chunk

        return length

    def write_to_file(self, f):
        length = self._limit - self._position

        if length:
            src_offset = self._offset + self._position
            self._position = self._limit
            f.write(self._array[src_offset:src_offset + length])

        return length

    def read_from_socket(self, sock):
        chunk = sock.recv(self._limit - self._position)
        length = len(chunk)

        if length:
            dst_offset = self._offset + self._position
            self._position += length
            self._array[dst_offset:dst_offset + length] = chunk

        return length

    def write_to_socket(self, sock):
        length = self._limit - self._position

        if length:
            src_offset = self._offset + self._position
            length = sock.send(self._array[src_offset:src_offset + length])
            self._position += length

        return length

    def read_from_stream(self, stream):
        chunk = stream.read(self._limit - self._position)
        length = len(chunk)

        if length:
            dst_offset = self._offset + self._position
            self._position += length
            self._array[dst_offset:dst_offset + length] = chunk

        return length

    def write_to_stream(self, stream):
        length = self._limit - self._position

        if length:
            src_offset = self._offset + self._position
            length = stream.write(self._array[src_offset:src_offset + length])
            self._position += length

        return length
