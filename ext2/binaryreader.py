import struct


class BinaryReader(object):
    def __init__(self, data):
        self.binary_data = data

    def getDataFromBinary(self, start_position, end_position, byte_format):
        data = self.binary_data[start_position:end_position]

        return struct.unpack(byte_format, data)[0]
