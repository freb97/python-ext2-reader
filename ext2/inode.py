from ext2 import binaryreader


class Inode(object):
    """
    Class representation of an inode.

    Attributes
    ----------
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
        16bit value indicating how many times this particular inode is linked (referred to). Most files will have a link
        count of 1. Files with hard links pointing to them will have an additional count for each hard link.
    i_blocks : int
        32-bit value representing the total number of 512-bytes blocks reserved to contain the data of this inode,
        regardless if these blocks are used or not. The block numbers of these reserved blocks are contained in the
        i_block array.
    i_flags : int
        32bit value indicating how the ext2 implementation should behave when accessing the data for this inode.
    """

    def __init__(self, file_input=None, index=0):
        """
        Class constructor.

        Parameters
        ----------
        file_input : bytearray
            The array of bytes representing the inode.
        """

        reader = binaryreader.BinaryReader(file_input)

        self.i_inode = index
        self.i_mode = hex(reader.get_data_from_binary(0, 2, "<H"))
        self.i_uid = reader.get_data_from_binary(2, 4, "<H")
        self.i_size = reader.get_data_from_binary(4, 8, "<L")
        self.i_atime = reader.get_data_from_binary(8, 12, "<L")
        self.i_ctime = reader.get_data_from_binary(12, 16, "<L")
        self.i_mtime = reader.get_data_from_binary(16, 20, "<L")
        self.i_dtime = reader.get_data_from_binary(20, 24, "<L")
        self.i_gid = reader.get_data_from_binary(24, 26, "<H")
        self.i_links_count = reader.get_data_from_binary(26, 28, "<H")
        self.i_blocks = reader.get_data_from_binary(28, 32, "<L")
        self.i_flags = reader.get_data_from_binary(32, 36, "<L")
        self.i_osd1 = reader.get_data_from_binary(36, 40, "<L")

        self.i_block = []
        read_position = 40
        for i in range(15):
            inode_pointer = reader.get_data_from_binary(read_position, read_position + 4, "<L")
            self.i_block.append(inode_pointer)
            read_position += 4

        self.i_generation = reader.get_data_from_binary(100, 104, "<L")
        self.i_file_acl = reader.get_data_from_binary(104, 108, "<L")
        self.i_dir_acl = reader.get_data_from_binary(108, 112, "<L")
        self.i_faddr = reader.get_data_from_binary(112, 116, "<L")
