"""groupdescriptor.py: EXT2 Group descriptor for storing block group information."""

__author__ = "Frederik Bußmann"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Frederik Bußmann"
__email__ = "frederik@bussmann.io"


from ext2 import binaryreader


class GroupDescriptor(object):
    """
    Class representation of a group descriptor.

    Attributes
    ----------
    reader : binaryreader.BinaryReader
        The reader used to extract values from the file input and track errors.
    bg_block_bitmap : int
        32bit block id of the first block of the “block bitmap” for the group represented.
    bg_inode_bitmap : int
        32bit block id of the first block of the “inode bitmap” for the group represented.
    bg_inode_table : int
        32bit block id of the first block of the “inode table” for the group represented.
    bg_free_blocks_count : half
        16bit value indicating the total number of free blocks for the represented group.
    bg_free_inodes_count : half
        16bit value indicating the total number of free inodes for the represented group.
    bg_used_dirs_count : half
        16bit value indicating the number of inodes allocated to directories for the represented group.
    """

    def __init__(self, file_input):
        """
        Class constructor.

        Parameters
        ----------
        file_input : bytes
            The array of bytes representing the super block.
        """

        self.reader = binaryreader.BinaryReader(file_input)

        self.bg_block_bitmap = self.reader.get_data_from_binary(0, 4, "<L")
        self.bg_inode_bitmap = self.reader.get_data_from_binary(4, 8, "<L")
        self.bg_inode_table = self.reader.get_data_from_binary(8, 12, "<L")

        self.bg_free_blocks_count = self.reader.get_data_from_binary(12, 14, "<H")
        self.bg_free_inodes_count = self.reader.get_data_from_binary(14, 16, "<H")
        self.bg_used_dirs_count = self.reader.get_data_from_binary(16, 18, "<H")
