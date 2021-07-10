from ext2 import stats
from ext2 import superblock
from ext2 import groupdescriptor
from ext2 import blockgroup


class File(object):
    def __init__(self):
        self.file_path = None
        self.file_name = None
        self.file_statistics = None

        self.super_block = None
        self.group_descriptor = None

        self.block_groups = []

    def read(self, file_path, file_name):
        data = open(file_path + file_name, "rb").read()

        self.file_path = file_path
        self.file_name = file_name

        self.get_super_block(data)
        self.get_group_descriptor(data)

        self.get_block_groups(data)

        self.file_statistics = stats.Stats(self)

    def print_statistics(self):
        print(self.file_statistics.to_string())

    def get_super_block(self, file_input):
        self.super_block = superblock.SuperBlock(file_input)

    def get_group_descriptor(self, file_input):
        block_size = self.super_block.s_block_size
        self.group_descriptor = groupdescriptor.GroupDescriptor(file_input[block_size:block_size*2])

    def get_block_groups(self, file_input):
        blocks_per_group = self.super_block.s_blocks_per_group
        block_size = self.super_block.s_block_size

        block_group_size = blocks_per_group * block_size

        i = 0

        while True:
            start_position = i*block_group_size
            end_position = i*block_group_size+block_group_size

            block_group = blockgroup.BlockGroup(file_input[start_position:end_position], blocks_per_group, block_size)

            if block_group.error:
                break

            self.block_groups.append(block_group)

            i += 1
