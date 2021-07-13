"""xattr.py: EXT2 Extended attributes for storing additional file information."""

__author__ = "Frederik Bußmann"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Frederik Bußmann"
__email__ = "frederik@bussmann.io"


from ext2 import binaryreader


class XAttrHeader(object):
    def __init__(self, file_input=None):
        """
        Class constructor.

        Parameters
        ----------
        file_input : bytes
            The array of bytes representing the extended attribute header.
        """

        self.reader = binaryreader.BinaryReader(file_input)

        self.h_magic = self.reader.get_data_from_binary(0, 4, "<L")
        self.h_refcount = self.reader.get_data_from_binary(4, 8, "<L")
        self.h_blocks = self.reader.get_data_from_binary(8, 12, "<L")
        self.h_hash = self.reader.get_data_from_binary(12, 16, "<L")

        self.reserved = []
        read_position = 16
        for i in range(4):
            reserved_pointer = self.reader.get_data_from_binary(read_position, read_position + 4, "<L")
            self.reserved.append(reserved_pointer)
            read_position += 4


class XAttrEntry(object):
    def __init__(self, file_input=None):
        """
        Class constructor.

        Parameters
        ----------
        file_input : bytes
            The array of bytes representing the extended attribute entry.
        """

        self.reader = binaryreader.BinaryReader(file_input)

        self.e_name_len = self.reader.get_data_from_binary(0, 1, "<L")
        self.e_name_index = self.reader.get_data_from_binary(1, 2, "<L")
        self.e_value_offs = self.reader.get_data_from_binary(2, 4, "<H")
        self.e_value_block = self.reader.get_data_from_binary(4, 8, "<L")
        self.e_value_size = self.reader.get_data_from_binary(8, 12, "<L")
        self.e_hash = self.reader.get_data_from_binary(12, 16, "<L")

        self.e_name = ""

        read_position = 16
        for i in range(self.e_name_len):
            char = chr(self.reader.get_data_from_binary(read_position, read_position + 4, "<L"))
            self.e_name += char
