from ext2 import block
from ext2 import superblock
from ext2 import inodetable
from ext2 import groupdescriptor


class BlockGroup(object):
    def __init__(self, data, block_size, blocks_per_group, group_id, sparse=False):
        memory_position = group_id * blocks_per_group * block_size
        data = data[memory_position:]

        self.blocks = []

        self.super_block = None
        self.group_descriptor = None
        self.inode_table = None

        self.get_blocks(data, block_size, blocks_per_group)

        self.sparse = sparse
        if sparse:
            self.get_sparse_super_block_feature(group_id)

        self.get_super_block()
        self.get_group_descriptor()
        self.get_inode_table()

    def get_blocks(self, data, block_size, blocks_per_group):
        for i in range(blocks_per_group):
            current_block = block.Block()
            current_block.get(data, i, block_size)

            self.blocks.append(current_block)

    def get_super_block(self):
        if not self.sparse:
            self.super_block = superblock.SuperBlock(self.blocks[0].data)

    def get_group_descriptor(self):
        group_descriptor_position = 1

        if self.sparse:
            group_descriptor_position = 0

        self.group_descriptor = groupdescriptor.GroupDescriptor(self.blocks[group_descriptor_position].data)

    def get_inode_table(self):
        inode_table_position = self.group_descriptor.bg_inode_table
        self.inode_table = inodetable.InodeTable(self.blocks[inode_table_position].data)

    def get_sparse_super_block_feature(self, group_id):
        if group_id == 0 or group_id == 8 or group_id == 34 or group_id == 128:
            self.sparse = False
