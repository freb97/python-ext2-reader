class Stats(object):
    def __init__(self, file):
        self.file_name = file.file_name

        self.block_size = file.super_block.s_block_size
        self.blocks_per_group = file.super_block.s_blocks_per_group / self.block_size
        self.block_group_count = len(file.block_groups)
        self.free_blocks = file.group_descriptor.bg_free_blocks_count

        self.magic_number = hex(file.super_block.s_magic)
        self.creator_os = self.get_creator_os_name(file.super_block.s_creator_os)

        self.inode_size = file.super_block.s_inode_size
        self.free_inodes = file.group_descriptor.bg_free_inodes_count

        self.br = "\n"
        self.tab = "\t"
        self.output = ""

    def to_string(self):
        if self.output != "":
            return self.output

        self.output = "EXT2 File statistics for file \"" + self.file_name + "\":" + "\n\n"

        self.formatted_line("Magic number (must equal 0xef53)", str(self.magic_number), 2)
        self.formatted_line("Created on OS", self.creator_os, 7)
        self.formatted_line()

        self.formatted_line("Block size", str(self.block_size), 8)
        self.formatted_line("Blocks per group", str(int(self.blocks_per_group)), 6)
        self.formatted_line("Block group count", str(int(self.block_group_count)), 6)
        self.formatted_line("Free blocks count", str(int(self.free_blocks)), 6)
        self.formatted_line()

        self.formatted_line("Inode size", str(int(self.inode_size)), 8)
        self.formatted_line("Free inode count", str(int(self.free_inodes)), 6)

        return self.output

    def formatted_line(self, title="", content="", tab_size=0):
        if title != "":
            title += ":"

        self.output += title + tab_size * self.tab + content + self.br

    @staticmethod
    def get_creator_os_name(creator_os):
        os_name = "Not specified"

        if creator_os == 0:
            os_name = "Linux"
        elif creator_os == 1:
            os_name = "GNU Hurd"
        elif creator_os == 2:
            os_name = "Masix"
        elif creator_os == 3:
            os_name = "FreeBSD"
        elif creator_os == 4:
            os_name = "Lites"

        return os_name
