from ext2 import binaryreader


class GroupDescriptor(object):
    def __init__(self, file_input):
        reader = binaryreader.BinaryReader(file_input)

        self.bg_block_bitmap = reader.getDataFromBinary(0, 4, "<I")
        self.bg_inode_bitmap = reader.getDataFromBinary(4, 8, "<I")
        self.bg_inode_table = reader.getDataFromBinary(8, 12, "<I")

        self.bg_free_blocks_count = reader.getDataFromBinary(12, 14, "<H")
        self.bg_free_inodes_count = reader.getDataFromBinary(14, 16, "<H")
        self.bg_used_dirs_count = reader.getDataFromBinary(16, 18, "<H")
