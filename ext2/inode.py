from ext2 import binaryreader


class Inode(object):
    def __init__(self, file_input):
        reader = binaryreader.BinaryReader(file_input)

        self.i_mode = reader.get_data_from_binary(0, 2, "<H")
        self.i_uid = reader.get_data_from_binary(2, 4, "<H")
        self.i_size = reader.get_data_from_binary(4, 8, "<L")
        self.i_atime = reader.get_data_from_binary(8, 12, "<L")
        self.i_ctime = reader.get_data_from_binary(12, 16, "<L")
        self.i_mtime = reader.get_data_from_binary(16, 20, "<L")
        self.i_dtime = reader.get_data_from_binary(20, 24, "<L")
        self.i_gid = reader.get_data_from_binary(24, 26, "<H")
        self.i_links_count = reader.get_data_from_binary(26, 28, "<H")
        self.i_blocks = reader.get_data_from_binary(28, 32, "<L")
        self.i_flags = reader.get_data_from_binary(32, 36, "<L")
