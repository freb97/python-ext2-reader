from ext2 import binaryreader


class InodeTable(object):
    def __init__(self, file_input):
        reader = binaryreader.BinaryReader(file_input)

        self.i_mode = hex(reader.getDataFromBinary(0, 2, "<H"))
        self.i_uid = reader.getDataFromBinary(2, 4, "<H")
        self.i_size = reader.getDataFromBinary(4, 8, "<I")
        self.i_atime = reader.getDataFromBinary(8, 12, "<I")
        self.i_ctime = reader.getDataFromBinary(12, 16, "<I")
        self.i_mtime = reader.getDataFromBinary(16, 20, "<I")
        self.i_dtime = reader.getDataFromBinary(20, 24, "<I")
        self.i_gid = reader.getDataFromBinary(24, 26, "<H")
        self.i_links_count = reader.getDataFromBinary(26, 28, "<H")
        self.i_blocks = reader.getDataFromBinary(28, 32, "<I")
        self.i_flags = reader.getDataFromBinary(32, 36, "<I")
        self.i_osd1 = reader.getDataFromBinary(36, 40, "<I")
        self.i_block = reader.getDataFromBinary(40, 44, "<I")
        self.i_generation = reader.getDataFromBinary(100, 104, "<I")
        self.i_file_acl = reader.getDataFromBinary(104, 108, "<I")
        self.i_dir_acl = reader.getDataFromBinary(108, 112, "<I")
        self.i_faddr = reader.getDataFromBinary(112, 116, "<I")
