"""bitmap.py: EXT2 Bitmap for storing block or inode information."""

__author__ = "Frederik Bußmann"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Frederik Bußmann"
__email__ = "frederik@bussmann.io"


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
        file_input : bytes
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

    def compare_with_list(self, entries):
        """
        Compares a list of entries with a bitmap.

        Parameters
        ----------
        entries : list
            The list of elements to compare with the bitmap.

        Returns
        -------
        list
            All entries that have a corresponding positive entry in the bitmap.
        """

        positive_entries = []

        print(len(self))

        for i in range(len(self)):
            if self.get_bit(i) == 1:
                positive_entries.append(entries[i])

        return positive_entries

    def __len__(self):
        """
        Overrides the len function.

        Returns
        -------
        int
            The length of the bytearray that's making up the bitmap.
        """

        return len(self.bytes)
