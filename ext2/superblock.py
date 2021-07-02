from ext2 import binaryreader


class SuperBlock(object):
    def __init__(self, file_input):
        data = file_input[1024:4096]

        reader = binaryreader.BinaryReader(data)

        self.s_inodes_count = reader.getDataFromBinary(0, 4, "<L")
        self.s_blocks_count = reader.getDataFromBinary(4, 8, "<I")
        self.s_r_blocks_count = reader.getDataFromBinary(8, 12, "<I")
        self.s_free_blocks_count = reader.getDataFromBinary(12, 16, "<I")
        self.s_free_inodes_count = reader.getDataFromBinary(16, 20, "<I")
        self.s_first_data_block = reader.getDataFromBinary(20, 24, "<I")
        self.s_log_block_size = reader.getDataFromBinary(24, 28, "<I")
        self.s_log_frag_size = reader.getDataFromBinary(28, 32, "<I")
        self.s_blocks_per_group = reader.getDataFromBinary(32, 36, "<I")
        self.s_frags_per_group = reader.getDataFromBinary(36, 40, "<I")
        self.s_inodes_per_group = reader.getDataFromBinary(40, 44, "<I")
        self.s_mtime = reader.getDataFromBinary(44, 48, "<I")
        self.s_wtime = reader.getDataFromBinary(48, 52, "<I")

        self.s_mnt_count = reader.getDataFromBinary(52, 54, "<H")
        self.s_max_mnt_count = reader.getDataFromBinary(54, 56, "<H")
        self.s_magic = reader.getDataFromBinary(56, 58, "<H")
        self.s_state = reader.getDataFromBinary(58, 60, "<H")
        self.s_errors = reader.getDataFromBinary(60, 62, "<H")
        self.s_minor_rev_level = reader.getDataFromBinary(62, 64, "<H")

        self.s_lastcheck = reader.getDataFromBinary(64, 68, "<I")
        self.s_checkinterval = reader.getDataFromBinary(68, 72, "<I")
        self.s_creator_os = reader.getDataFromBinary(72, 76, "<I")
        self.s_rev_level = reader.getDataFromBinary(76, 80, "<I")
        self.s_def_resuid = reader.getDataFromBinary(80, 82, "<H")
        self.s_def_resgid = reader.getDataFromBinary(82, 84, "<H")

        self.s_first_ino = reader.getDataFromBinary(84, 88, "<I")
        self.s_inode_size = reader.getDataFromBinary(88, 90, "<H")
        self.s_block_group_nr = reader.getDataFromBinary(90, 92, "<H")
