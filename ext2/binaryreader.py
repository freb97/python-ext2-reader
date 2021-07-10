import struct


class BinaryReader(object):
    def __init__(self, data):
        self.binary_data = data
        self.error = False

    def get_data_from_binary(self, start_position, end_position, byte_format):
        if self.error:
            return 0

        raw_data = self.binary_data[start_position:end_position]

        try:
            data = struct.unpack(byte_format, raw_data)[0]

            return data
        except struct.error:
            self.error = True
            return 0
