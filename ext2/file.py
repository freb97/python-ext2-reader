from ext2 import blockgroup
from ext2 import groupdescriptor
from ext2 import inodetable
from ext2 import stats
from ext2 import superblock


class File(object):
    def __init__(self):
        self.file_path = None
        self.file_name = None
        self.file_stats = None

        self.super_block = None
        self.block_size = None
        self.sparse_super = False

        self.block_groups = []

    def read(self, file_path, file_name):
        data = open(file_path + file_name, "rb").read()

        self.file_path = file_path
        self.file_name = file_name

        self.super_block = superblock.SuperBlock(data)
        self.block_size = self.super_block.s_block_size
        self.sparse_super = self.super_block.s_feature_compat >= 3

        blocks_per_group = self.super_block.s_blocks_per_group
        num_blocks_per_group = int(blocks_per_group / self.block_size)

        test = blockgroup.BlockGroup(data, self.block_size, num_blocks_per_group, 0, self.sparse_super)
        print(hex(test.super_block.s_magic))
        print(test.group_descriptor.bg_inode_table)
        print(test.inode_table.i_ctime)

        self.file_stats = stats.Stats(self)

    def stats(self):
        print(self.file_stats.to_string())
