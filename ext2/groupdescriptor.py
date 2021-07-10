from ext2 import binaryreader


class GroupDescriptor(object):
    def __init__(self, file_input):
        self.reader = binaryreader.BinaryReader(file_input)

        self.bg_block_bitmap = self.reader.get_data_from_binary(0, 4, "<I")
        self.bg_inode_bitmap = self.reader.get_data_from_binary(4, 8, "<I")
        self.bg_inode_table = self.reader.get_data_from_binary(8, 12, "<I")

        self.bg_free_blocks_count = self.reader.get_data_from_binary(12, 14, "<H")
        self.bg_free_inodes_count = self.reader.get_data_from_binary(14, 16, "<H")
        self.bg_used_dirs_count = self.reader.get_data_from_binary(16, 18, "<H")
