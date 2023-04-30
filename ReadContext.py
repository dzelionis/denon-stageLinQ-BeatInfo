from myByteBuffer import ByteBuffer
import codecs

def fromCString(p_buffer):
    #arr = str(fromCharCode.apply(null, p_buffer).split('\0');
    arr = codecs.utf_8_decode(p_buffer)

    # assert (arr.length > 0);
    return arr[0]






class ReadContext(ByteBuffer):



    p_buffer = bytearray()
    p_littleEndian = False


    def read(self, p_bytes):

        bytesToRead = min(self.get_remaining(), p_bytes);
        if bytesToRead <= 0:
            return None

        #self.set_position(bytesToRead)
        src_offset = self._position

        view = self._array[src_offset:src_offset + p_bytes]
        #view = ReadContext(self.get_buffer(), self._position - bytesToRead, bytesToRead)
        #self._offset += self._position
        self._position += p_bytes
        #view._position += bytesToRead
        return view


    def readRemaining(self):
        return self.read(self.has_remaining())


    def readRemainingAsNewBuffer(self):
        view = self.readRemaining()
        newArrayBuffer = view._array.slice(view.byteOffset, view.byteOffset + view.length);
        return newArrayBuffer

    def getString(self, p_bytes):
        buf = self.read(p_bytes)
        if buf is not None:
            return fromCString(buf)
        else:
            return ""

    def readNetworkStringUTF16(self):
        # node.js only supports little endian of UTF16, and we need big endian, so read one by one
        bytes = self.get_UBInt32();
        #print(bytes)
        assert (bytes <= self.get_limit())
        assert (bytes % 2 == 0);
        # Should be 2 bytes per character; otherwise
        result = '';
        for i in range(0, int(bytes/2)):
            result += chr(self.get_UBInt16());
        return result;




    def readFixedSizedString(self, p_string):
        for i in range(0, len(str(p_string)) ):
            self.get_UBInt8(ord(p_string[i]))
        return len(p_string)


    def lenght(self):
        return self._length

    def get_buffer(self):
        new_buffer = bytearray(self._position)
        size = self._position
        self.set_position(0)
        w = self.get(new_buffer, 0, size)
        return w
#    def readNetworkStringUTF16(self,p_string):#
#
#        self.read_UBInt32(len(p_string) * 2);
#        for i in range(0,len(p_string)):
#            self.readUInt16(ord(p_string[i]))


    #def get_buffer(self):
    #    new_buffer = bytearray(self._position)
    #    size = self._position
    #    self.set_position(0)
    #    w = self.get(new_buffer, 0,size)
    #    return new_buffer
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
