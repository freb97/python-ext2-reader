import math
from ext2 import binaryreader
from ext2 import bitmap
from ext2 import groupdescriptor
from ext2 import inode
from ext2 import stats
from ext2 import superblock


class File(object):
    BLOCK_GROUP_DESCRIPTOR_SIZE = 32
    SUPER_BLOCK_OFFSET = 1024
    SUPER_BLOCK_SIZE = 1024

    def __init__(self):
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

    def read(self, file_path, file_name):
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

    def print_statistics(self):
        print(self.file_statistics.get_statistics())

    def get_super_block(self, file_input):
        self.super_block = superblock.SuperBlock(file_input)

    def get_bitmaps(self):
        self.block_bitmap = bitmap.BitMap(self.read_block(self.group_descriptors[0].bg_block_bitmap))
        self.inode_bitmap = bitmap.BitMap(self.read_block(self.group_descriptors[0].bg_inode_bitmap))

    def get_group_descriptors(self, file_input):
        group_count = int(math.ceil(self.super_block.s_inodes_count / self.super_block.s_inodes_per_group))
        read_position = 0

        for i in range(group_count):
            start_position = read_position
            end_position = read_position + self.BLOCK_GROUP_DESCRIPTOR_SIZE

            block_group_descriptor = groupdescriptor.GroupDescriptor(file_input[start_position:end_position])
            self.group_descriptors.append(block_group_descriptor)

            read_position += self.BLOCK_GROUP_DESCRIPTOR_SIZE

    def get_inodes(self):
        inodes_per_group = self.super_block.s_inodes_per_group
        size = int((self.inode_size * inodes_per_group) / self.block_size)

        for group in self.group_descriptors:
            block_data = self.read_block(group.bg_inode_table, size)

            for i in range(inodes_per_group):
                current_inode = block_data[i * self.inode_size:(i + 1) * self.inode_size]
                self.inodes.append(inode.Inode(current_inode, i + 1))

    def get_inode_blocks(self, input_inode):
        blocks = bytearray()

        for i in range(len(input_inode.i_block)):
            if input_inode.i_block[i] != 0:
                block_id = input_inode.i_block[i]

                if i < 12:
                    blocks.extend(self.read_block(block_id))
                elif i == 12:
                    blocks.extend(self.read_indirect_block(block_id, 1))
                elif i == 13:
                    blocks.extend(self.read_indirect_block(block_id, 2))
                elif i == 14:
                    blocks.extend(self.read_indirect_block(block_id, 3))

        return blocks

    def read_block(self, index, number_of_blocks=1):
        offset = index * self.block_size
        size = number_of_blocks * self.block_size

        return self.raw_data[offset:offset+size]

    def read_indirect_block(self, index, indirect_index=1):
        input_block = self.read_block(index)
        reader = binaryreader.BinaryReader(input_block)

        block = bytes()
        read_position = 0
        while read_position < len(input_block):
            block_id = reader.get_data_from_binary(read_position, read_position + 4, "<L")

            if block_id != 0:
                if indirect_index == 1:
                    block += self.read_block(block_id)  # First indirect block
                elif indirect_index == 2:
                    block += self.read_indirect_block(block_id)  # Doubly indirect block
                elif indirect_index == 3:
                    block += self.read_indirect_block(self.read_indirect_block(block_id))  # Triply indirect block

            read_position += 4

        return block
