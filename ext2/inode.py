"""inode.py: EXT2 Inode for storing file information."""

__author__ = "Frederik Bußmann"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Frederik Bußmann"
__email__ = "frederik@bussmann.io"


from ext2 import binaryreader


class Inode(object):
    """
    Class representation of an inode.

    Attributes
    ----------
    reader : binaryreader.BinaryReader
        The reader used to extract values from the file input and track errors.
    i_mode : hex
        16bit value used to indicate the format of the described file and the access rights.
    i_uid : hex
        16bit user id associated with the file.
    i_size : int
        In revision 0, (signed) 32bit value indicating the size of the file in bytes. In revision 1 and later revisions,
        and only for regular files, this represents the lower 32-bit of the file size the upper 32-bit is located in the
        i_dir_acl.
    i_atime : int
        32bit value representing the number of seconds since january 1st 1970 of the last time this inode was accessed.
    i_ctime : int
        32bit value representing the number of seconds since january 1st 1970, of when the inode was created.
    i_mtime : int
        32bit value representing the number of seconds since january 1st 1970, of the last time this inode was modified.
    i_dtime : int
        32bit value representing the number of seconds since january 1st 1970, of when the inode was deleted.
    i_gid : half
        16bit value of the POSIX group having access to this file.
    i_links_count : half
        16bit value indicating how many times this particular inode is linked (referred to).
    i_blocks : int
        32-bit value representing the total number of 512-bytes blocks reserved to contain the data of this inode.
    i_flags : int
        32bit value indicating how the ext2 implementation should behave when accessing the data for this inode.
    i_osd1 : int
        32bit OS dependant value.
    i_block : int[15]
        15 x 32bit block numbers pointing to the blocks containing the data for this inode.
    i_generation : int
        32bit value used to indicate the file version (used by NFS).
    i_file_acl : int
        32bit value indicating the block number containing the extended attributes.
    i_dir_acl : int
        In revision 0 this 32bit value is always 0. In revision 1, for regular files this 32bit value contains the high
        32 bits of the 64bit file size.
    i_faddr : int
        32bit value indicating the location of the file fragment.
    """

    def __init__(self, file_input=None, index=0):
        """
        Class constructor.

        Parameters
        ----------
        file_input : bytes
            The array of bytes representing the inode.
        index : int
            The index of the inode.
        """

        self.reader = binaryreader.BinaryReader(file_input)

        self.i_inode = index
        self.i_mode = hex(self.reader.get_data_from_binary(0, 2, "<H"))
        self.i_uid = self.reader.get_data_from_binary(2, 4, "<H")
        self.i_size = self.reader.get_data_from_binary(4, 8, "<L")
        self.i_atime = self.reader.get_data_from_binary(8, 12, "<L")
        self.i_ctime = self.reader.get_data_from_binary(12, 16, "<L")
        self.i_mtime = self.reader.get_data_from_binary(16, 20, "<L")
        self.i_dtime = self.reader.get_data_from_binary(20, 24, "<L")
        self.i_gid = self.reader.get_data_from_binary(24, 26, "<H")
        self.i_links_count = self.reader.get_data_from_binary(26, 28, "<H")
        self.i_blocks = self.reader.get_data_from_binary(28, 32, "<L")
        self.i_flags = self.reader.get_data_from_binary(32, 36, "<L")
        self.i_osd1 = self.reader.get_data_from_binary(36, 40, "<L")

        self.i_block = []
        read_position = 40
        for i in range(15):
            inode_pointer = self.reader.get_data_from_binary(read_position, read_position + 4, "<L")
            self.i_block.append(inode_pointer)
            read_position += 4

        self.i_generation = self.reader.get_data_from_binary(100, 104, "<L")
        self.i_file_acl = self.reader.get_data_from_binary(104, 108, "<L")
        self.i_dir_acl = self.reader.get_data_from_binary(108, 112, "<L")
        self.i_faddr = self.reader.get_data_from_binary(112, 116, "<L")
