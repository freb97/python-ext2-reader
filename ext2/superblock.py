from ext2 import binaryreader


class SuperBlock(object):
    def __init__(self, file_input):
        self.reader = binaryreader.BinaryReader(file_input)

        self.s_inodes_count = self.reader.get_data_from_binary(0, 4, "<L")
        self.s_blocks_count = self.reader.get_data_from_binary(4, 8, "<L")
        self.s_r_blocks_count = self.reader.get_data_from_binary(8, 12, "<L")
        self.s_free_blocks_count = self.reader.get_data_from_binary(12, 16, "<L")
        self.s_free_inodes_count = self.reader.get_data_from_binary(16, 20, "<L")
        self.s_first_data_block = self.reader.get_data_from_binary(20, 24, "<L")
        self.s_log_block_size = self.reader.get_data_from_binary(24, 28, "<L")
        self.s_log_frag_size = self.reader.get_data_from_binary(28, 32, "<L")
        self.s_blocks_per_group = self.reader.get_data_from_binary(32, 36, "<L")
        self.s_frags_per_group = self.reader.get_data_from_binary(36, 40, "<L")
        self.s_inodes_per_group = self.reader.get_data_from_binary(40, 44, "<L")
        self.s_mtime = self.reader.get_data_from_binary(44, 48, "<L")
        self.s_wtime = self.reader.get_data_from_binary(48, 52, "<L")

        self.s_mnt_count = self.reader.get_data_from_binary(52, 54, "<H")
        self.s_max_mnt_count = self.reader.get_data_from_binary(54, 56, "<H")
        self.s_magic = self.reader.get_data_from_binary(56, 58, "<H")
        self.s_state = self.reader.get_data_from_binary(58, 60, "<H")
        self.s_errors = self.reader.get_data_from_binary(60, 62, "<H")
        self.s_minor_rev_level = self.reader.get_data_from_binary(62, 64, "<H")

        self.s_lastcheck = self.reader.get_data_from_binary(64, 68, "<L")
        self.s_checkinterval = self.reader.get_data_from_binary(68, 72, "<L")
        self.s_creator_os = self.reader.get_data_from_binary(72, 76, "<L")
        self.s_rev_level = self.reader.get_data_from_binary(76, 80, "<L")
        self.s_def_resuid = self.reader.get_data_from_binary(80, 82, "<H")
        self.s_def_resgid = self.reader.get_data_from_binary(82, 84, "<H")

        self.s_first_ino = self.reader.get_data_from_binary(84, 88, "<L")
        self.s_inode_size = self.reader.get_data_from_binary(88, 90, "<H")
        self.s_block_group_nr = self.reader.get_data_from_binary(90, 92, "<H")

        self.s_feature_compat = self.reader.get_data_from_binary(92, 96, "<L")
        self.s_feature_incompat = self.reader.get_data_from_binary(96, 100, "<L")
        self.s_feature_ro_compat = self.reader.get_data_from_binary(100, 104, "<L")

        self.s_block_size = 1024 << self.s_log_block_size
