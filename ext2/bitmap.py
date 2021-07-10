class BitMap(object):
    """
    Class representation of a bit map.

    Attributes
    ----------
    bytes : bytearray
        The bytes representing the bit map.

    Methods
    -------
    get_bit(index)
        Gets a bit in the bit map at a given index.
    to_string()
        Gets the bit map as a string of bits.
    get_ones_percentage()
        Gets the percentage of bits that represent a 1.
    """

    def __init__(self, file_input):
        """
        Class constructor.

        Parameters
        ----------
        file_input : int
            The array of bytes representing the bit map.
        """

        self.bytes = bytearray(file_input)

    def get_bit(self, index):
        """
        Gets a bit in the bit map at a given index.

        Parameters
        ----------
        index : int
            The index of the bit.

        Returns
        -------
        int
            The integer representation of the bit.
        """

        base = int(index // 8)
        shift = int(index % 8)

        return (self.bytes[base] & (1 << shift)) >> shift

    def to_string(self):
        """
        Gets the bit map as a string of bits.

        Returns
        -------
        str
            The string representation of the bits of the bitmap.
        """

        output = ""

        for byte in self.bytes:
            output += str(bin(byte))[2:]

        return output

    def get_ones_percentage(self):
        """
        Gets the percentage of bits that represent a 1.

        Returns
        -------
        float
            The percentage of ones in the bitmap.
        """

        bit_count = len(self.bytes) * 8
        ones = 0

        for i in range(bit_count):
            bit = self.get_bit(i)

            if bit == 1:
                ones += 1

        return ones / bit_count
