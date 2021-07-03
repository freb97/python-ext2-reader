from ext2 import groupdescriptor
from ext2 import superblock
from ext2 import stats


class File(object):
    def __init__(self):
        self.file_path = None
        self.file_name = None
        self.file_stats = None

        self.super_block = None
        self.group_descriptor = None

    def read(self, file_path, file_name):
        data = open(file_path + file_name, "rb").read()

        self.file_path = file_path
        self.file_name = file_name

        read_position = 1024
        self.super_block = superblock.SuperBlock(data[read_position:])

        read_position = self.super_block.s_log_block_size
        self.group_descriptor = groupdescriptor.GroupDescriptor(data[read_position:])

        self.file_stats = stats.Stats(self)

    def stats(self):
        print(self.file_stats.toString())
