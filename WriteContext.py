from myByteBuffer import *



class WriteContext(ByteBuffer):

    def writeFixedSizedString(self, p_string):
        for i in range(0, len(p_string) ):
            self.put_UBInt8(ord(p_string[i]))
        return len(p_string)


    def lenght(self):
        return self._position

    def writeNetworkStringUTF16(self,p_string):

        self.put_UBInt32(len(p_string) * 2);
        for i in range(0,len(p_string)):
            self.put_UBInt16(ord(p_string[i]))


    def get_buffer(self):
        new_buffer = bytearray(self._position)
        size = self._position
        self.set_position(0)
        w = self.get(new_buffer, 0,size)
        return new_buffer
