import struct
from ext2 import superblock
from ext2 import groupdescriptor
from ext2 import inodetable
from ext2 import bitmap


class BlockGroup(object):
    def __init__(self, file_input, blocks_per_group, block_size):
        self.error = False

        self.blocks_per_group = blocks_per_group
        self.block_size = block_size

        self.super_block = None
        self.group_descriptor = None
        self.block_bitmap = None
        self.inode_bitmap = None
        self.inode_table = None
        self.data_blocks = None

        self.blocks = []

        self.get_blocks(file_input)
        self.check_for_super_block()

        block_bitmap_position = 0
        inode_bitmap_position = 1
        inode_table_position = 2

        if self.group_descriptor is not None:
            block_bitmap_position = self.group_descriptor.bg_block_bitmap
            inode_bitmap_position = self.group_descriptor.bg_inode_bitmap
            inode_table_position = self.group_descriptor.bg_inode_table

        self.block_bitmap = bitmap.BitMap(self.blocks[block_bitmap_position])
        self.inode_bitmap = bitmap.BitMap(self.blocks[inode_bitmap_position])
        self.get_inode_table(self.blocks[inode_table_position])

    def get_blocks(self, data):
        for i in range(self.blocks_per_group):
            block = data[i * self.block_size:i * self.block_size + self.block_size]
            self.blocks.append(block)

    def check_for_super_block(self):
        super_block_position = 1024
        s_magic_position_start = super_block_position + 56
        s_magic_position_end = super_block_position + 58

        try:
            s_magic = struct.unpack("<H", self.blocks[0][s_magic_position_start:s_magic_position_end])[0]

            if s_magic == 61267:
                self.get_super_block(self.blocks[0])
                self.get_group_descriptor(self.blocks[1])
        except struct.error:
            return
        except TypeError:
            return

    def get_super_block(self, data):
        self.super_block = superblock.SuperBlock(data)

        if self.super_block.reader.error:
            self.error = True

    def get_group_descriptor(self, data):
        self.group_descriptor = groupdescriptor.GroupDescriptor(data)

        if self.group_descriptor.reader.error:
            self.error = True

    def get_inode_table(self, data):
        self.inode_table = inodetable.InodeTable(data)

        if self.inode_table.reader.error:
            self.error = True
