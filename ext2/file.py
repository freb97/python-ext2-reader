"""file.py: EXT2 Image file class representation."""

__author__ = "Frederik Bußmann"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Frederik Bußmann"
__email__ = "frederik@bussmann.io"


import math
from ext2 import binaryreader
from ext2 import bitmap
from ext2 import groupdescriptor
from ext2 import inode
from ext2 import stats
from ext2 import superblock


class File(object):
    """
    Class representation of an ext2 image file.

    Attributes
    ----------
    file_path : str
        The path to the file to read.
    file_name : str
        The name of the file to read.
    file_statistics : stats.Stats
        The cached file statistics instance.
    raw_data : bytes
        The raw file data in bytes.
    block_size : int
        The block size stored away for convenience.
    inode_size : int
        The inode size stored away for convenience.
    super_block : superblock.SuperBlock
        The cached super block instance.
    group_descriptors : groupdescriptor.GroupDescriptor[]
        All group descriptors in the file.
    block_bitmap : bitmap.BitMap
        The cached block bitmap instance.
    inode_bitmap : bitmap.BitMap
        The cached inode bitmap instance.
    inodes : inode.Inode[]
        All inodes in the file.
    used_inodes : inode.Inode[]
        All used inodes in the file according to the inode bitmap.

    Methods
    -------
    read(file_path, file_name)
        Reads a file at given path with a given name.
    """

    BLOCK_GROUP_DESCRIPTOR_SIZE: int = 32
    SUPER_BLOCK_OFFSET: int = 1024
    SUPER_BLOCK_SIZE: int = 1024

    def __init__(self):
        """
        Class constructor.
        """

        self.file_path = None
        self.file_name = None
        self.file_statistics = None

        self.raw_data = None

        self.block_size = 1024
        self.inode_size = 128

        self.super_block = None
        self.group_descriptors = []

        self.block_bitmap = None
        self.inode_bitmap = None

        self.inodes = []
        self.used_inodes = []

    def read(self, file_path, file_name):
        """
        Reads a file at given path with a given name.

        Parameters
        ----------
        file_path : str
            The path of the file to read.
        file_name : str
            The name of the file to read.
        """

        data = open(file_path + file_name, "rb").read()

        self.raw_data = data

        self.file_path = file_path
        self.file_name = file_name

        self.get_super_block(data[self.SUPER_BLOCK_OFFSET:self.SUPER_BLOCK_OFFSET + self.SUPER_BLOCK_SIZE])
        self.block_size = self.super_block.s_block_size
        self.inode_size = self.super_block.s_inode_size

        self.get_group_descriptors(data[self.block_size:])

        self.get_bitmaps()
        self.get_inodes()

        self.file_statistics = stats.Stats(self)

    def get_super_block(self, file_input):
        """
        Gets the super block from a given file input.

        Parameters
        ----------
        file_input : bytes
            The byte representation of the super block.
        """

        self.super_block = superblock.SuperBlock(file_input)

    def get_group_descriptors(self, file_input):
        """
        Gets the group descriptors from a given file input.

        Parameters
        ----------
        file_input : bytes
            The byte representation of the group descriptors.
        """

        group_count = int(math.ceil(self.super_block.s_inodes_count / self.super_block.s_inodes_per_group))
        read_position = 0

        for i in range(group_count):
            start_position = read_position
            end_position = read_position + self.BLOCK_GROUP_DESCRIPTOR_SIZE

            block_group_descriptor = groupdescriptor.GroupDescriptor(file_input[start_position:end_position])
            self.group_descriptors.append(block_group_descriptor)

            read_position += self.BLOCK_GROUP_DESCRIPTOR_SIZE

    def get_bitmaps(self):
        """
        Get the block bitmap and inode bitmap of the file.
        """

        block_bitmap_block = self.read_block(self.group_descriptors[0].bg_block_bitmap)
        inode_bitmap_block = self.read_block(self.group_descriptors[0].bg_inode_bitmap)

        self.block_bitmap = bitmap.BitMap(block_bitmap_block)
        self.inode_bitmap = bitmap.BitMap(inode_bitmap_block)

    def get_inodes(self):
        """
        Gets all inodes in the file.
        """

        # Determine number of inodes per group
        inodes_per_group = self.super_block.s_inodes_per_group

        # Determine size of the inode table block
        size = int((self.inode_size * inodes_per_group) / self.block_size)

        for group in self.group_descriptors:
            # Get inode table block from group descriptor
            block_data = self.read_block(group.bg_inode_table, size)

            for i in range(inodes_per_group):
                # Get inodes from inode table
                current_inode = block_data[i * self.inode_size:(i + 1) * self.inode_size]
                self.inodes.append(inode.Inode(current_inode, i))

        # Check for used inodes
        self.used_inodes = self.inode_bitmap.compare_with_list(self.inodes)

    def get_inode_blocks(self, input_inode):
        """
        Gets all blocks from a given inode.

        Parameters
        ----------
        input_inode : inode.Inode
            The inode to retrieve the blocks from.

        Returns
        -------
        bytearray
            All blocks from the inode stored linearly in a bytearray.
        """

        blocks = bytearray()

        # Iterate through all ids in i_block
        for i in range(len(input_inode.i_block)):
            if input_inode.i_block[i] != 0:
                block_id = input_inode.i_block[i]

                if i < 12:
                    blocks.extend(self.read_block(block_id))
                elif i == 12:
                    # Read first indirect block
                    blocks.extend(self.read_indirect_block(block_id, 1))
                elif i == 13:
                    # Read doubly indirect block
                    blocks.extend(self.read_indirect_block(block_id, 2))
                elif i == 14:
                    # Read triply indirect block
                    blocks.extend(self.read_indirect_block(block_id, 3))

        return blocks

    def read_block(self, index, number_of_blocks=1):
        """
        Reads a block of a given size at a given index.

        Parameters
        ----------
        index : int
            The index of the block to read.
        number_of_blocks : int
            The number of blocks to read.

        Returns
        -------
        bytes
            The block in bytes.
        """

        offset = index * self.block_size
        size = number_of_blocks * self.block_size

        return self.raw_data[offset:offset+size]

    def read_indirect_block(self, index, indirect_index=1):
        """
        Reads an indirect block of a given type at a given index.

        Parameters
        ----------
        index : int
            The index of the block to read.
        indirect_index : int
            The type of the indirect block (1 = indirect, 2 = doubly indirect, 3 = triply indirect).

        Returns
        -------
        bytes
            The block in bytes.
        """

        input_block = self.read_block(index)
        reader = binaryreader.BinaryReader(input_block)

        block = bytes()
        read_position = 0
        while read_position < len(input_block):
            block_id = reader.get_data_from_binary(read_position, read_position + 4, "<L")

            if block_id != 0:
                if indirect_index == 1:
                    block += self.read_block(block_id)

                elif indirect_index == 2:
                    block += self.read_indirect_block(block_id)

                elif indirect_index == 3:
                    indirect_block = self.read_indirect_block(block_id)
                    indirect_reader = binaryreader.BinaryReader(indirect_block)
                    indirect_read_position = 0

                    while indirect_read_position < len(indirect_block):
                        if indirect_block != 0:
                            indirect_block_id = indirect_reader.get_data_from_binary(indirect_read_position,
                                                                                     indirect_read_position + 4, "<L")
                            block += self.read_indirect_block(indirect_block_id)

                            indirect_read_position += 4

            read_position += 4

        return block

    def print_statistics(self):
        """
        Prints the statistics of the file.
        """

        print(self.file_statistics.get_statistics())
