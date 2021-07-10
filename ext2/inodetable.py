from ext2 import binaryreader


class InodeTable(object):
    def __init__(self, file_input):
        self.reader = binaryreader.BinaryReader(file_input)

        self.i_mode = hex(self.reader.get_data_from_binary(0, 2, "<H"))
        self.i_uid = self.reader.get_data_from_binary(2, 4, "<H")
        self.i_size = self.reader.get_data_from_binary(4, 8, "<I")
        self.i_atime = self.reader.get_data_from_binary(8, 12, "<I")
        self.i_ctime = self.reader.get_data_from_binary(12, 16, "<I")
        self.i_mtime = self.reader.get_data_from_binary(16, 20, "<I")
        self.i_dtime = self.reader.get_data_from_binary(20, 24, "<I")
        self.i_gid = self.reader.get_data_from_binary(24, 26, "<H")
        self.i_links_count = self.reader.get_data_from_binary(26, 28, "<H")
        self.i_blocks = self.reader.get_data_from_binary(28, 32, "<I")
        self.i_flags = self.reader.get_data_from_binary(32, 36, "<I")
        self.i_osd1 = self.reader.get_data_from_binary(36, 40, "<I")
        self.i_block = self.reader.get_data_from_binary(40, 44, "<I")
        self.i_generation = self.reader.get_data_from_binary(100, 104, "<I")
        self.i_file_acl = self.reader.get_data_from_binary(104, 108, "<I")
        self.i_dir_acl = self.reader.get_data_from_binary(108, 112, "<I")
        self.i_faddr = self.reader.get_data_from_binary(112, 116, "<I")
