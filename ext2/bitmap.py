class BitMap(object):
    def __init__(self, file_input):
        self.bytes = bytearray(file_input)

    def get_bit(self, index):
        base = int(index // 8)
        shift = int(index % 8)

        return (self.bytes[base] & (1 << shift)) >> shift

    def to_string(self):
        output = ""

        for byte in self.bytes:
            output += str(bin(byte))[2:]

        return output

    def get_ones_percentage(self):
        bit_count = len(self.bytes) * 8
        ones = 0

        for i in range(bit_count):
            bit = self.get_bit(i)

            if bit == 1:
                ones += 1

        return ones / bit_count
