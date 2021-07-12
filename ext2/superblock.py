"""superblock.py: EXT2 Super block for storing file system information."""

__author__ = "Frederik Bußmann"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Frederik Bußmann"
__email__ = "frederik@bussmann.io"


from ext2 import binaryreader


class SuperBlock(object):
    """
    Class representation of a super block.

    Attributes
    ----------
    reader : binaryreader.BinaryReader
        The reader used to extract values from the file input and track errors.
    s_inodes_count : int
        32bit value indicating the total number of inodes.
    s_blocks_count : int
        32bit value indicating the total number of blocks.
    s_r_blocks_count : int
        32bit value indicating the total number of blocks reserved for the usage of the super user.
    s_free_blocks_count : int
        32bit value indicating the total number of free blocks.
    s_free_inodes_count : int
        32bit value indicating the total number of free inodes.
    s_first_data_block : int
        32bit value identifying the first data block.
    s_log_block_size : int
        The block size is computed using this 32bit value as the number of bits to shift left the value 1024.
    s_log_frag_size : int
        The fragment size is computed using this 32bit value as the number of bits to shift left the value 1024.
    s_blocks_per_group : int
        32bit value indicating the total number of blocks per group.
    s_frags_per_group : int
        32bit value indicating the total number of fragments per group.
    s_inodes_per_group : int
        32bit value indicating the total number of inodes per group.
    s_mtime : int
        Unix timestamp of the last time the file system was mounted.
    s_wtime : int
        Unix timestamp of the last write access to the file system.
    s_mnt_count : half
        16bit value indicating how many time the file system was mounted since the last time it was fully verified.
    s_max_mnt_count : half
        16bit value indicating the max number of times the file system may be mounted before a full check is performed.
    s_magic : hex
        16bit value identifying the file system as Ext2.
    s_state : half
        16bit value indicating the file system state.
    s_errors : half
        16bit value indicating what the file system driver should do when an error is detected.
    s_minor_rev_level : half
        16bit value identifying the minor revision level within its revision level.
    s_lastcheck : int
        Unix timestamp of the last file system check.
    s_checkinterval : int
        Maximum Unix time interval, as defined by POSIX, allowed between file system checks.
    s_creator_os : int
        32bit identifier of the os that created the file system.
    s_rev_level : int
        32bit revision level value.
    s_def_resuid : half
        16bit value used as the default user id for reserved blocks.
    s_def_resgid : half
        16bit value used as the default group id for reserved blocks.
    s_first_ino : int
        32bit value used as index to the first inode useable for standard files.
    s_inode_size : half
        16bit value indicating the size of the inode structure.
    s_block_group_nr : half
        16bit value used to indicate the block group number hosting this super block structure.
    s_feature_compat : int
        32bit bitmask of compatible features.
    s_feature_incompat : int
        32bit bitmask of incompatible features.
    s_feature_ro_compat : int
        32bit bitmask of “read-only” features.
    s_block_size : int
        The precomputed s_log_block_size for convenient usage.
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

        self.s_inodes_count = self.reader.get_data_from_binary(0, 4, "<L")
        self.s_blocks_count = self.reader.get_data_from_binary(4, 8, "<L")
        self.s_r_blocks_count = self.reader.get_data_from_binary(8, 12, "<L")
        self.s_free_blocks_count = self.reader.get_data_from_binary(12, 16, "<L")
        self.s_free_inodes_count = self.reader.get_data_from_binary(16, 20, "<L")
        self.s_first_data_block = self.reader.get_data_from_binary(20, 24, "<L")
        self.s_log_block_size = self.reader.get_data_from_binary(24, 28, "<L")
        self.s_log_frag_size = self.reader.get_data_from_binary(28, 32, "<L")
        self.s_blocks_per_group = self.reader.get_data_from_binary(32, 36, "<L")
        self.s_frags_per_group = self.reader.get_data_from_binary(36, 40, "<L")
        self.s_inodes_per_group = self.reader.get_data_from_binary(40, 44, "<L")
        self.s_mtime = self.reader.get_data_from_binary(44, 48, "<L")
        self.s_wtime = self.reader.get_data_from_binary(48, 52, "<L")

        self.s_mnt_count = self.reader.get_data_from_binary(52, 54, "<H")
        self.s_max_mnt_count = self.reader.get_data_from_binary(54, 56, "<H")
        self.s_magic = self.reader.get_data_from_binary(56, 58, "<H")
        self.s_state = self.reader.get_data_from_binary(58, 60, "<H")
        self.s_errors = self.reader.get_data_from_binary(60, 62, "<H")
        self.s_minor_rev_level = self.reader.get_data_from_binary(62, 64, "<H")

        self.s_lastcheck = self.reader.get_data_from_binary(64, 68, "<L")
        self.s_checkinterval = self.reader.get_data_from_binary(68, 72, "<L")
        self.s_creator_os = self.reader.get_data_from_binary(72, 76, "<L")
        self.s_rev_level = self.reader.get_data_from_binary(76, 80, "<L")
        self.s_def_resuid = self.reader.get_data_from_binary(80, 82, "<H")
        self.s_def_resgid = self.reader.get_data_from_binary(82, 84, "<H")

        self.s_first_ino = self.reader.get_data_from_binary(84, 88, "<L")
        self.s_inode_size = self.reader.get_data_from_binary(88, 90, "<H")
        self.s_block_group_nr = self.reader.get_data_from_binary(90, 92, "<H")

        self.s_feature_compat = self.reader.get_data_from_binary(92, 96, "<L")
        self.s_feature_incompat = self.reader.get_data_from_binary(96, 100, "<L")
        self.s_feature_ro_compat = self.reader.get_data_from_binary(100, 104, "<L")

        self.s_block_size = 1024 << self.s_log_block_size
